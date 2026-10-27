---
description: robust frontmatter text is not prose
---
# Edge cases

The parser returns `List<int>` and Rust uses Vec<String> for the buffer.
Latency stays a < b > c in the worst case, with throughput > 5 per core.
See <https://example.com/spec> or mail <alice@example.com>.
<section>Plain block</section>

    leverage <indented code is skipped>

<!--
leverage inside a multi-line comment
-->

```text
~~~
leverage inside a fence that contains a tilde line
~~~
```

The cache cut p95 latency from 41 ms to 12 ms, significantly faster at 3.4x.
