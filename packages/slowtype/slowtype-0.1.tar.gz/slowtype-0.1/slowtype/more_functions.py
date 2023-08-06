from sys import stdout


def PrintOnLine(TypeText: str,
                Clear: bool = True,
                NewLineAfterEnd: bool = False):
    """
    
    Types a text on line, where cursor is now
    
    """
    print(TypeText, end='' if not Clear else '\r', flush=True)

    if NewLineAfterEnd:
        print()


def ClearLine(GoToLineUp: bool = False):
    """
    
    Clear a line, where cursor is now
    
    """

    if GoToLineUp:
        stdout.write('\x1b[1A')
        stdout.write('\x1b[2K')
    else:
        stdout.write('\x1b[2K')


def LineUp():
    """
    
    Moving cursor on 1 line up
    
    """

    stdout.write('\x1b[1A')