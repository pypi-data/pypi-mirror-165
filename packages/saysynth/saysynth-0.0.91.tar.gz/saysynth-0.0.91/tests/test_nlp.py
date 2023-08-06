from saysynth.utils import here
from saysynth.lib import nlp
from saysynth.constants import G2P_PHONEMES_TO_SAY_PHONEMES


def test_g2p_phonemes_to_say_phonemes():
    g2p_texts = nlp.word_to_g2p_phonemes("hello world")
    for t in g2p_texts:
        if t.strip():
            assert t in G2P_PHONEMES_TO_SAY_PHONEMES
    say_texts = nlp.word_to_say_phonemes("hello world")
    for t in say_texts:
        if t.strip():
            assert t in set(G2P_PHONEMES_TO_SAY_PHONEMES.values())


def test_word_to_syllable_count():
    word = "hello"
    syllables = nlp.word_to_syllable_count(word)
    assert syllables == 2


def test_process_text_for_say():
    text = "hello world. I am a computer."
    words = nlp.process_text_for_say(text)
    assert words[0][1] == ["h", "AAh", "l", "1OW"]
    assert words[0][2] == "hello"
    assert words[0][0] == 2
    assert words[2][1] == ["%"]
    assert words[2][0] == 1
    assert words[-1][1] == ["%"]
    assert len(words) == 8
