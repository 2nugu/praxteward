#!/usr/bin/env python3
"""Diagnose machine-written Korean prose and gate a revision. Standard library only.

Usage:
  python3 ko_scan.py <file> [--genre G]              diagnose: spans by severity, metrics, score, route
  python3 ko_scan.py <revised> --base <original>     also gate the revision and grade it A to D
  python3 ko_scan.py <file> --length N               report length against a target of N characters (±5%)
  python3 ko_scan.py <file> --voice <sample>         compare rhythm metrics with a writing sample
  add --json for machine-readable output
Genres: general (default), report, column, essay, news, academic, legal, medical, policy, marketing, chat, fiction.
A genre turns off patterns that are its convention (hedges in legal text, section headings in academic text).
Pattern IDs follow references/korean.md. Exit codes: 0 no S1 finding and gates pass, 1 otherwise, 2 usage error.
Thresholds are starting points, not calibrated against a human-written corpus; read every span before editing.
"""
import difflib, json, os, re, statistics, sys

WEIGHT = {"S1": 5.0, "S2": 2.0, "S3": 0.5}
GENRES = ("general", "report", "column", "essay", "news", "academic", "legal", "medical", "policy",
          "marketing", "chat", "fiction", "slides")
HEDGED = {"A-10", "G-1", "G-2", "I-5", "K-13"}
GENRE_OFF = {
    "legal": HEDGED | {"F-4", "K-3", "A-5"}, "medical": HEDGED | {"F-4"}, "policy": HEDGED | {"F-7"},
    "academic": {"C-3", "C-10", "F-4", "A-4", "J-4"}, "news": {"K-20", "I-1"},
    "fiction": {"A-16", "A-16a", "D-13", "D-14", "F-1", "E-7", "K-10"}, "essay": {"D-13"},
    "chat": {"C-3", "E-3"},
    "slides": {"C-2", "C-3", "C-6", "C-10", "J-1", "K-31", "E-1", "E-2", "E-3"},
}
N = r"(?<![가-힣])"  # word start

