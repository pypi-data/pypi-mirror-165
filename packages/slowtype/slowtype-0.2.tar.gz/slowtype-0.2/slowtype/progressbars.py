from slowtype.more_functions import PrintOnLine


class ProgressBar:

    def __init__(self,
                 Min,
                 Max,
                 CharOnDone='#',
                 CharOnNotDone='_',
                 LineLength=20,
                 ShowPercents=True,
                 PercentsPattern='[?p%]',
                 ShowMessage=True,
                 Message='Progress:'):
        self.Min = Min
        self.Max = Max
        self.CharOnDone = CharOnDone
        self.CharOnNotDone = CharOnNotDone
        self.LineLength = LineLength
        self.ShowPercents = ShowPercents
        self.PercentsPattern = PercentsPattern
        self.ShowMessage = ShowMessage
        self.Message = Message

    def SetValue(self, Value):
        ProgressBarUpdate = ''

        if self.ShowMessage:
            ProgressBarUpdate += self.Message

        CharsDone = int((self.LineLength * Value) / self.Max)
        CharsNotDone = int(self.LineLength - CharsDone)

        PBarLine = (self.CharOnDone * CharsDone) + (self.CharOnNotDone *
                                                  CharsNotDone)

        ProgressBarUpdate += ' ' + PBarLine

        if self.ShowPercents:
            ProgressBarUpdate += ' ' + self.PercentsPattern.replace(
                '?p', str(Value))

        PrintOnLine(ProgressBarUpdate)

    def FinishProgressBar(self):
        print()