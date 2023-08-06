from typing import Tuple

from .constants import POSSIBLE_NOTES
from .syncopation import weighted_note_to_beat, density
from .conversion import individual_to_melody, encodable
from .compression import encode_lz77, encode_lz78, encode_lzw
from .config import Configuration
from .types import Gene

from itertools import takewhile
from deap import base, creator, algorithms, tools

import random
import logging


def fitness(genes: list[Gene]) -> tuple[float, float]:
    notes = individual_to_melody(genes)
    return abs(weighted_note_to_beat(notes) - 0.35), abs(density(genes) - 0.8)


def fitness_kolmogorov(config, genes: list[Gene]) -> tuple[float]:
    if config.compression_method == 'LZ77':
        compression = lambda x: len(encode_lz77(x))
    elif config.compression_method == 'LZ78':
        compression = lambda x: len(encode_lz78(x))
    elif config.compression_method == 'LZW':
        compression = lambda x: len(encode_lzw(x))
    else:
        raise AttributeError("compression method not found")

    ncd = lambda x, y: max(compression(x + y) - compression(x),
                           compression(y + x) - compression(y)) / max(compression(x), compression(y))

    distances = [ncd(encodable(genes), x) for x in config.match]

    return 1 / sum(distances),


def generator(config=Configuration()):
    prev_gene: Gene | None = None

    def create_random_gene() -> Gene:
        nonlocal prev_gene
        if prev_gene is not None and prev_gene.remaining_ticks > 1:
            prev_gene = Gene(prev_gene.pitch, prev_gene.velocity, prev_gene.remaining_ticks - 1)
            return prev_gene

        tick = min(config.rate)
        duration = int(random.choice(config.rate) / tick)
        key = random.choice(list(config.scale.notes)[30:40])
        velocity = random.randint(80, 100)
        prev_gene = Gene(key, velocity, duration)
        return prev_gene

    return create_random_gene


def mutation(config: Configuration, genes):
    for gene in genes:
        change = random.random()
        if change < config.pitch_change_rate:
            change_2 = random.random()
            gene.pitch = random.choice(config.scale.notes[30:40])
            # if change_2 > config.consonance_rate:
            #     gene.pitch = random.choice(config.scale.notes[30:40])
            # else:
            #     gene.pitch = random.choice(list(set(POSSIBLE_NOTES) - set(config.scale.notes))[30:40])

        change = random.random()
        if change < config.length_change_rate:
            gene.remaining_ticks = 1
    return genes,


def check_remaining_ticks():
    def decorator(func):
        def wrapper(*args, **kwargs):
            offspring = func(*args, **kwargs)
            for genes in offspring:
                for i, gene in enumerate(genes):
                    if gene.remaining_ticks == 1:
                        continue
                    gene.remaining_ticks = len(list(takewhile(lambda x: x.pitch == gene.pitch, genes[i:])))
            return offspring

        return wrapper

    return decorator


def ea_simple_with_elitism(population, toolbox, cxpb, mutpb, ngen, hall_of_fame=None):
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if hall_of_fame is None:
        raise ValueError("halloffame parameter must not be empty!")

    hall_of_fame.update(population)
    hof_size = len(hall_of_fame.items) if hall_of_fame.items else 0

    for gen in range(1, ngen + 1):
        offspring = toolbox.select(population, len(population) - hof_size)
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        offspring.extend(hall_of_fame.items)
        hall_of_fame.update(offspring)
        population[:] = offspring

    return population


def create_config(config=Configuration()) -> base.Toolbox:
    toolbox = base.Toolbox()
    toolbox.register("generator", generator())

    if config.fitness_method == 'kolmogorov':
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.generator, n=32)
        toolbox.register("evaluate", fitness_kolmogorov, config)
    else:
        toolbox.register("individual", tools.initRepeat, creator.KolmogorovIndividual, toolbox.generator, n=32)
        toolbox.register("evaluate", fitness)

    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("select", tools.selStochasticUniversalSampling)
    toolbox.register("mutate", mutation, config)
    toolbox.register("mate", tools.cxOnePoint)

    decorator = check_remaining_ticks()
    toolbox.decorate("mate", decorator)
    toolbox.decorate("mutate", decorator)

    return toolbox


def run_genetic_algorithm(config=Configuration()):
    toolbox = create_config(config)

    population = toolbox.population(100)
    hof = tools.HallOfFame(10)
    population = ea_simple_with_elitism(population, toolbox, cxpb=0.1, mutpb=0.1,
                                        ngen=100, hall_of_fame=hof)
    hof.update(population)
    best = hof.items[0]
    logging.info('-- Best Ever Individual = %s\n', best)
    logging.info('-- Best Ever Fitness -- %s\n', best.fitness.values)

    melody = individual_to_melody(best)
    return melody
