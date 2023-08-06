import random
import copy
import math
from typing import Optional, List, Union, Tuple, Dict, Any

from midi_utils import (
    midi_arp,
    midi_to_freq,
    note_to_midi,
    midi_chord,
    midi_to_note,
    ADSR,
)

from .lib import midi, say, nlp
from .cli.options import prepare_options_for_say
from .utils import bpm_to_time, frange, rescale
from .constants import (
    SAY_PHONEME_SILENCE,
    SAY_SEGMENT_MAX_DURATION,
    SAY_SEGMENT_SILENCE_DURATION,
    SAY_EMPHASIS,
    SAY_PHONEME_CLASSES,
    SAY_ALL_PHONEMES,
    SAY_TUNE_TAG,
    SAY_TUNED_VOICES,
    SAY_PHONEME_VOICE_CLASSES,
    SAY_VOLUME_RANGE,
)


class Word(object):
    def __init__(self, *args):
        self.text = args[2]
        self.syllables = args[0]
        self.phonemes = args[1]
        self.n_phonemes = len(self.phonemes)
        self.max_phonemes_per_syllable = math.floor(self.n_phonemes / self.syllables)


class Lyrics(object):
    # A lyric object is initialized from a text and containes info about the words in a song
    def __init__(self, text):
        self.text = text
        self.words = [Word(*word) for word in nlp.process_text_for_say(text)]

        self.n_words = len(self.words)
        self.n_syllables = sum([word.syllables for word in self.words])
        self.phonemes = [p for word in self.words for p in word.phonemes]
        self.n_phonemes = len(self.phonemes)

    def get_phoneme_for_segment(self, index):
        seg_index = index % self.n_phonemes
        phon = self.phonemes[seg_index]
        return phon


class Segment(object):
    # a segment represents an individaul part-of-speech (phoneme) in say
    # a segment can have a duration, a rate, and a sequences of pitches
    # its final state is a string for input to say
    # TODO: move randomization out of here and into the note class
    #
    def __init__(
        self,
        note: Union[int, str],
        velocity: int = 127,
        phoneme: str = "m",
        duration: Union[float, int] = SAY_SEGMENT_MAX_DURATION,
        type: str = "note",
        emphasis: Tuple[int, int] = SAY_EMPHASIS,
        volume_range: Tuple[float, float] = SAY_VOLUME_RANGE,
        show_volume: bool = True,
        duration_sig_digits: int = 4,
        **kwargs,
    ):
        self._phoneme = phoneme
        self._duration = duration
        self._emphasis = emphasis
        self.velocity = velocity
        self.note = note
        self.is_silence = type == "silence"
        self.volume_range = volume_range
        self.show_volume = show_volume
        self.duration_sig_digits = duration_sig_digits

    @property
    def phoneme(self):
        return self._phoneme

    @property
    def phoneme_has_emphasis(self):
        if (
            self._phoneme.startswith("0")
            or self._phoneme.startswith("1")
            or self._phoneme.startswith("2")
        ):
            return True
        return False

    @property
    def frequency_envelope(self):
        # lookup frequency
        freq = midi_to_freq(note_to_midi(self.note))
        return f"P {freq}:0"

    @property
    def duration(self):
        """
        calculate phoneme duration or pass it through
        """
        return round(
            min(self._duration, SAY_SEGMENT_MAX_DURATION), self.duration_sig_digits
        )

    @property
    def volume(self) -> str:
        """
        Translate a midi velocity value (0-127) into a pair of say volume tags, eg: "[[ volm +0.1 ]]"
        """
        if self.show_volume:
            volm = rescale(self.velocity, [0, 127], self.volume_range)
            return f"[[ volm {volm} ]]"
        return ""

    @property
    def emphasis(self) -> str:
        """
        Translate a midi velocity value (0-127) into a phoneme emphasis value ("", "1", or "2")
        when provided with a tuple of steps (step_1, step_2) eg: (75, 100)
        Don't perform this action when the phoneme already has an emphasis included.
        """
        if not self.phoneme_has_emphasis:
            if not self.velocity:
                return ""
            if self.velocity > self._emphasis[1]:
                return "2"
            if self.velocity > self._emphasis[0]:
                return "1"
        return ""

    def to_text(self):
        """ "
        Format phoneme text.
        TODO: Handle intra-note modulation?
        """
        if self.is_silence:
            return f"{SAY_PHONEME_SILENCE} {{D {self.duration}}}"
        return f"{self.volume} {self.emphasis}{self.phoneme} {{D {self.duration}; {self.frequency_envelope}}}"

    def __eq__(self, other):
        return str(self) == str(other)