# (id, severity, regex, scope, threshold). scope: "each" flags every hit; "para" flags when one paragraph
# reaches the threshold; "doc" when the document does; "tail" every hit in the last 30% of the text;
# "density" when hits exceed one per <threshold> characters.
PATTERNS = [
    # A. Translationese
    ("A-1", "S2", r"에 대해서?(?![가-힣])", "para", 3),
    ("A-2", "S2", r"[을를] 통해서?", "para", 3),
    ("A-3", "S2", r"에 있어서?(?![가-힣])|에게 있어서?(?![가-힣])|하는 데 있어서?(?![가-힣])", "each", 1),
    ("A-4", "S2", r"라는 점에서", "doc", 3),
    ("A-5", "S3", r"[와과] 관련(하여|된|해서?|한)|에 관해서?(?![가-힣])|에 관하여", "each", 1),
    ("A-6", "S2", r"에 기반(하여|한|해)|[을를] 바탕으로", "doc", 3),
    ("A-7", "S2", r"[을를] (가지고|갖고) 있", "each", 1),
    ("A-7a", "S3", r"(의미|가치|관심|특징|장점|단점|능력|역사)[을를] (가지|가진|갖는|갖)", "each", 1),
    ("A-8", "S1", r"되어지|되어졌|되어질|지어지|불려지|쓰여지|보여지", "each", 1),
    ("A-9", "S2", r"에 의해 [^.\n]{0,30}?(되었|됐|된다|되는|되고|됩니다|되어)", "each", 1),
    ("A-10", "S2", r"할 수 있(다|습니다)", "doc", 4),
    ("A-11", "S2", r"[을를] 위해서?(?![가-힣])|기 위해서?(?![가-힣])", "para", 3),
    ("A-12", "S3", r"만들어지|만들어졌|이루어지|이루어졌", "each", 1),
    ("A-14", "S2", r"[다요]\. 그리고 ", "doc", 3),
    ("A-15", "S2", r"[을를] (보여준다|보여줍니다|제공한다|제공합니다)", "each", 1),
    ("A-16", "S3", N + r"(그는|그가|그를|그의|그에게|그들은|그들이|그들을|그들의|그것은|그것이|그것을|그것의|이것은|이것이|이것을)(?![가-힣])", "doc", 5),
    ("A-16a", "S1", N + r"그녀", "each", 1),
    ("A-19", "S2", r"에서의|으로부터의|로부터의|에로의|으로의|[과와]의(?![가-힣])|에게서의", "doc", 4),
    ("A-20", "S2", r"(되|지)고 있(다|습니다)", "para", 3),
    ("A-21", "S2", r"단순한 [^.\n]{1,30}?[을를] 넘어|단순히 [^.\n]{1,20}?[을를] 넘어", "each", 1),
    ("A-22", "S3", r"(명확|분명)(하다|합니다)", "each", 1),
    ("A-23", "S2", r"(발판|토대|기반|초석)[을를] (마련|다지|놓)|지평[을를] (열|넓)", "each", 1),
    ("A-24", "S2", r"더 이상 [^.\n]{0,20}?않", "doc", 2),
    ("A-25", "S3", r"에 위치(한|하고|해 있)", "each", 1),
    ("A-26", "S2", r"(으로|로) 구성되어 있|(으로|로) 이루어져 있", "doc", 2),
    ("A-27", "S2", r"[을를] 포함한|[을를] 포함하여", "doc", 3),
    # B. English terms
    ("B-2", "S2", N + r"(인사이트|솔루션|시너지|퍼포먼스|레버리지|임팩트|니즈|이니셔티브|어젠다|밸류|모멘텀|퀄리티|트랜스포메이션)", "doc", 3),
    # C. Structure (C-2, C-3, C-10, E-3 and K-20 are structural, below)
    ("C-1", "S2", N + r"(첫째|둘째|셋째|넷째)[,는 ]", "doc", 3),
    ("C-7", "S2", r"(^|[.!?]\s+)먼저[, ][^.\n]*[.!?]\s+[^.\n]*반면[, ][^.\n]*[.!?]\s+[^.\n]*결국", "each", 1),
    ("C-8", "S1", r"[이가] 아니라|인가,\s*[^.?\n]{1,25}인가|도, [^.\n]{2,30}도 아니", "doc", 2),
    ("C-9", "S2", r"(^|\s)[1-9]\)\s", "each", 1),
    ("C-11", "S3", r"[가-힣](고|며|지만|는데|면서|으며|거나|어서|아서|해서|니까|므로),", "density", 90),
    ("C-13", "S2", r"[가-힣]{2,}(은|는|이|가),\s", "doc", 2),
    ("C-14", "S2", r"(^|[.!?]\s+)(또한|그러나|따라서|하지만|그리고|게다가|결과적으로|그럼에도|이에|더불어|아울러|한편|특히),", "doc", 3),
    # D. Stock phrases
    ("D-1", "S1", r"결론적으로|따라서|이를 통해|그러므로|요컨대|종합하면", "doc", 4),
    ("D-2", "S1", r"시사하는 바가 크|시사점을 (준|던지)|의의가 크|주목할 만하|눈여겨볼 만하|큰 의미를 지닌", "each", 1),
    ("D-3", "S1", r"(두|세|네|다섯) 가지로 (나눌|정리할|요약할|살펴볼) 수 있|다음과 같(습니다|다)\s*[:：]", "each", 1),
    ("D-4", "S1", r"혁신적|획기적|압도적|폭발적|게임 체인저|패러다임 전환|새로운 차원", "doc", 3),
    ("D-5", "S2", N + r"(데이터|시장|기술|인공지능|AI|사회|역사|숫자|현실|결과|통계|지표)(가|이|는|은) (말해준다|말해줍니다|말한다|보여준다|요구한다|원한다|증명한다)", "each", 1),
    ("D-6", "S2", r"[가-힣] 때(다|이다|입니다)\.|시점(입니다|이다)\.", "each", 1),
    ("D-7", "S2", r"에서 [^.\n]{1,15}?(으로|로)의 전환|[을를] 넘어 [^.\n]{1,15}?(으로|로) ", "doc", 2),
    ("D-8", "S2", r"필요한 것은 [^.\n]{1,30}?(이다|입니다)|문제는 [^.\n]{1,30}?(이다|입니다)\.|중요한 것은 [^.\n]{1,30}?(이다|입니다)", "each", 1),
    ("D-9", "S2", r"(으로|로) 이어(진다|집니다)|[과와] 직결|(으로|로) 귀결", "doc", 2),
    ("D-10", "S2", r"(하는|인|한) 이유(다|입니다)\.", "each", 1),
    ("D-11", "S2", r"(^|[.!?]\s+)(향후|앞으로|중장기적으로|장기적으로)", "tail", 1),
    ("D-12", "S2", r"과제(도|가) 남아 있|한계(도|가) 존재|해결해야 할 과제", "each", 1),
    ("D-13", "S2", N + r"(어쩌면|비로소|문득|그렇게 우리는|결국 우리는)", "tail", 1),
    ("D-14", "S2", N + r"(나침반|등대|청사진|이정표|여정|퍼즐 조각|양날의 검|촉매|원동력|빙산의 일각|첫걸음|날개를 달|물꼬를 트|새 장을 열|막을 올리|한 획을 긋|신호탄|마중물|디딤돌|초석|DNA|풍경이 되|풍경이다|민낯|현주소|자화상|숙제로 남|숙제다|숙제입니다|갈림길|기로에 서|시험대|분수령|골든타임|터널의 끝)", "doc", 2),
    ("D-15", "S1", r"도움이 되(셨|었)길|궁금한 점이 있으시면|살펴보겠습니다|알아보겠습니다|좋은 질문입니다|정리해 드리겠습니다|말씀드리겠습니다", "each", 1),
    # F. Modifiers and redundancy
    ("F-1", "S2", N + r"(매우|정말|굉장히|상당히|아주|너무나|대단히|극도로)(?![가-힣])", "density", 300),
    ("F-2", "S2", r"(중요하고 핵심적|핵심적이고 중요|다양하고 폭넓|빠르고 신속|명확하고 분명|분명하고 명확|효율적이고 효과적|효과적이고 효율적|새롭고 혁신|혁신적이고 새로)", "each", 1),
    ("F-4", "S2", r"[가-힣]{1,4}(적|성|화)(인|이|을|를|의|으로|에|은|는|된|하)(?=\s)", "doc", 13),
    ("F-5", "S2", r"[가-힣]{2,}적(인)? [가-힣]{1,6}(의|을|를|과|와|에)? [가-힣]{2,}적(인)? ", "doc", 2),
    ("F-7", "S2", r"(강화|확대|개선|제고|활성화|고도화|내실화|극대화|최적화)", "doc", 5),
    # G. Hedging
    ("G-1", "S2", r"(으로|로) 보(인다|입니다)", "doc", 3),
    ("G-2", "S2", r"(것으로|것이라고) (보인다|생각된다|판단된다|예상된다|사료된다)|할 수 있을 것(으로|이)|ㄹ 수도 있을 것", "each", 1),
    # H. Connectives
    ("H-1", "S2", r"(^|[.!?]\s+)(또한|따라서|즉|나아가|게다가|더불어|아울러|특히)[ ,]", "para", 3),
    ("H-3", "S2", r"(^|[.!?]\s+)(이는|이 점에서|이 말은|이처럼|이와 같이)\s", "para", 3),
    ("H-4", "S2", r"(^|[.!?]\s+)즉,", "doc", 3),
    # I. Formal nouns
    ("I-1", "S2", r"것(이다|입니다)\.", "para", 3),
    ("I-2", "S2", r"(는|ㄴ|은|한) (점이다|점입니다|바이다|바입니다|바 있)", "doc", 3),
    ("I-3", "S2", r"라는 (것|뜻|의미)(이다|입니다)", "doc", 3),
    ("I-5", "S2", r"[이가] 필요(하다|합니다)|할 필요가 있|하는 것이 필요", "doc", 3),
    ("I-6", "S2", r"[가-힣]{2,}능력", "doc", 3),
    # J. Decoration
    ("J-3", "S2", r"—", "doc", 3),
    # K. Generative-Korean patterns (Praxteward additions)
    ("K-1", "S1", r"가장 [^.\n]{1,25}? (것|곳|사람|기업|도시|요소|방법|기술|문제|사례)? ?중 (하나|한 곳|한 명)", "each", 1),
    ("K-2", "S1", r"(하는|되는) 것이 가능(하다|합니다|한)|[이가] 가능(해졌|해집|하게 되)", "each", 1),
    ("K-3", "S2", r"[을를] (진행|수행|실시)(하|했|합|한|해|됩|된)", "doc", 2),
    ("K-4", "S2", r"역할을 (하|한다|합니다|했|수행)|중요한 역할|핵심적인 역할", "each", 1),
    ("K-5", "S2", r"에 초점을 (맞추|맞춘|두)|에 주목(하|해)|에 중점을 (두|둔)", "doc", 2),
    ("K-6", "S2", r"(으로|로) 인해", "doc", 3),
    ("K-7", "S2", N + r"(이러한|이와 같은|이같은|해당)(?![가-힣])", "doc", 4),
    ("K-8", "S2", N + r"(효과적으로|지속적으로|적극적으로|체계적으로|원활하게|다양한|효율적으로|전반적으로|본격적으로)(?![가-힣])", "doc", 5),
    ("K-9", "S2", N + r"여러분|해 ?보세요|하시길 바랍니다|하는 것이 좋습니다|추천드립니다|도움이 될 것입니다|잊지 마세요|권합니다|권해 드립니다|하시길 권", "doc", 2),
    ("K-10", "S2", r"(^|[.!?]\s+)만약 ", "doc", 2),
    ("K-11", "S2", r"[^.\n]{2,}의 [가-힣]{1,8}의 [가-힣]{1,8}의 ", "each", 1),
    ("K-12", "S2", N + r"(약|대략) [\d.,]+ ?[^\s.]{0,4} ?(정도|가량|쯤)", "each", 1),
    ("K-13", "S2", r"(할|될|하게 될|되게 될) 것(이다|입니다)", "doc", 3),
    ("K-14", "S2", r"하는 경향이 있|할 가치가 있|에도 불구하고", "doc", 2),
    ("K-15", "S3", r"지 않을 수 없|하는 중(이다|입니다)", "doc", 2),
    ("K-16", "S2", r"에 대한 [가-힣]{1,6}(의 )?(이해|고민|논의|접근|분석|관심|인식)", "doc", 3),
    ("K-17", "S2", r"할 수 있도록", "doc", 3),
    ("K-18", "S2", r"(합니다|입니다|습니다|세요)!", "doc", 2),
    ("K-23", "S1", r"(이 글에서는|이번 글에서는|이 글은|오늘은) [^.\n]{0,40}?(알아보|살펴보|정리해 보|정리하려|소개해 드리|소개하려|이야기해 보|다뤄 보|짚어 보)", "each", 1),
    ("K-24", "S1", r"(느냐|는지|하기)에 따라 [^.\n]{0,15}?달라(진다|집니다|질 수)|에 따라 (결과|성패|모든 것)[이가] (크게 )?달라", "each", 1),
    ("K-25", "S1", r"(원하시면|필요하시면|궁금하시면|더 궁금한|추가로 궁금한)[^.\n]{0,50}?(알려 ?주|말씀해 ?주|도와|드리겠|드릴게|보겠습니다)", "each", 1),
    ("K-26", "S2", r"것만으로도", "doc", 2),
    ("K-27", "S2", r"(그 자체로|이미) [^.\n]{0,20}?(신호|첫걸음|용기|시작)|해도 괜찮(습니다|아요)|당연한 (감정|일|반응)(입니다|이에요)|자연스러운 (감정|반응|일)(입니다|이에요)|충분히 (잘하고|노력하고)", "each", 1),
    ("K-28", "S3", r"(^|[.!?]\s+)(결론부터 말하면|한마디로 말하면|요약하면|간단히 말해),", "each", 1),
    ("K-29", "S2", r"(잊어서는|간과해서는|외면해서는) 안 (된다|됩니다)\.|(가볍게|쉽게) 넘길 (일|문제)이 아니", "each", 1),
    ("K-30", "S2", r"양측 모두|모두가 [^.\n]{0,15}?(한 걸음|머리를 맞대)|머리를 맞대", "each", 1),
]
COMPILED = [(i, s, re.compile(r, re.M), sc, t) for i, s, r, sc, t in PATTERNS]
FIX = {
    "A-1": "목적격으로 직결", "A-2": "일부를 '~로', '~해서'로", "A-3": "'에서', '~하는 데', '~에게'", "A-4": "'~서', '~라는 이유로'",
    "A-5": "'~에', '~의', '~을'", "A-6": "'~로', '~을 보고'", "A-7": "'~가 있다', 형용사 서술, 이중주어", "A-8": "능동 또는 단일 피동",
    "A-9": "행위자를 주어로", "A-10": "형태만 분산, 단정으로 바꾸지 않음", "A-11": "'~려고', '~도록', 생략", "A-12": "능동 동사",
    "A-14": "연결어미 '-고', '-며'로 잇기", "A-15": "구체 주어, '~에 따르면'", "A-16": "주어 생략 또는 명사구로 되짚기",
    "A-16a": "이름이나 명사구, 또는 생략", "A-19": "절로 풀어쓰기", "A-20": "일부를 추세 단언으로", "A-21": "'X만이 아니라 Y다'",
    "A-22": "명제를 바로 단언", "A-23": "실제 내용으로", "A-24": "'이제'로", "A-25": "'~에 있는'", "A-26": "'~로 되어 있다', 나열",
    "A-27": "'~까지', '~와', 나열", "B-2": "한국어로, 표준 기술 용어는 유지", "C-1": "본문에 녹이거나 변주",
    "C-7": "둘을 지우고 본문에 녹이기", "C-8": "하나만 남기고 비대칭 서술로, 전부 지우지 않음", "C-9": "본문에 녹이기",
    "C-11": "쉼표 삭제", "C-13": "조사 뒤 쉼표 삭제", "C-14": "문두 접속어 뒤 쉼표 삭제 또는 접속어 삭제",
    "D-1": "1~2건만 남김", "D-2": "삭제 또는 구체 결론", "D-3": "도입구 삭제", "D-4": "수치·사실로", "D-5": "실제 행위자 주어로",
    "D-6": "구체 동사 단언", "D-7": "직접 단언", "D-8": "주어-서술 직결", "D-9": "인과 경로를 구체로", "D-10": "순방향 단언",
    "D-11": "실제 시점·조건으로, 없으면 삭제", "D-12": "실제 과제를 바로", "D-13": "구체 서술로", "D-14": "직설로, 가장 나은 하나만",
    "D-15": "삭제", "F-1": "대부분 삭제", "F-2": "하나만 남김", "F-4": "동사·형용사 어근으로", "F-5": "동사구로 해체",
    "F-7": "구체 행위 동사로", "G-1": "유보 강도는 두고 형태만 변주", "G-2": "완곡 하나만, 확신도 유지", "H-1": "그 문단의 절반 정도 삭제",
    "H-2": "역접 표지를 절반 이하로", "H-3": "본 서술로 직진", "H-4": "생략 또는 '곧'", "I-1": "일부를 확정 서술로",
    "I-2": "'X는 ~다' 직설", "I-3": "'~다'로 종결", "I-4": "당위 문장을 앞으로 옮기기만", "I-5": "주어·동사 구체화",
    "I-6": "동사형으로", "J-1": "대부분 제거", "J-2": "진짜 인용만 남김", "J-3": "쉼표, 괄호, 문장 분리", "J-4": "본문화 또는 삭제",
    "C-2": "산문으로 잇기", "C-3": "제목을 내용 명사로 또는 삭제", "C-10": "단일 명사구로", "C-12": "단문화 또는 연결어미 흡수",
    "E-1": "단문과 장문 섞기, 내용 추가 금지", "E-2": "종결 다양화", "E-3": "문단 길이 섞기", "E-4": "인접 단문을 연결어미로 묶기",
    "E-7": "격식 등급 하나로", "B-1": "첫 등장만 병기", "K-1": "'손꼽히는', '대표적인', 또는 사실로", "K-2": "'~할 수 있다', '~된다'",
    "K-3": "동사를 바로: '회의했다', '분석했다'", "K-4": "실제 하는 일을 동사로", "K-5": "'~을 중심으로', 동사로",
    "K-6": "'~로', '~때문에', 연결어미", "K-7": "지시어 삭제 또는 '이', '그'", "K-8": "삭제 또는 구체 방법", "K-9": "안내조 삭제, 평서로",
    "K-10": "'만약' 삭제", "K-11": "'의' 하나만 남기고 절로", "K-12": "'약'이나 '정도' 하나만", "K-13": "현재형 또는 '~한다'",
    "K-14": "'~하곤 한다', '~해도', 직설", "K-15": "직설", "K-16": "동사로: '~을 이해하다'", "K-17": "'~하게', '~도록' 생략",
    "K-18": "느낌표 삭제", "K-20": "문단 묶기", "A-7a": "'~가 있다', '~를 지닌'이 아닌 서술로",
    "K-21": "마지막 문장을 사실이나 다음 행동으로", "K-22": "목록 하나만 남기고 문장으로 풀기",
    "K-23": "예고 삭제, 바로 본론", "K-24": "실제 조건과 결과를 구체로", "K-25": "제안 문장 삭제",
    "K-26": "직설로", "K-27": "공감 공식 삭제, 바로 내용", "K-28": "삭제하고 결론을 바로", "K-29": "삭제 또는 실제 결과로",
    "K-30": "누가 무엇을 할지 구체로", "K-31": "문장으로 풀기", "C-5": "이모지 삭제", "C-6": "제목 줄이기", "E-5": "쉼표 구간 나누기", "E-7b": "합쇼체나 해요체 하나로",
}
HANGUL = re.compile(r"[가-힣]")
EMOJI = re.compile("[%s-%s%s-%s]" % (chr(0x1F300), chr(0x1FAFF), chr(0x2600), chr(0x27BF)))
NUMBER = re.compile(r"\d[\d,.]*")
QUOTE = re.compile(r"[\"“]([^\"”\n]{2,200})[\"”]")
CONNECTIVE = re.compile(r"(고|며|으며|지만|는데|은데|ㄴ데|면서|어서|아서|해서|니까|으니|므로|도록|려고|자|거나|든지|다가|면|으면|어도|아도|해도)[ ,]")
LAST_LINE = re.compile(r"(지도 모른다|지도 모릅니다|야말로|목적지|첫걸음|출발점|열쇠|시작이다|시작입니다|시작일 것|아닐까|않을까요?\?|기다리고 있을|궁금합니다|충분합니다|충분하다|길이다|길입니다|답이다|답입니다)[.!?]?$")
TEMPLATE_HEADINGS = re.compile(r"^#+\s*(\d+[.)]\s*)?(서론|본론|결론|개요|마무리|맺음말|들어가며|나가며|맺으며|마치며|요약|정리|결론 및 시사점|시사점|소개|장점|단점|문제점|해결 방안|기대 효과)\s*$")


