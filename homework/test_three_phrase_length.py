# python -m pytest -s test_three_phrase_length.py
def test_phrase_length():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, 'Phrase is longer than 15 symbols ({phrase})'