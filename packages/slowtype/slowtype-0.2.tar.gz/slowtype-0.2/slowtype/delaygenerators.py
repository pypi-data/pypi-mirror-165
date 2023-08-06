class DelayGenerators:

    def Faster(CharacterIndex, TypeTextLength, Divide: float = 1):
        """
        
        Returns: (TypeTextLength-CharacterIndex)/Divide

        In args: float

        """
        return (TypeTextLength - CharacterIndex) / Divide

    def Slower(CharacterIndex, TypeTextLength, Divide: float = 1):
        """
        
        Returns: -(CharacterIndex-TypeTextLength)/Divide

        In args: float

        """
        return (CharacterIndex) / Divide

    def PrintSleep(CharacterIndex, TypeTextLength, Args):
        """

        In args: (DivMod, Sleep)
        Print DivMod characters and sleeps Sleep seconds

        """
        DivMod = Args[0]
        Sleep = Args[1]

        CharacterIndex += 1

        if CharacterIndex % DivMod != 0:
            return 0
        else:
            return Sleep