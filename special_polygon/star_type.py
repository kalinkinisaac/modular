from enum import Enum

class StarType(Enum):
    Segment = 0
    SlingShot = 1
    Racket = 2

    @staticmethod
    def star_type(neighbors):
        if len(neighbors) == 1:
            return StarType.Segment

        elif len(set(neighbors)) == 3:
            return StarType.SlingShot

        else:
            return StarType.Racket