class Note(object):
    def __init__(
        self,
        note: Union[int, str] = "A3",
        phoneme: str = "m",
        text: Optional[str] = None,
        # start position
        start: Optional[int] = 0,
        start_bpm: Optional[Union[float, int]] = 120,
        start_count: Union[str, float, int] = 0,
        start_time_sig: str = "4/4",
        # envelope
        velocity: int = 127,
        show_volume_per_segment: int = 3,
        show_volume: bool = True,
        attack: Union[float, int] = 0,
        decay: Union[float, int] = 0,
        sustain: Union[float, int] = 1,
        release: Union[float, int] = 0,
        # length
        duration: Optional[Union[float, int]] = None,
        duration_bpm: Optional[Union[float, int]] = 120,
        duration_count: Union[str, float, int] = 1,
        duration_time_sig: str = "4/4",
        # segmentation
        segment_duration: Optional[int] = None,
        segment_bpm: Optional[float] = 120,
        segment_count: Optional[Union[str, float, int]] = 1.0 / 8.0,
        segment_time_sig: Optional[str] = "4/4",
        # randomization
        randomize_phoneme: Optional[str] = None,
        randomize_velocity: Optional[Tuple[int, int]] = None,
        randomize_octave: Optional[List[int]] = [],
        randomize_segments: Optional[List[str]] = [],
        randomize_start: Optional[Tuple[int, int]] = None,
        **segment_options,
    ):
        """
        Generate say text for a collection of phonemes with adsr + pitch modulation
        """

        self.segment_options = segment_options
        root = segment_options.pop("root", None)

        if root or note:
            self.note = note_to_midi(root or note)  # root == note
            self.name = midi_to_note(self.note)
        else:
            self.note = 0
            self.name = "silence"

        # phoneme
        self.phoneme = phoneme

        # text / lyrics
        self.lyrics = None
        if text:
            self.lyrics = Lyrics(text)

        # start position
        self.start = start
        if not self.start:
            self.start = bpm_to_time(start_bpm, start_count, start_time_sig)
        if randomize_start:
            self.start = random.choice(
                range(self.randomize_start[0], self.randomize_start[1] + 1)
            )

        # duration
        self.duration = duration
        if not self.duration:
            self.duration = bpm_to_time(duration_bpm, duration_count, duration_time_sig)

        # velocity
        self.velocity = velocity
        self.show_volume_per_segment = show_volume_per_segment
        self.show_volume = show_volume

        # segmentation
        self.segment_duration = segment_duration
        if not self.segment_duration:
            self.segment_duration = bpm_to_time(
                segment_bpm, segment_count, segment_time_sig
            )
        self.segment_duration = min(SAY_SEGMENT_MAX_DURATION, self.segment_duration)
        self.segment_count = int(self.duration / self.segment_duration) + 1
        self._segments = []

        # adsr
        self.adsr = ADSR(attack, decay, sustain, release, samples=self.segment_count)

        # randomization
        self.randomize_phoneme = randomize_phoneme
        self.randomize_velocity = randomize_velocity
        self.randomize_octave = randomize_octave
        self.randomize_segments = randomize_segments
        self.randomize_start = randomize_start

    def _get_phoneme(self, index):
        # handle phoneme randomization
        if self.randomize_phoneme:
            if self.randomize_phoneme == "all":
                return random.choice(SAY_ALL_PHONEMES)
            elif ":" in self.randomize_phoneme:
                voice, style = self.randomize_phoneme.split(":")
                voice = voice.title()  # allow for lowercase
                try:
                    return random.choice(SAY_PHONEME_VOICE_CLASSES[voice][style])
                except KeyError:
                    raise ValueError(
                        f"Invalid `voice` '{voice}' or `style` '{style}'. "
                        f"`voice` must be one of: {', '.join(SAY_TUNED_VOICES)}. "
                        f"`style` must be one of: {', '.join(SAY_PHONEME_CLASSES)}"
                    )
            else:
                return random.choice(
                    [c.strip() for c in self.randomize_phoneme.split(",")]
                )

        # handle lyrics
        if self.lyrics:
            return self.lyrics.get_phoneme_for_segment(index)

        return self.phoneme

    def _get_note(self):
        if self.randomize_octave:
            return (random.choice(self.randomize_octave) * 12) + note_to_midi(self.note)
        return self.note

    def _get_velocity(self):
        if self.randomize_velocity:
            return random.choice(
                range(self.randomize_velocity[0], self.randomize_velocity[1] + 1)
            )
        return self.velocity

    def _get_segment_kwargs(self, **kwargs):
        opts = copy.copy(self.segment_options)
        opts.update(kwargs)
        return opts

    def _get_segment(
        self,
        index=0,
        note=None,
        velocity=0,
        duration=None,
        **kwargs,
    ):
        # optionally randomize every segment.
        if "note" in self.randomize_segments and self.randomize_velocity:
            note = self._get_note()
        if "velocity" in self.randomize_segments and self.randomize_velocity:
            velocity = self._get_velocity()

        return Segment(
            note=note,
            velocity=velocity * self.adsr.get_value(index),
            phoneme=self._get_phoneme(index),
            duration=duration or self.segment_duration,
            show_volume=self.show_volume and index % self.show_volume_per_segment == 0,
            **self._get_segment_kwargs(**kwargs),
        )

    @property
    def segments(self):

        # cache segments
        if len(self._segments) > 0:
            return self._segments

        # get initial value of note + velocity + phoneme
        note = self._get_note()
        velocity = self._get_velocity()

        if self.start and self.start > 0:
            # create multiple silent phonemes which add up to the desired start position
            start_breaks = list(
                frange(0.0, self.start, SAY_SEGMENT_SILENCE_DURATION, 10)
            )
            for index, total_start_time in enumerate(start_breaks[1:]):
                segment = self._get_segment(index, type="silence", velocity=0)
                self._segments.append(segment)

            if total_start_time < self.start:
                # add final step of silence
                self._segments.append(
                    self._get_segment(index + 1, type="silence", velocity=0)
                )

        # create multiple phonemes which add up to the phoneme_duration
        segment_breaks = list(frange(0.0, self.duration, self.segment_duration, 10))
        total_time = 0
        index = 0
        for index, total_time in enumerate(segment_breaks[1:]):
            segment = self._get_segment(
                index,
                note,
                velocity,
                type=self.segment_options.get("type", "note"),
            )
            self._segments.append(segment)

        if total_time < self.duration and len(self._segments) < self.segment_count:

            # add final step
            self._segments.append(
                self._get_segment(
                    index + 1,
                    note,
                    velocity,
                    duration=self.duration - total_time,
                    type=self.segment_options.get("type", "note"),
                )
            )
        return self._segments

    def to_text(self):
        return "\n".join([s.to_text() for s in self.segments])

    def to_say_text(self):
        return SAY_TUNE_TAG + "\n" + self.to_text()

    def __eq__(self, other):
        return self.to_text() == other.to_text()


