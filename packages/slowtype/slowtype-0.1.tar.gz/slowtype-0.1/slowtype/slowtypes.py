from time import sleep
from random import uniform


class SlowTypes:

    def SlowType(TypeText: str,
                 NextCharDelay: float = 0.1,
                 UseInput: bool = False,
                 NewLineAfterEnd: bool = True):
        """
        
        Standard SlowType, delay has attribute NextCharDelay
        
        """

        for TypeChar in TypeText:
            print(TypeChar, end='', flush=True)
            sleep(NextCharDelay)

        if UseInput:
            return input()

        if NewLineAfterEnd:
            print()

    def SlowType_DelayRandom(TypeText: str,
                             NextCharDelayMin: float = 0.1,
                             NextCharDelayMax: float = 0.2,
                             UseInput: bool = False,
                             NewLineAfterEnd: bool = True):
        """
        
        Random delay (from NextCharDelayMin to NextCharDelayMax)
        
        Alternative:
        SlowTypes.SlowType_UsingDelayGenerator(..., lambda x, y: random.uniform(0.1, 0.2))

        """

        for TypeChar in TypeText:
            print(TypeChar, end='', flush=True)
            sleep(uniform(NextCharDelayMin, NextCharDelayMax))

        if UseInput:
            return input()

        if NewLineAfterEnd:
            print()

    def SlowType_UsingDelayGenerator(TypeText: str,
                                     DelayGenerator,
                                     DelayGeneratorArgs: any = None,
                                     UseInput: bool = False,
                                     NewLineAfterEnd: bool = True):
        """
        
        DelayGenerator: Function
        Attributes:
            CharacterIndex: attribute #0, index of character (first character has index 0)
            len TypeText: attribute #1, length of type text

        Example of DelayGenerator:

        / ------------------------------ /

        def GenerateDelay(CharacterIndex, TypeTextLength, OtherArgs):
            return CharacterIndex / 10 # delay: index/10 secs

        SlowTypes.SlowType_UsingDelayGenerator(..., GenerateDelay, (1, 2, 3), False)

        / ------------------------------ /

        And acceps args for delay generator function (any object as arg, ex: {"Speed": 1, ...})
            
        Delay returned by DelayGenerator function
        
        """

        CharacterIndex = 0
        for TypeChar in TypeText:
            print(TypeChar, end='', flush=True)

            if DelayGeneratorArgs:
                sleep(
                    DelayGenerator(CharacterIndex, len(TypeText),
                                   DelayGeneratorArgs))
            else:
                sleep(DelayGenerator(CharacterIndex, len(TypeText)))

            CharacterIndex += 1

        if UseInput:
            return input()

        if NewLineAfterEnd:
            print()