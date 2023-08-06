from random import choice
from slowtype.more_functions import *
from time import sleep


def _random_chars():
    return ''.join([choice('QWERTYUIOPASDFGHJKLZXCVBNM') for x in range(15)])


class SlowtypeExamples:

    def ProgressbarExample():
        """
        
        Progress bar example
        Progress: #_________ [10%]
        
        """

        Progress = 0

        while Progress < 20:
            sleep(.1)
            Progress += 1
            PrintOnLine(f'Progress: ' + '#' * Progress + '_' *
                        (20 - Progress) + ' [' + str(Progress * 5) + '%]')

        ClearLine()
        PrintOnLine('Progress: DONE')

        print('\n')

    def PasswordHackerExample():
        """
        
        Password hacker example
        ABCDEABCDE | INVALID
        
        """

        print('Password hacker\n')

        while True:
            PrintOnLine(_random_chars() + ' | INVALID')
            sleep(.1)