def prose(path_or_text, is_text=False):
    """(lines, [(line_index, text)]) of prose: Markdown structure, code, and tables removed."""
    text = path_or_text if is_text else open(path_or_text, encoding="utf-8-sig").read()
    lines = text.splitlines()
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from tell_scan import prose_lines
    return lines, list(prose_lines(lines))


def paragraphs(rows):
    out, prev = [], None
    for i, t in rows:
        if prev is None or i != prev + 1 or re.match(r"^\s*([-*]|\d+\.)\s", t):
            out.append([])
        out[-1].append((i, t))
        prev = i
    return out


def sentences(rows):
    joined = " ".join(re.sub(r"^\s*([-*]|\d+\.)\s+", "", t).strip() for _, t in rows)
    joined = QUOTE.sub("인용", joined)
    return [s for s in re.split(r"(?<=[.!?。])\s+", joined) if HANGUL.search(s)]


def ending(s):
    s = re.sub(r"[\s\"'”’)\]]+$", "", s).rstrip(".!?。")
    m = re.search(r"([가-힣]{1,2})$", s)
    return m.group(1) if m else ""


def metrics(rows):
    sents = sentences(rows)
    lens = [len(s) for s in sents]
    chars = sum(len(t) for _, t in rows)
    paras = [len(sentences(p)) for p in paragraphs(rows) if not re.match(r"^\s*([-*]|\d+\.)\s", p[0][1])]
    ends = [ending(s) for s in sents]
    run = best = 0
    for a, b in zip(ends, ends[1:]):
        run = run + 1 if a and a == b else 0
        need = 6 if re.search(r"(었다|았다|했다|였다|겼다|렸다|졌다|웠다)$", a) else 4
        if run + 1 >= need:
            best = max(best, run + 1)
    segs = [len(seg.split()) for s in sents for seg in s.split(",") if seg.strip()]
    return {
        "chars": chars, "chars_no_space": sum(len(re.sub(r"\s", "", t)) for _, t in rows),
        "sentences": len(sents),
        "mean_len": round(statistics.mean(lens), 1) if lens else 0,
        "cv_len": round(statistics.pstdev(lens) / statistics.mean(lens), 2) if len(lens) > 1 else 0,
        "long_share": round(sum(l >= 100 for l in lens) / len(lens), 2) if lens else 0,
        "comma_share": round(sum("," in s for s in sents) / len(sents), 2) if sents else 0,
        "complex_share": round(sum(bool(CONNECTIVE.search(s)) for s in sents) / len(sents), 2) if sents else 0,
        "mean_segment_words": round(statistics.mean(segs), 1) if segs else 0,
        "max_same_ending_run": best,
        "last": sents[-1] if sents else "",
        "lists": sum(1 for x in sents if len([g for g in x.split(",") if g.strip()]) >= 4 and all(len(g.strip()) <= 16 for g in x.split(",")[:-1])),
        "polite": sum(bool(re.search(r"(니다|요|죠)[.!?]?$", x)) for x in sents),
        "plain": sum(bool(re.search(r"[다라][.!?]?$", x)) and not re.search(r"니다[.!?]?$", x) for x in sents),
        "para_sizes": paras,
        "endings": dict(sorted(((e, ends.count(e)) for e in set(ends) if e), key=lambda kv: -kv[1])[:6]),
    }


