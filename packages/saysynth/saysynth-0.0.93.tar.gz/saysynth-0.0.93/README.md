# saysynth

Generate music with the say command. Sounds like this:

<iframe width="100%" height="300" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/1231627354&color=%23ffffff&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true"></iframe><div style="font-size: 10px; color: #cccccc;line-break: anywhere;word-break: normal;overflow: hidden;white-space: nowrap;text-overflow: ellipsis; font-family: Interstate,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Garuda,Verdana,Tahoma,sans-serif;font-weight: 100;"><a href="https://soundcloud.com/abelsonlive" title="brian abelson" target="_blank" style="color: #cccccc; text-decoration: none;">brian abelson</a> · <a href="https://soundcloud.com/abelsonlive/saymidi-example" title="saymidi example" target="_blank" style="color: #cccccc; text-decoration: none;">saysynth example</a></div>

## installation

* clone this repo
* create a virtualenv: `python -m venv .venv`
* activate it `source .venv/bin/activate`
* install the lib `pip install -e . `

## usage

### `sy midi`

`sy midi` accepts a midi file and generates pitched phonemes. The midi files must be fully monophonic. In other words there must not be any overlapping notes. Eventually I'll figure out this issue, but for now there is a helpful error message which indicates the name of an overlapping note and the time at which it occurs. You can then use this information to edit your midi file in whatever DAW you use. There is also no support for multi-track midi files, though that will be less challenging to implement.

`sy midi` works by mapping midi notes to their associated frequencies (via my associated library [`midi-utils`](https://gitlab.com/gltd/midi-utils/)) and generating phonemes with pitch contours (as described in [Apple's Speech Synthesis Programming Guide](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/SpeechSynthesisProgrammingGuide/FineTuning/FineTuning.html#//apple_ref/doc/uid/TP40004365-CH5-SW7)).

The syntax for these pitch contours looks something like this:

```
AA {D 120; P 176.9:0 171.4:22 161.7:61}
```

Where `AA` is a [valid phoneme](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/SpeechSynthesisProgrammingGuide/Phonemes/Phonemes.html#//apple_ref/doc/uid/TP40004365-CH9-SW1), `D 120` signifies the duration of the phoneme in milliseconds, and ` P 176.9:0 171.4:22 161.7:61` represents the pitch contour for the phoneme in pairs of frequnect and percentage duration. (For now, `sy midi` only generates flat pitch contours for each phoneme).

Here's a simple example of `sy midi` that pipes its output to the `say command`: (**NOTE**: The only `say` voices which accept pitch contours are `Fred`, `Alex` and `Victoria`)

```shell
sy midi examples/arp.mid --phoneme m | say -v Fred
```

Here, we pass in a midi file and generate a series pitches all with the phoneme `m`. `sy midi` fills in gaps between notes with silence using the `%` phoneme.

You can see the full list of options via `sy midi --help`.

### `sy note`

`sy note` accepts a note name (eg: C3) or midi note number (eg: 69) and generates input to the `say` command which makes a monophonic note.

Example:

```
sy note D#3 -rp Fred:drone | say -v Fred &
```

You can see the full list of options via `sy note --help`.

### `sy chord`

`sy chord` accepts a chord root (eg: C3) or midi note number (eg: 69) and generates multiple `say` commands generating a polyphonic note,

Example:

```
sy chord C1 -c min6 -db 155 -dc 64 -sb 155 -sc 1/2 -at 0.3 -de 0.3 -su 0.9 -re 0.4 -rs phoneme -rp Fred:drone -vr 0.1 0.50 -x
```

You can see the full list of options via `sy chord --help`.

### `sy seq`

`sy seq` accepts a `yaml` filepath specifying multiple `saysynth` commands to be concurrently executed.

The `yaml` file might look something like this:

```yaml
tracks:
  - type: chord
    options:
      root: E3
      chord: min6
      duration_bpm: 80
      duration_count: 128
      segment_bpm: 80
  - type: note
    options:
      start_bpm: 80
      start_count: 2
      root: F#3
      duration_bpm: 80
```

Example:

```
sy seq examples/sequence.yml
```

You can see the full list of options via `sy seq --help`.


## references

- [Docs on advanced say usage](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/SpeechSynthesisProgrammingGuide/FineTuning/FineTuning.html#//apple_ref/doc/uid/TP40004365-CH5-SW3)
- [List of phonemes](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/SpeechSynthesisProgrammingGuide/Phonemes/Phonemes.html#//apple_ref/doc/uid/TP40004365-CH9-SW1)

## todo

- [ ] (6) Add text-to-speech in arp and midi commands
- [ ] (2) Refactor Sequence/controller into a class.
- [ ] (5) controls for intra-phoneme pitch modulation
- [ ] (4) glide or portamento?
- [ ] (3) more unit tests
- [ ] (2) what to log?
- [ ] (2) print out track length and starting point at beginning of sequence
- [ ] (2) Improve soundfont to include all note params
- [ ] (6) Shut down certain channels in sequences
- [ ] (3) Figure out tempfile weirdness with prepare_options_for_say
- [ ] (2) Add stop all command.
- [ ] (2) Add demo command with release.
- [x] (3) Add `render` command to `seq` which writes all tracks (including chords) to files in a directory
- [x] (3) Figure out how to suppress this error: `ImportError: sys.meta_path is None, Python is likely shutting down`
- [x] (4) Figure out why notes drop out (it's because of too many `[[ volm ]]` tags; add an option which removes these )
- [x] (3) Basic text-to-speech via text_to_phonemes
- [x] (3) add individual track launching/config overrides in seq.yml
- [x] (2) add global configs to sequence file.
- [x] (1) add more pitches to midi utils
- [x] (6) word-to-phoneme conversion
- [x] (2) Add syllable counting.
- [x] (4) arpeggiation via `midi-utils` ?
- [x] (1) custom note list for a chord


## ideas
- use pedalboard / guitarboard for realtime audio processing?
  * https://github.com/spotify/pedalboard
  * https://github.com/stefanobazzi/guitarboard
