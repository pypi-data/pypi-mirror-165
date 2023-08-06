# SlowType - Small python library for type-effect
## All functions and classes
```python
SlowTypes.SlowType()
```
### - Default SlowType module function.
### _______________________
```python
SlowTypes.SlowType_DelayRandom()
```
### - SlowType with random duration
### - Alternative:
```python
SlowTypes.SlowType_UsingDelayGenerator(..., lambda x, y: random.uniform(0.1, 0.2))
```
### _______________________
```python
SlowTypes.SlowType_UsingDelayGenerator()
```
### - Using function to get delay
### - DelayGenerators (or user custom)
### _______________________
```python
SlowtypeExamples.ProgressBarExample()
```
### - Progress bar example
### _______________________
```python
SlowtypeExamples.PasswordHackerExample()
```
### _______________________
### - Password hacker example
```python
DelayGenerators.Faster()
```
### - Makes type faster after next char
### _______________________
```python
DelayGenerators.Slower()
```
### - Makes type slower after next char
### _______________________
```python
DelayGenerators.PrintSleep(x, y)
```
### - Prints X chars and waiting Y seconds
### _______________________
```python
PrintOnLine()
```
### - Print a text on line, where cursor is
### _______________________
```python
ClearLine()
```
### - Clear line, where cursor
# SlowType - Python type-print module
## All functions and classes
```python
SlowTypes.SlowType()
```
### - Default SlowType module function.
### _______________________
```python
SlowTypes.SlowType_DelayRandom()
```
### - SlowType with random duration
### - Alternative:
```python
SlowTypes.SlowType_UsingDelayGenerator(..., lambda x, y: random.uniform(0.1, 0.2))
```
### _______________________
```python
SlowTypes.SlowType_UsingDelayGenerator()
```
### - Using function to get delay
### - DelayGenerators (or user custom)
### _______________________
```python
SlowtypeExamples.ProgressBarExample()
```
### - Progress bar example
### _______________________
```python
SlowtypeExamples.PasswordHackerExample()
```
### - Password hacker example
### _______________________
```python
DelayGenerators.Faster()
```
### - Makes type faster after next char
### _______________________
```python
DelayGenerators.Slower()
```
### - Makes type slower after next char
### _______________________
```python
DelayGenerators.PrintSleep(x, y)
```
### - Prints X chars and waiting Y seconds
### _______________________
```python
PrintOnLine()
```
### - Print a text on line, where cursor is
### _______________________
```python
ClearLine()
```
### - Clear line, where cursor
### _______________________
```python
LineUp()
```
### - Moving cursor up
### _______________________
```python
ProgressBar()
```
### - Progressbar (scroll down for examples)
### _______________________
## Examples
### Example of slow type with input:
```python
text = SlowTypes.SlowType('What is your name?: ', 0.1, True)
```
### Example of using SlowTypes.SlowType_UsingDelayGenerator
```python
SlowTypes.SlowType_UsingDelayGenerator('Just a big string... ' * 5, DelayGenerators.Faster, 10)
```
```python
LineUp()
```
### - Moving cursor up
## Examples
### Example of slow type with input:
```python
text = SlowTypes.SlowType('What is your name?: ', 0.1, True)
```
### Example of using SlowTypes.SlowType_UsingDelayGenerator
```python
SlowTypes.SlowType_UsingDelayGenerator('Just a big string... ' * 5, DelayGenerators.Faster, 10)
```
## 0.2 - Progressbars!
### Example of progressbar
```python
from time import sleep

# Initializing ProgressBar
# (ProgressBar dont shows on initializing)
LoadingProgress = ProgressBar(1, 100, LineLength=50, Message = 'Loading...')

# Loading... (ProgressBar(Min, Max).SetValue(Value))
for x in range(1, 100):
    LoadingProgress.SetValue(x)
    sleep(.01)

LoadingProgress.FinishProgressBar()
```

```python
ProgressBar(
    1,
    100,
    LineLength=10,
    Message = 'Loading...',
    CharOnDone = '+',
    CharOnNotDone = '_',
    PercentsPattern='(?p/100)').SetValue(40)

# Output:
# Loading... ++++______ (40/100)

# ?p in PercentsPattern is value
```
#### Translated by google translate!