def diagnose(lines, rows, genre="general"):
    found = []
    off = GENRE_OFF.get(genre, set())

    def add(pid, sev, i, what, n=1):
        if pid not in off:
            found.append({"id": pid, "severity": sev, "line": i + 1, "span": what, "count": n, "fix": FIX.get(pid, "")})

    paras = paragraphs(rows)
    chars = sum(len(t) for _, t in rows)
    tail_line = rows[int(len(rows) * 0.7)][0] if rows else 0
    for pid, sev, rx, scope, thr in COMPILED:
        hits = [(i, m.group(0).strip()) for i, t in rows for m in rx.finditer(t)]
        if scope == "each":
            for i, w in hits:
                add(pid, sev, i, w)
        elif scope == "tail":
            for i, w in hits:
                if i >= tail_line:
                    add(pid, sev, i, w)
        elif scope == "para":
            for p in paras:
                ph = [(i, m.group(0).strip()) for i, t in p for m in rx.finditer(t)]
                if len(ph) >= thr:
                    add(pid, sev, ph[0][0], f"{len(ph)} x '{ph[0][1]}' in one paragraph", len(ph))
        elif scope == "density":
            if hits and len(hits) * thr > chars:
                add(pid, sev, hits[0][0], f"{len(hits)} in {chars} characters", len(hits))
        elif len(hits) >= thr:
            sev2 = "S1" if (pid == "C-11" and len(hits) >= 6) or (pid == "C-13" and len(hits) >= 4) else sev
            add(pid, sev2, hits[0][0], f"{len(hits)} x '{hits[0][1]}' in the document", len(hits))

    terms = {}
    for i, t in rows:
        for m in re.finditer(r"([가-힣]+)\(([A-Za-z][A-Za-z .-]{1,40})\)", t):
            terms.setdefault(m.group(2).lower(), []).append(i)
    for term, where in terms.items():
        if len(where) > 1:
            add("B-1", "S2", where[1], f"'{term}' glossed {len(where)} times", len(where))

    run, start = 0, None
    for i, t in rows + [(10 ** 9, "")]:
        if re.match(r"^\s*([-*]|\d+\.)\s", t) and (run == 0 or i == last + 1):
            start = i if run == 0 else start
            run, last = run + 1, i
            continue
        if run >= 4:
            add("C-2", "S3" if genre in ("chat", "report") else "S2", start, f"{run} bullets in a row")
        run = 1 if re.match(r"^\s*([-*]|\d+\.)\s", t) else 0
        start, last = (i, i) if run else (None, None)
    heads = [(k, l) for k, l in enumerate(lines) if re.match(r"^#{1,6}\s", l)]
    for k, l in heads:
        if re.search(r"[을를] 넘어 [^\n]{1,20}?(으로|로)?$|에서 [^\n]{1,15}?(으로|로)$", l):
            add("D-7", "S2", k, f"heading: {l.strip('# ')[:40]}")
    tmpl = [(k, l) for k, l in heads if TEMPLATE_HEADINGS.match(l.strip())]
    if len(tmpl) >= 2:
        add("C-3", "S2", tmpl[0][0], f"{len(tmpl)} template headings ({', '.join(l.strip('# ') for _, l in tmpl[:3])})")
    colon = [(k, l) for k, l in heads if re.search(r"[가-힣A-Za-z]\s*:\s*\S", l)]
    if len(colon) >= 2:
        add("C-10", "S2", colon[0][0], f"{len(colon)} 'X: Y' headings")
    emoji_heads = [k for k, l in heads if EMOJI.search(l)]
    if emoji_heads:
        add("C-5", "S1", emoji_heads[0], f"{len(emoji_heads)} headings with emoji")
    if len(heads) >= 3 and chars and chars / len(heads) < 120:
        add("C-6", "S2", heads[0][0], f"{len(heads)} headings over {chars} characters of prose")

    text = "\n".join(t for _, t in rows)
    if len(re.findall(N + r"하지만", text)) >= 2 and len(re.findall(N + r"그러나", text)) >= 2:
        add("H-2", "S2", rows[0][0], "'하지만' and '그러나' both used repeatedly")
    shall = [p for p in paras if sentences(p) and re.search(r"(해야 한다|해야 합니다|필요가 있다|필요가 있습니다)\.?$", sentences(p)[-1])]
    if len(shall) >= 2:
        add("I-4", "S2", shall[1][0][0], f"{len(shall)} paragraphs end in an obligation")
    labels = [i for i, t in rows if re.match(r"^\s*([-*]\s+)?\*\*[^*]{1,30}\*\*\s*[:：]", t)]
    if len(labels) >= 2:
        add("K-31", "S3" if genre in ("chat", "report") else "S2", labels[0], f"{len(labels)} bold labels with a colon")
    bolds = sum(len(re.findall(r"\*\*[^*]+\*\*", t)) for _, t in rows)
    if bolds >= 3 and bolds * 150 > chars:
        add("J-1", "S2", rows[0][0], f"{bolds} bold spans")
    scare = len(re.findall(r"['‘\"“][가-힣 ]{1,8}['’\"”]", text))
    if scare > 5:
        add("J-2", "S3", rows[0][0], f"{scare} short quoted words")
    parens = len(re.findall(r"\([^)]{1,60}\)", text))
    if parens >= 3 and parens * 100 > chars:
        add("J-4", "S3", rows[0][0], f"{parens} parenthetical asides")

    m = metrics(rows)
    first = rows[0][0] if rows else 0
    if m["sentences"] >= 8 and m["long_share"] < 0.05 and m["cv_len"] < 0.35:
        add("E-1", "S2", first, f"uniform sentence length (cv {m['cv_len']}, no sentence of 100+ characters)")
    if m["max_same_ending_run"]:
        add("E-2", "S2", first, f"{m['max_same_ending_run']} consecutive sentences share one ending")
    sizes = [n for n in m["para_sizes"] if n]
    if len(sizes) >= 4 and all(3 <= n <= 4 for n in sizes):
        add("E-3", "S2", first, f"every paragraph has 3 or 4 sentences ({sizes})")
    if len(sizes) >= 4 and sum(n == 1 for n in sizes) / len(sizes) >= 0.8:
        add("K-20", "S2", first, f"{sum(n == 1 for n in sizes)} of {len(sizes)} paragraphs are one sentence")
    if m["sentences"] >= 8 and m["complex_share"] < 0.15:
        add("E-4", "S2", first, f"only {m['complex_share']:.0%} of sentences join clauses")
    if m["lists"] >= 2:
        add("K-22", "S2", first, f"{m['lists']} sentences built on comma lists of four or more items")
    if m["last"] and LAST_LINE.search(m["last"]):
        add("K-21", "S2", rows[-1][0], f"aphoristic last line: '{m['last'][-30:]}'")
    if m["sentences"] >= 5 and m["mean_segment_words"] > 12:
        add("E-5", "S3", first, f"comma segments average {m['mean_segment_words']} words")
    if m["sentences"] >= 5 and m["comma_share"] > 0.7:
        add("C-12", "S3", first, f"{m['comma_share']:.0%} of sentences contain a comma")
    hapsho = sum(bool(re.search(r"니다[.!?]?$", x)) for x in sentences(rows))
    haeyo = sum(bool(re.search(r"(어요|아요|에요|예요|해요|네요|거든요|죠|래요|대요|군요)[.!?]?$", x)) for x in sentences(rows))
    if hapsho >= 2 and haeyo >= 2:
        add("E-7b", "S2" if genre in ("report", "news", "policy", "legal", "academic") else "S3", first,
            f"합쇼체 {hapsho} and 해요체 {haeyo} sentences mixed")
    if m["polite"] >= 2 and m["plain"] >= 2:
        add("E-7", "S2", first, f"mixed speech levels: {m['polite']} polite, {m['plain']} plain sentences")
    return found, m


