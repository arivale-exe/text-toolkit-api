#!/usr/bin/env python3
"""Text toolkit module with pure stdlib text processing functions."""
import re, json

def split_sentences(text):
    """Split text into sentences."""
    text = text.strip()
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def word_freq(text):
    """Get word frequency counts."""
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq

def summarize(text, num_sentences=3):
    """Extractive summarization using word frequency scoring."""
    sentences = split_sentences(text)
    if len(sentences) <= num_sentences:
        return sentences
    freq = word_freq(text)
    scored = []
    for sent in sentences:
        words = re.findall(r'\b[a-z]{3,}\b', sent.lower())
        score = sum(freq.get(w, 0) for w in words) / max(len(words), 1)
        scored.append((score, sent))
    scored.sort(reverse=True)
    result = [s for _, s in scored[:num_sentences]]
    result.sort(key=lambda x: sentences.index(x))
    return result

def keywords(text, n=10):
    """Extract top keywords by frequency."""
    freq = word_freq(text)
    ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:n]
    return [{"term": term, "count": count} for term, count in ranked]

def html_to_text(html):
    """Convert HTML to clean text."""
    html = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def validate_schema(instance, schema):
    """Validate a JSON instance against a basic JSON schema."""
    errors = []
    if not isinstance(instance, dict):
        errors.append("Instance must be a dict/object")
        return errors
    if not isinstance(schema, dict):
        errors.append("Schema must be a dict/object")
        return errors
    properties = schema.get("properties", {})
    for prop, prop_schema in properties.items():
        if prop in instance:
            val = instance[prop]
            if "type" in prop_schema:
                expected = prop_schema["type"]
                type_map = {"string": str, "number": (int, float), "boolean": bool, "object": dict, "array": list}
                expected_type = type_map.get(expected)
                if expected_type and not isinstance(val, expected_type):
                    errors.append(f"Property '{prop}': expected {expected}, got {type(val).__name__}")
    return errors

if __name__ == "__main__":
    print(summarize("Hello world. This is a test sentence. Machine learning processes data efficiently."))
    print(keywords("Machine learning algorithms process data efficiently. Machine data processing."))
    print(html_to_text("<p>Hello <b>world</b></p>"))