class Chord(object):
    _notes = []

    def __init__(self, **kwargs):
        og_note = kwargs.pop("note", "A1")
        self.root = kwargs.pop("root", og_note)  # root == note
        self.root_midi = note_to_midi(self.root)
        self.note_options = kwargs
        # check for arbitrary notes
        notes = kwargs.pop("chord_notes", [])
        if len(notes):
            self.midi_notes = [self.root_midi + n for n in notes]

        # otherwise use chord
        else:
            self.midi_notes = midi_chord(root=self.root, **self.note_options)

    def get_kwargs(self, **kwargs):
        """
        get kwargs + update with new ones
        used for mapping similar kwards over different notes
        """
        d = dict(self.note_options.items())
        d.update(kwargs)
        return d

    @property
    def notes(self):
        if not len(self._notes):
            for n in self.midi_notes:
                self._notes.append(Note(**self.get_kwargs(note=n)))
        return self._notes

    def write(self, output_file):
        for note in self.notes:
            fn = ".".join(output_file.split(".")[:-1])
            ext = "txt" if "." not in output_file else output_file.split(".")[-1]
            note_output_file = f"{fn}-{note.note}.{ext}"
            with open(note_output_file, "w") as f:
                f.write(str(note))

    def play(self):
        # generate a command for each note in the chord
        commands = []
        for note in self.notes:
            cmd_kwargs = prepare_options_for_say(
                input_text=note.to_say_text(),
                **self.get_kwargs(note=note.note, type="note"),
            )
            audio_output_file = cmd_kwargs.get("audio_output_file", None)
            if audio_output_file:
                fn = ".".join(audio_output_file.split(".")[:-1])
                ext = (
                    "aiff"
                    if "." not in audio_output_file
                    else audio_output_file.split(".")[-1]
                )
                cmd_kwargs["audio_output_file"] = f"{fn}-{note.name}.{ext}"
            commands.append(cmd_kwargs)
        say.spawn(commands)


