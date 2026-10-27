"""Test helper: append a locator line to the first work record's Locators field."""
import sys

path, loc, what = sys.argv[1:4]
text = open(path, encoding="utf-8").read()
marker = "- **Locators:**\n"
i = text.index(marker) + len(marker)
open(path, "w", encoding="utf-8").write(text[:i] + f"  - `{loc}` — {what}\n" + text[i:])
