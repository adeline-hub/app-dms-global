def chunk_text(text: str, max_chars: int = 3000):
    chunks = []
    while len(text) > max_chars:
        split = text.rfind("\n", 0, max_chars)
        if split == -1:
            split = max_chars
        chunks.append(text[:split])
        text = text[split:]
    chunks.append(text)
    return chunks