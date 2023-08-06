import sys

import click

from midi_utils import note_to_midi
from saysynth import say, Arp

from saysynth.cli.options import (
    say_opts,
    start_opts,
    chord_opts,
    phoneme_opts,
    segment_opts,
    adsr_opts,
    arp_opts,
    duration_opts,
    velocity_emphasis_opt,
    volume_range_opt,
    show_volume_opts,
    randomize_velocity_opt,
    prepare_options_for_say
)
from saysynth.lib import say

def run(**kwargs):
    """
    Given a note name (or midi note number), stream text required to generate a continuous drone for input to say
    """
    kwargs['start_duration'] = kwargs.get('start', 0)
    text = Arp(**kwargs).to_say_text()

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
@arp_opts
@chord_opts
@velocity_emphasis_opt
@volume_range_opt
@randomize_velocity_opt
@show_volume_opts
@start_opts
@duration_opts
@phoneme_opts
@segment_opts
@adsr_opts
@click.option(
    "-o",
    "--output-file",
    type=str,
    help="A filepath to write the generated text to",
)
@say_opts
def cli(**kwargs):
    return run(**kwargs)
