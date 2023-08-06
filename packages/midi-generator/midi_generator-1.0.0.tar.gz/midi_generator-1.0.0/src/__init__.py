import argparse
import logging

from deap import creator, base

from .constants import DEFAULT_RATES
from .types import Scale, match_key, match_mode
from .math import powerset
from .constants import NOTE_DURATIONS
from .config import Configuration
from .parser import parse_config_for_generate
from .commands import generate, mutate, continue_sequence


class CustomParser(argparse.ArgumentDefaultsHelpFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(
            kwargs.get('prog'),
            indent_increment=2,
            max_help_position=100,
            width=None)

    def _format_action(self, action):
        result = super()._format_action(action)
        if isinstance(action, argparse._SubParsersAction):
            # fix indentation on first line
            return "%*s%s" % (self._current_indent, "", result.lstrip())
        return result

    def _format_action_invocation(self, action):
        if isinstance(action, argparse._SubParsersAction):
            # remove metavar and help line
            return ""
        return super()._format_action_invocation(action)

    def _iter_indented_subactions(self, action):
        if isinstance(action, argparse._SubParsersAction):
            try:
                get_subactions = action._get_subactions
            except AttributeError:
                pass
            else:
                # remove indentation
                yield from get_subactions()
        else:
            yield from super()._iter_indented_subactions(action)


def print_cli():
    parser = argparse.ArgumentParser(prog="midi-generator",
                                     description='Command line interface for b2bAI.',
                                     usage='%(prog)s [OPTIONS] COMMAND',
                                     epilog="Run 'midi-generator COMMAND --help' for more information on a command.",
                                     formatter_class=CustomParser)

    parser.add_argument('-l', '--logging-level',
                        choices=[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL],
                        type=int,
                        help='set logging level',
                        default=logging.INFO)

    subparsers = parser.add_subparsers(title='commands', dest='command')

    generate_seq = subparsers.add_parser('generate',
                                         description='Generate a MIDI file from a given configuration.',
                                         help='generate a MIDI file',
                                         usage='%(prog)s [OPTIONS] generate {FILE|OPTIONS}',
                                         formatter_class=CustomParser)

    generate_seq.add_argument('-c', '--config',
                              type=argparse.FileType('r'),
                              help='the configuration file',
                              metavar='File')

    generate_seq.add_argument('--bars',
                              type=int,
                              metavar='{4|8}',
                              help='the number of bars to generate',
                              choices=[4, 8],
                              default=4)

    generate_seq.add_argument('--rates',
                              type=set[float],
                              metavar='set[float]',
                              help='the note lengths used to generate the MIDI file',
                              default=set(DEFAULT_RATES))

    generate_seq.add_argument('--scale',
                              type=str,
                              metavar='Scale',
                              help='the scale in which to generate the MIDI file',
                              default='C minor')

    generate_seq.add_argument('--density',
                              type=float,
                              metavar='float',
                              help='the density of notes in the generated MIDI file',
                              default=0.8)

    generate_seq.add_argument('--syncopation',
                              type=float,
                              metavar='float',
                              help='the level of syncopation in the generated MIDI file',
                              default=0.1)

    mutate_seq = subparsers.add_parser('mutate',
                                       description='Mutate a given MIDI file.',
                                       usage='%(prog)s [OPTIONS] generate FILE [OPTIONS]',
                                       help='mutate a MIDI file.',
                                       formatter_class=CustomParser)

    mutate_seq.add_argument('file',
                            type=str,
                            help='file containing sequence to mutate')

    mutate_seq.add_argument('--probability',
                            type=float,
                            metavar='float',
                            help='the probability of mutating a note',
                            default=0.1)

    continue_seq = subparsers.add_parser('continue',
                                         description='Continue a given MIDI sequence.',
                                         usage='%(prog)s [OPTIONS] generate FILE [OPTIONS]',
                                         help='continue a MIDI sequence.',
                                         formatter_class=CustomParser)

    continue_seq.add_argument('file',
                              type=argparse.FileType('r'),
                              help='file containing sequence to continue')

    args = parser.parse_args()

    logging.basicConfig(level=args.logging_level)
    logging.debug(' arguments given: %s\n', args)

    match args.command:
        case 'generate':
            if args.config is None:
                logging.info(' no configuration file given, using default configuration\n')

                if args.rates not in powerset(NOTE_DURATIONS):
                    logging.warning(' rates not in powerset of note durations, using default rates\n')
                    args.rates = DEFAULT_RATES
                else:
                    args.rates = list(args.rates)

                key = match_key(args.scale.split(' ')[0].lower())
                mode = match_mode(args.scale.split(' ')[1].lower())

                config = Configuration(
                    bars=args.bars,
                    rate=args.rates,
                    scale=Scale(key, mode),
                    density=args.density,
                    syncopation=args.syncopation,
                )
            else:
                logging.info(' using configuration file %s', args.config)
                config = parse_config_for_generate(args.config)
            logging.debug(' configuration: %s\n', config)

            generate(config)

        case 'mutate':
            return mutate(args.file)

        case 'continue':
            return continue_sequence(args.file)


creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0))
creator.create("KolmogorovFitness", base.Fitness, weights=(1.0,))

creator.create("Individual", list, fitness=creator.KolmogorovFitness)
creator.create("KolmogorovIndividual", list, fitness=creator.Fitness)