class Arp(object):
    _notes = []

    def __init__(
        self,
        text: Optional[str] = None,  # text to 'sing'
        notes: List[int] = [],  # arbitrary list of notes to arpeggiate
        root: str = "A3",  # root note of chord
        chord: str = "min6_9",  # chord name,
        inversions: List[int] = [],  # inversions list
        stack: int = 0,  # stack a chord up or down
        styles: List[str] = ["down"],
        octaves: List[int] = [0],  # a list of octaves to add to the notes (eg: [-1, 2])
        velocities: List[int] = [100],
        # a list of velocities to apply across notes,
        # velocities are retrieved using a modulo so
        # this can be any duration and will be applied
        # in order
        show_volume_per_note: int = 3,
        beat_bpm: float = 131.0,  # bpm to use when determining beat length
        beat_count: Union[float, int, str] = "1/16",  # count of one beat of the arp
        beat_time_sig: str = "4/4",  # time signature of arp
        beat_duration: Optional[float] = None,  # the time of the note in ms
        note_bpm: float = 131.0,  # bpm to use when determining note duration
        note_count: Union[
            float, int, str
        ] = "3/64",  # count of note legth (should be less than or equat to beat count)
        note_time_sig: str = "4/4",  # time signature of arp
        note_duration: Optional[float] = None,  # arbitrary duration of note in ms
        randomize_start: Optional[List[int]] = None,
        start_bpm: float = 131.0,  # bpm to use when determining the start of the arp and adds silence at the beginning
        start_count: Union[float, int, str] = 0,  # the start beat count
        start_time_sig: str = "4/4",  # time signature to use when determining start
        start_duration: Optional[
            float
        ] = None,  # the amount of silence to add at the beginning in ms
        duration_bpm: float = 131.0,  # bpm to use when determining note duration
        duration_count: Union[float, int, str] = "16",  # the duration beat count
        duration_time_sig: str = "4/4",  # time signature to use when determining duration
        duration: Optional[float] = None,  # the total duration of the pattern in ms
        loops: Optional[int] = None,
        **note_options,
    ):
        self.styles = styles

        if randomize_start:
            start_duration = random.choice(
                range(randomize_start[0], randomize_start[1] + 1)
            )

        self.sequence = midi_arp(
            notes=notes,
            root=root,
            chord=chord,
            inversions=inversions,
            stack=stack,
            octaves=octaves,
            styles=styles,
            velocities=velocities,
            beat_bpm=beat_bpm,
            beat_count=beat_count,
            beat_time_sig=beat_time_sig,
            beat_duration=beat_duration,
            note_bpm=note_bpm,
            note_count=note_count,
            note_time_sig=note_time_sig,
            note_duration=note_duration,
            start_bpm=start_bpm,
            start_count=start_count,
            start_time_sig=start_time_sig,
            start_duration=start_duration,
            duration_bpm=duration_bpm,
            duration_count=duration_count,
            duration_time_sig=duration_time_sig,
            duration=duration,
            loops=loops,
        )
        self.show_volume_per_note = show_volume_per_note
        self.note_options = note_options

    def get_kwargs(self, index, **kwargs):
        """
        get kwargs + update with new ones
        used for mapping similar kwards over different notes
        """
        d = dict(self.note_options.items())
        d.update(kwargs)
        d["show_volume"] = index % self.show_volume_per_note == 0
        return d

    @property
    def notes(self):
        if not len(self._notes):
            for i, note in enumerate(self.sequence):
                kwargs = self.get_kwargs(i, **note)
                self._notes.append(Note(**kwargs))
        return self._notes

    def to_text(self):
        return "\n".join([n.to_text() for n in self.notes])

    def to_say_text(self):
        return SAY_TUNE_TAG + "\n" + self.to_text()

    def __repr__(self):
        return f"<Arp {','.join(self.styles)}"


