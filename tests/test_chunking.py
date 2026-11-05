from app.chunking import split_into_chunks, MAX_CHUNK_CHARS


def test_empty_text_returns_no_chunks():
    assert split_into_chunks("") == []
    assert split_into_chunks("   \n\n  ") == []


def test_short_text_is_single_chunk():
    text = "Python developer with Flask experience"
    assert split_into_chunks(text) == [text]


def test_bullet_markers_are_stripped():
    chunks = split_into_chunks("• Built REST APIs\n- Wrote unit tests")
    assert chunks == ["Built REST APIs Wrote unit tests"]


def test_many_lines_are_packed_within_max_length():
    text = "\n".join(
        f"Line number {i} describing some experience with backend development."
        for i in range(50)
    )
    chunks = split_into_chunks(text)

    assert len(chunks) > 1
    assert all(len(chunk) <= MAX_CHUNK_CHARS for chunk in chunks)


def test_long_line_is_split_on_sentences():
    sentence = "This sentence describes one responsibility of the role."
    text = " ".join([sentence] * 20)

    chunks = split_into_chunks(text)

    assert len(chunks) > 1
    assert all(len(chunk) <= MAX_CHUNK_CHARS for chunk in chunks)


def test_long_text_without_punctuation_is_split_by_words():
    text = " ".join(["word"] * 200)

    chunks = split_into_chunks(text)

    assert len(chunks) > 1
    assert all(len(chunk) <= MAX_CHUNK_CHARS for chunk in chunks)


def test_no_text_is_lost():
    text = "First line about Python.\nSecond line about Flask.\nThird line about SQL."
    joined = " ".join(split_into_chunks(text))

    for word in ["Python", "Flask", "SQL"]:
        assert word in joined