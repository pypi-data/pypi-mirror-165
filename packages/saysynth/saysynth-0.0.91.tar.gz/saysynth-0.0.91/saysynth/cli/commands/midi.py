import sys

import click

from saysynth import MidiTrack
from saysynth.cli.options import (
    phoneme_opts,
    segment_opts,
    start_opts,
    adsr_opts,
    say_opts,
    velocity_emphasis_opt,
    volume_range_opt,
    show_volume_opts,
    randomize_velocity_opt,
    prepare_options_for_say,
    group_options
)
from saysynth.lib import say

# # # ##
# Midi #
# # # ##

def run(**kwargs):
    """
    Given a midi file, generate a text-file (or stdout stream) of phonemes with pitch information for input to say
    """

    # generate the text
    text = MidiTrack(**kwargs).to_say_text()

    # handle writing text to file
    output_file = kwargs.get("output_file")
    if output_file:
        with open(output_file, "w") as f:
            f.write(text)


    # if we're not executing say, write text to stdout
    elif not kwargs.get('exec'):
        sys.stdout.write(text)

    else:
        # execute say
        say.run(**prepare_options_for_say(text, **kwargs))


@click.command()
@click.argument("midi_file", required=True)
@click.option(
    "-l",
    "--loops",
    default=1,
    show_default=True,
    type=int,
    help="The number of times to loop the midi file",
)
@start_opts
@phoneme_opts
@group_options(velocity_emphasis_opt, volume_range_opt, randomize_velocity_opt)
@show_volume_opts
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