class MidiTrack(object):
    def __init__(
        self,
        midi_file: str,
        loops: int = 1,
        # start position
        start: Optional[int] = None,
        start_bpm: Optional[Union[float, int]] = 120,
        start_count: Union[str, float, int] = 0,
        start_time_sig: str = "4/4",
        **kwargs,
    ):
        """
        TODO: multichannel midi
        """
        self.midi_file = midi_file
        self.loops = loops

        self.start = start
        if not self.start:
            self.start = bpm_to_time(start_bpm, start_count, start_time_sig)
        self.start_segment_count = int(self.start / SAY_SEGMENT_SILENCE_DURATION) + 1
        self.kwargs = kwargs
        self._notes = []
        self._start_segments = []

    @property
    def notes(self):
        if len(self._notes):
            return self._notes
        for _ in range(0, self.loops):
            for note in midi.process(self.midi_file):
                self.kwargs.update(note)
                self._notes.append(Note(**self.kwargs))
        return self._notes

    def _get_start_text(self):
        if not self.start:
            return ""

        # create multiple silent segments which add up to the start position
        if not len(self._start_segments):
            for _, total_time in enumerate(
                list(frange(0.0, self.start, SAY_SEGMENT_SILENCE_DURATION, 10))[1:]
            ):
                self._start_segments.append(
                    Segment(
                        type="silence",
                        velocity=0,
                        duration=SAY_SEGMENT_SILENCE_DURATION,
                    )
                )

            if (
                total_time < self.start
                and len(self._start_segments) < self.start_segment_count
            ):
                # add final silent step
                self._start_segments.append(
                    Segment(
                        type="silence", velocity=0, duration=self.start - total_time
                    )
                )
        return "\n".join(self._start_segments)

    def to_text(self):
        return self._get_start_text() + "\n" + "\n".join(map(str, self.notes))

    def to_say_text(self):
        return SAY_TUNE_TAG + "\n" + self.to_text()

    def __repr__(self):
        return f"<MidiTrack {self.midi_file}>"
