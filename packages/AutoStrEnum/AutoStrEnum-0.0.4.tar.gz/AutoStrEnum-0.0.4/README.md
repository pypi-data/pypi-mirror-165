# AutoStrEnum

This project defines an extended `Enum` class.  
It can automatically assign the value to your Enum member, and the value is just the same as the member name!  
And when you print it, you won't see the Enum name in front of the class member.

## Install

```shell
pip install AutoStrEnum
```

## Demo

```python
from enum import auto

from AutoStrEnum import AutoStrEnum


class Fruit(AutoStrEnum):
    BANANA = auto()
    WATERMELON = auto()
    DURIAN = auto()


class MagicFruit(AutoStrEnum):
    BANANA = auto()
    WATERMELON = auto()
    DURIAN = auto()


if __name__ == '__main__':
    print(Fruit, MagicFruit)
    print(Fruit.BANANA, Fruit.WATERMELON, Fruit.DURIAN)

    print('should be True:', Fruit.BANANA in Fruit)
    print('should be True:', Fruit.BANANA is Fruit.BANANA)
    print('should be True:', Fruit.BANANA == Fruit.BANANA)
    print('should be True:', isinstance(Fruit.BANANA, Fruit))
    print('should be False:', isinstance(Fruit.BANANA, str))
    print('should be False:', isinstance(Fruit.BANANA, MagicFruit))
    print('should be False:', isinstance(False, Fruit))

    # We also can use as dict key!
    test_dict = {
        Fruit: {
            Fruit.BANANA: 2,
            Fruit.DURIAN: 10,
            Fruit.WATERMELON: 0
        }}

    print(test_dict)
```

```shell
$ python demo.py
Fruit MagicFruit
BANANA WATERMELON DURIAN
should be True: True
should be True: True
should be True: True
should be True: True
should be False: False
should be False: False
should be False: False
{Fruit: {BANANA: 2, DURIAN: 10, WATERMELON: 0}}
```