def score(found, m):
    weighted = sum(WEIGHT[f["severity"]] for f in found)
    per_k = round(weighted * 1000 / max(m["chars"], 1), 1)
    route = "light" if per_k < 5 else "standard" if per_k < 15 else "heavy"
    return per_k, route


def change_rate(base, revised):
    a, b = base.splitlines(True), revised.splitlines(True)
    same = 0
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            same += sum(map(len, a[i1:i2]))
        elif op == "replace":
            sm = difflib.SequenceMatcher(None, "".join(a[i1:i2]), "".join(b[j1:j2]), autojunk=False)
            same += sum(x.size for x in sm.get_matching_blocks())
    total = max(len(base), len(revised))
    return 0.0 if not total else 1 - same / total


def gate(base_text, rev_text, base_found, rev_found, base_score, rev_score):
    rate = change_rate(base_text, rev_text)
    lost_numbers = sorted(set(NUMBER.findall(base_text)) - set(NUMBER.findall(rev_text)))
    lost_quotes = [q for q in QUOTE.findall(base_text) if q not in rev_text]
    base_ids = {f["id"] for f in base_found}
    introduced = sorted({f["id"] for f in rev_found if f["id"].startswith("D") or f["id"].startswith("K")} - base_ids)
    c8_before = sum(f["count"] for f in base_found if f["id"] == "C-8")
    c8_after = sum(f["count"] for f in rev_found if f["id"] == "C-8")
    s1 = sum(f["severity"] == "S1" for f in rev_found)
    s2 = sum(f["severity"] == "S2" for f in rev_found)
    gain = 1 - rev_score / base_score if base_score else 1.0
    gates = {
        "change_rate": round(rate, 3),
        "change_level": "stop" if rate >= 0.5 else "warn" if rate > 0.3 else "ok",
        "numbers_lost": lost_numbers,
        "quotes_lost": lost_quotes,
        "stock_introduced": introduced,
        "contrast_pairs_wiped": c8_before >= 2 and c8_after == 0,
        "score_gain": round(gain, 2),
    }
    overedit = (gates["change_level"] != "ok") + bool(introduced) + gates["contrast_pairs_wiped"]
    if s1 >= 3 or rate >= 0.5 or lost_numbers or lost_quotes:
        grade = "D"
    elif s1 or overedit >= 2:
        grade = "C"
    elif s2 <= 2 and gain >= 0.7 and not introduced:
        grade = "A"
    elif s2 <= 4 and gain >= 0.5:
        grade = "B"
    else:
        grade = "C"
    gates["grade"] = grade
    return gates


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = sys.argv[1:]
    opts = {}
    for key in ("--base", "--length", "--voice", "--genre"):
        if key in args:
            k = args.index(key)
            if k + 1 >= len(args):
                print(__doc__); sys.exit(2)
            opts[key] = args[k + 1]
            args = args[:k] + args[k + 2:]
    as_json = "--json" in args
    args = [a for a in args if a != "--json"]
    genre = opts.get("--genre", "general")
    if len(args) != 1 or any(a.startswith("--") for a in args) or genre not in GENRES:
        print(__doc__); sys.exit(2)
    for p in [args[0]] + [opts[k] for k in ("--base", "--voice") if k in opts]:
        if not os.path.isfile(p):
            print(f"ERROR {p}: not found"); sys.exit(2)
    try:
        lines, rows = prose(args[0])
        found, m = diagnose(lines, rows, genre)
        per_k, route = score(found, m)
        report = {"file": args[0], "genre": genre, "score_per_1000_chars": per_k, "route": route, "metrics": m, "findings": found}
        failed = any(f["severity"] == "S1" for f in found)
        if "--base" in opts:
            blines, brows = prose(opts["--base"])
            bfound, bm = diagnose(blines, brows, genre)
            bscore, _ = score(bfound, bm)
            report["base_score_per_1000_chars"] = bscore
            report["gates"] = gate("\n".join(blines), "\n".join(lines), bfound, found, bscore, per_k)
            failed = report["gates"]["grade"] in ("C", "D")
        if "--length" in opts:
            target = int(opts["--length"])
            dev = m["chars"] / target - 1 if target else 0
            report["length"] = {"target": target, "chars": m["chars"], "chars_no_space": m["chars_no_space"], "deviation": round(dev, 3), "within_5pct": abs(dev) <= 0.05}
            failed = failed or abs(dev) > 0.05
        if "--voice" in opts:
            _, vrows = prose(opts["--voice"])
            vm = metrics(vrows)
            keys = ("mean_len", "cv_len", "long_share", "comma_share", "complex_share")
            report["voice"] = {k: {"sample": vm[k], "text": m[k]} for k in keys}
            report["voice"]["sample_endings"] = vm["endings"]
            report["voice"]["sample_level"] = "polite" if vm["polite"] > vm["plain"] else "plain"
    except (UnicodeDecodeError, ValueError) as e:
        print(f"ERROR {e}"); sys.exit(2)
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(1 if failed else 0)
    order = {"S1": 0, "S2": 1, "S3": 2}
    for f in sorted(found, key=lambda f: (order[f["severity"]], f["line"])):
        print(f"{f['severity']} {f['id']} {args[0]}:{f['line']}: {f['span']}  -> {f['fix']}")
    print(f"metrics: {m['chars']} chars ({m['chars_no_space']} without spaces), {m['sentences']} sentences, "
          f"mean {m['mean_len']}, cv {m['cv_len']}, comma share {m['comma_share']}, joined clauses {m['complex_share']}, endings {m['endings']}")
    print(f"score: {per_k} per 1000 chars, route {route}, genre {genre}")
    if "gates" in report:
        g = report["gates"]
        print(f"gates: change {g['change_rate']:.0%} ({g['change_level']}), numbers lost {g['numbers_lost'] or 'none'}, "
              f"quotes lost {len(g['quotes_lost'])}, stock introduced {g['stock_introduced'] or 'none'}, "
              f"contrast pairs wiped {g['contrast_pairs_wiped']}, score gain {g['score_gain']:.0%} from {report['base_score_per_1000_chars']}")
        print(f"grade: {g['grade']}")
    if "length" in report:
        L = report["length"]
        print(f"length: {L['chars']} / {L['target']} ({L['deviation']:+.1%}), {L['chars_no_space']} without spaces, "
              f"{'within' if L['within_5pct'] else 'outside'} 5%")
    if "voice" in report:
        v = report["voice"]
        print("voice: " + ", ".join(f"{k} {v[k]['text']} vs sample {v[k]['sample']}" for k in ("mean_len", "cv_len", "long_share", "comma_share", "complex_share"))
              + f"; sample level {v['sample_level']}, endings {v['sample_endings']}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
