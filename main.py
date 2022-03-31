import neat
import pickle
import os
import random

from hilo.game import Game, GameInfo


class HiLoGame:
    MAX_ATTEMPTS = 30

    def __init__(self, v):
        self.game = Game(v)

    def train_ai(self, id, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.genome = genome
        self.genome.fitness = 0

        game_info = GameInfo(0, 0, 0, 0)

        while True:
            output = net.activate((game_info.attempts, game_info.guess, game_info.higher, game_info.lower))
            decision = output.index(max(output))

            # decision is one of our 1-100 outputs, which is the number to guess
            self.game.guess(id, decision)

            game_info = self.game.loop()
            if game_info.correct or game_info.attempts >= self.MAX_ATTEMPTS:
                # print("ID: %d  AT: %d  C: %d" % (id, game_info.attempts, game_info.correct))
                self.genome.fitness = self.MAX_ATTEMPTS - game_info.attempts
                break

        return False


def eval_genomes(genomes, config):
    v = random.randint(1, 100)

    for i, (genome_id, genome) in enumerate(genomes):
        hilo = HiLoGame(v)
        force_quit = hilo.train_ai(genome_id, genome, config)
        if force_quit:
            quit()


def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())
    p.add_reporter(neat.Checkpointer(10))

    winner = p.run(eval_genomes)
    with open('winner.pickle', 'wb') as f:
        pickle.dump(winner, f)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    run_neat(config)
    #test_best_network(config)