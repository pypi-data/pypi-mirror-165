import copy

import click

from midi_utils import note_to_midi
from saysynth import Chord
from saysynth.cli.options import (
    say_opts,
    velocity_opts,
    show_volume_opts,
    phoneme_opts,
    segment_opts,
    chord_opts,
    adsr_opts,
    duration_opts,
    start_opts
)

# # # # #
# Chord #
# # # # #

def run(**kwargs):
    """
    Given a note name (or midi note number), stream text required to generate a continuous drone for input to say
    """
    # generate chord
    chord = Chord(**kwargs)
    # handle writing text to multiple files
    output_file = kwargs.pop("output_file", None)
    if output_file:
        chord.write(output_file)
    else:
        chord.play()


@click.command()
@click.argument("root", type=note_to_midi, default="A2")
@click.option("-tx", "--text", type=str, default=None, help="Text to 'sing', e.g. to use when selecting phonemes.")
@chord_opts
@start_opts
@duration_opts
@velocity_opts
@show_volume_opts
@adsr_opts
@phoneme_opts
@segment_opts
@click.option(
    "-o",
    "--output-file",
    type=str,
    help="A filepath to write the generated text to. This filepath will be used as a pattern to generate multiple text files, one per note in the chord.",
)
@say_opts
def cli(**kwargs):
    return run(**kwargs)