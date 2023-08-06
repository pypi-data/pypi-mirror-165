from saysynth import Segment, Note, MidiTrack, Lyrics, Word


def test_segment():
    segment = Segment(note="A3", velocity=127, duration=100)
    assert segment.to_text() == "[[ volm 1.0 ]] 2m {D 100; P 440:0}"


def test_note():
    note = Note(
        note="C4",
        phoneme="m",
        velocity=127,
        attack=0.1,
        decay=0.2,
        sustain=0.3,
        release=0.5,
        bpm=126,
        count=1 / 2,
        segment_bpm=126,
        volume_range=[0.1, 0.5],
        segment_count=1 / 32,
    )
    assert note.segments[0].to_text() == "[[ volm 0.1 ]] m {D 59.5238; P 523.25:0}"
    assert note.segments[-1].to_text() == "[[ volm 0.108 ]] m {D 35.7143; P 523.25:0}"


def test_lyrics():
    lyrics = Lyrics("hello world")
    assert len(lyrics.words) == 2
    assert [isinstance(word, Word) for word in lyrics.words]
