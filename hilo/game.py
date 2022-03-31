import random

class GameInfo:
    def __init__(self, higher, lower, attempts, guess):
        self.correct = higher == 0 and lower == 0
        self.incorrect = higher != 0 or lower != 0
        self.attempts = attempts
        self.higher = lower
        self.lower = higher
        self.guess = guess

class Game:
    def __init__(self, v):
        self.value = v
        self.attempts = 0
        self.userguess = None

    def guess(self, id, i):
        self.userguess = i
#        print("(%d) Guessing %d (for %d)" % (id, self.userguess, self.value))
        if i == self.value:
            print("Guessed after %d attempts" % (self.attempts))

    def loop(self):
        self.attempts += 1
        return GameInfo(self.value > self.userguess, self.value < self.userguess, self.attempts, self.userguess)