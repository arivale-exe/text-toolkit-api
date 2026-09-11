#!/usr/bin/env python3
"""Zero-dependency test suite for the canonical Text Toolkit analyzer (server.py).
Run: python3 test.py
Validates summarizing, keyword extraction, HTML-to-text, and schema validation.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from server import summarize, keywords, html_to_text, validate_schema, split_sentences

passed, failed = 0, 0
def check(name, cond, detail=""):
    global passed, failed
    if cond:
        print(f"PASS  {name}"); passed += 1
    else:
        print(f"FAIL  {name} -> {detail}"); failed += 1

sample = ("Autonomous agents need tools. The Text Toolkit provides free text analysis. "
          "It works entirely offline, so your data never leaves your machine. "
          "Summarization and keyword extraction are fast and private.")

s = summarize(sample, 3)
check("summarize returns <= n sentences", len(s) <= 3, f"got {len(s)}")
check("summarize returns non-empty", len(s) >= 1)
check("summary sentences are from source", all(st.strip(" .") in sample for st in s))
check("split_sentences counts", len(split_sentences(sample)) == 4, f"got {len(split_sentences(sample))}")

kw = keywords(sample, 20)
check("keywords is list of dicts", all(isinstance(k, dict) and "term" in k and "count" in k for k in kw))
check("keywords excludes stopwords", not any(k["term"] in ("the","of","to","and") for k in kw))
check("keywords sorted desc", all(kw[i]["count"] >= kw[i+1]["count"] for i in range(len(kw)-1)))

html = "<p>Hello <script>bad()</script>world.</p><div>Second</div>"
txt = html_to_text(html)
check("html_to_text drops script", "bad()" not in txt, repr(txt))
check("html_to_text keeps visible", "Hello" in txt and "world" in txt and "Second" in txt)

errs = validate_schema("hi", {"type": "object"})
check("validate detects type mismatch", len(errs) >= 1, str(errs))
errs2 = validate_schema({"a": 1}, {"type": "object", "required": ["b"]})
check("validate detects missing required", any("missing" in e for e in errs2), str(errs2))
errs3 = validate_schema({"a": 1}, {"type": "object", "properties": {"a": {"type": "number"}}})
check("validate passes clean object", len(errs3) == 0, str(errs3))

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
