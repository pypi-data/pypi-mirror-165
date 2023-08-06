from slowtype.more_functions import PrintOnLine


class ProgressBar:

    def __init__(self,
                 Min,
                 Max,
                 Pattern='Progress: ?pbar? [?value?% / ?max? $ ?min?]',
                 CharOnDone='#',
                 CharOnNotDone='_',
                 LineLength=20):
        self.Min = Min
        self.Max = Max
        self.CharOnDone = CharOnDone
        self.CharOnNotDone = CharOnNotDone
        self.LineLength = LineLength
        self.Pattern = Pattern

        if Min > Max:
            raise ValueError('Maximal value must be bigger than minimal.')

        if Min == Max:
            raise ValueError('Maximal valie cannot be equals minimal.')

        if Min < 0:
            raise ValueError('Minimal value must be bigger than 0 or equals.')

        if Max < 0:
            raise ValueError('Maximal value must be bigger than 0 or equals.')

    def SetValue(self, Value):
        if Value < self.Min:
            raise ValueError(
                'Value must be bigger than minimal progressbar value.')

        if Value < self.Min:
            raise ValueError(
                'Value must be lower than maximal progressbar value.')

        if '?pbar?' in self.Pattern:
            CharsDone = int((self.LineLength * Value) / self.Max)
            CharsNotDone = int(self.LineLength - CharsDone)

            PBarLine = (self.CharOnDone * CharsDone) + (self.CharOnNotDone *
                                                        CharsNotDone)

        # ?pbar? - Progress Bar
        # ?value? - Value
        # ?min? - Minimal
        # ?max? - Maximal
        # ?donechar? - Char on done
        # ?ndonechar? - Not done char

        if '?pbar?' in self.Pattern:
            ProgressBarUpdate = self.Pattern.replace(
                '?pbar?', PBarLine).replace('?value?', str(Value)).replace(
                    '?min?',
                    str(self.Min)).replace('?max?', str(self.Max)).replace(
                        '?donechar?',
                        self.CharOnDone).replace('?ndonechar?',
                                                 self.CharOnNotDone)
        else:
            ProgressBarUpdate = self.Pattern.replace(
                '?value?', str(Value)).replace('?min?', str(self.Min)).replace(
                    '?max?', str(self.Max)).replace('?donechar?',
                                                    self.CharOnDone).replace(
                                                        '?ndonechar?',
                                                        self.CharOnNotDone)

        PrintOnLine(ProgressBarUpdate)

    def FinishProgressBar(self):
        print()