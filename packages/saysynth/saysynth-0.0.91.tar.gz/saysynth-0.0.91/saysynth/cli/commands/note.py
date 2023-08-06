import sys

import click

from midi_utils import note_to_midi
from saysynth import Note, say
from saysynth.cli.options import (
    say_opts,
    show_volume_per_segment_opt,
    start_opts,
    velocity_opts,
    phoneme_opts,
    segment_opts,
    adsr_opts,
    duration_opts,
    prepare_options_for_say
)
from saysynth.lib import say

def run(**kwargs):
    """
    Given a note name (or midi note number), stream text required to generate a continuous drone for input to say
    """
    text = Note(**kwargs).to_say_text()

    # handle writing text to file
    output_file = kwargs.get("output_file")
    if output_file:
        with open(output_file, "w") as f:
            f.write(text)

    # if we're not executing say, write text to stdout
    elif not kwargs.get('exec', False):
        sys.stdout.write(text)

    else:
        say.run(**prepare_options_for_say(text, **kwargs))

@click.command()
@click.argument("root", type=note_to_midi, default="A2")
@click.option("-tx", "--text", type=str, default=None, help="Text to 'sing', e.g. to use when selecting phonemes.")
@start_opts
@duration_opts
@phoneme_opts
@velocity_opts
@show_volume_per_segment_opt
@adsr_opts
@segment_opts
@click.option(
    "-o",
    "--output-file",
    type=str,
    help="A filepath to write the generated text to",
)
@say_opts
def cli(**kwargs):
    return run(**kwargs)
