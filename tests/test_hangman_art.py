from unittest import TestCase
from minigames.hangman_art import stage


class Test(TestCase):
    def test_stage_whole_stage(self):
        expected = ['\n  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========\n',
                    '\n  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========\n',
                    '\n  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========\n',
                    '\n  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========',
                    '\n  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========\n',
                    '\n  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========\n',
                    '\n  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========\n',
                    '\n  +---+\n      |\n      |\n      |\n      |\n      |\n=========\n',
                    '\n      +\n      |\n      |\n      |\n      |\n      |\n=========\n']

        actual = stage()
        self.assertEqual(actual, expected)
