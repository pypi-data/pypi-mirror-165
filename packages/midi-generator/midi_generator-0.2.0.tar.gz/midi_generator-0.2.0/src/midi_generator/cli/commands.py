import logging
from midi_generator.utils.output import write_file
from note import Note
from ..config import Configuration
from deap import base, creator, tools
from ..genetic import ea_simple_with_elitism, generator, fitness, mutation, check_remaining_ticks, individual_to_melody
from ..config import Configuration
import numpy as np


def generate(config: Configuration) -> list[Note]:
    toolbox = base.Toolbox()
    gene_generator = generator(config)
    toolbox.register("Note", gene_generator)
    creator.create("FitnessComposed", base.Fitness, weights=(-1.0, -1.0))
    creator.create("Individual", list, fitness=creator.FitnessComposed)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.Note, n=32)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", fitness)
    toolbox.register("select", tools.selStochasticUniversalSampling)
    toolbox.register("mutate", mutation, config)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("select", tools.selTournament, tournsize=3)
    decorator = check_remaining_ticks()
    toolbox.decorate("mate", decorator)
    toolbox.decorate("mutate", decorator)
    population = toolbox.population(100)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)
    stats.register("min_axis", np.min, axis=0)
    stats.register("avg_axis", np.mean, axis=0)

    hof = tools.HallOfFame(10)
    population, logbook = ea_simple_with_elitism(population, toolbox, cxpb=0.4, mutpb=0.2,
                                                 ngen=100, stats=stats, hall_of_fame=hof)

    hof.update(population)
    best = hof.items[0]
    logging.info('-- Best Ever Individual = %s\n', best)
    logging.info('-- Best Ever Fitness -- %s\n', best.fitness.values)
    
    melody = individual_to_melody(best)
    write_file(melody, "best")
    return melody


def mutate(sequence: list[Note]) -> list[Note]:
    pass

def continue_sequence(sequence: list[Note]) -> list[Note]:
    pass