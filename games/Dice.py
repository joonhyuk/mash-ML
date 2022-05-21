import random

class Dice:
    def __init__(self, faces = range(1, 7)) -> None:
        self.face = None
        self.faces = None
        self.set_faces(faces)
    
    def set_faces(self, faces):
        try:
            self.len = len(faces)
        except:
            raise ValueError('Faces must be a sequence like tuple, list, dict')
        if self.len < 2:
            raise ValueError('The dice must have at least 2 sides.')
        self.faces = faces
        self.roll()
    
    def roll(self, exception = None, weights = None, k = 1):
        if isinstance(self.faces, dict):
            k = random.choice(list(self.faces.keys()))
            self.face = k, self.faces[k]
            return self.face
        self.face = random.choice(self.faces)
        return self.face
    
    @classmethod
    def coin(cls):
        return cls((True, False))
    
    @classmethod
    def dx(cls, number_of_sides = 6):
        return cls(range(1, number_of_sides + 1))


if __name__ == '__main__':
    d = Dice({'k1':1, 'k2':2})
    print(d.roll())