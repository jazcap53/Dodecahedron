import argparse
from dataclasses import dataclass, field
from itertools import combinations, chain


@dataclass
class Pentagon:
    """Represents a face of a dodecahedron"""
    name: str
    colors: tuple[str] = ('Red', 'Blue')
    _color: str = colors[0]

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    def __post_init__(self):
        assert len(self.name) == 1

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}: {self.color}"


@dataclass
class Dodeca:
    """A representation of a dodecahedron: each face may be red or blue"""
    n_rows: int = 4
    # face_names: [['A'], ['B','C','D','E','F'],
    #              ['G','H','I','J','K'], ['L']]
    face_names: list[list[str]] = field(init=False)
    # faces: [Pentagon(name='A'...), Pentagon(name='B'...),
    #        ...Pentagon(name='L'...)]]
    faces: list[Pentagon] = field(init=False)
    face_string: str = field(default='ABCDEFGHIJKL')
    # map each face name to a list of its adjacent face names
    adj_list: dict[str: list[str]] = field(init=False)
    n_blues: int = field(init=False)
    second_colors: iter = field(init=False)  # = combinations(range(12), self.n_blues)
    dict_face_names_to_faces: dict = field(init=False)

    def __init__(self, blues: int):  # blues: c.l.a., defaults to 3
        self.__post_init__(blues)

    def __post_init__(self, blues: int):  # blues: c.l.a., defaults to 3
        self.face_names = [[self.face_string[0]],  # the top face
                           list(self.face_string[1: 6]),  # two 'rows' in between
                           list(self.face_string[6: 11]),
                           [self.face_string[11]]]  # the bottom face
        # flatten self.face_names
        self.faces = [Pentagon(face) for face in chain.from_iterable(self.face_names)]
        self.n_blues = blues
        self.second_colors = combinations(range(12), self.n_blues)
        self.make_adj_list()  # {'A': list('BCDEF'), 'B': list('ACFGK'), ...}
        self.dict_face_names_to_faces = {self.face_string[i]: self.faces[i] 
                                   for i in range(len(self.face_string))}

    def __str__(self):
        return '\n'.join([face.__str__() for face in self.faces])

    def set_colors(self):
        try:
            # blue_faces: a list of self.n_blues ints
            blue_faces = next(self.second_colors)
            for face_ix in blue_faces:
                self.faces[face_ix].color = self.faces[face_ix].colors[1]
        except StopIteration:
            return False
        return True

    def reset_colors(self):
        for face in self.faces:
            face.color = face.colors[0]

    def make_adj_list(self):
        top_face = self.get_face_names_this_row(0)
        top_row_face_names = self.get_face_names_this_row(1)
        bottom_row_face_names = self.get_face_names_this_row(2)
        bottom_face = self.get_face_names_this_row(3)
        self.adj_list = {'A': top_row_face_names}
        for ix, val in enumerate(top_row_face_names):
            self.adj_list[val] = [top_face[0]]
            self.adj_list[val].extend([self.get_prev_face_this_row(top_row_face_names, ix),
                                  self.get_next_face_this_row(top_row_face_names, ix)])
            self.adj_list[val].extend([self.get_prev_face_other_row(bottom_row_face_names, ix),
                                  self.get_next_face_other_row(bottom_row_face_names, ix)])
            self.adj_list[val].sort()
        for ix, val in enumerate(bottom_row_face_names):
            self.adj_list[val] = [bottom_face[0]]
            self.adj_list[val].extend([
                self.get_prev_face_this_row(bottom_row_face_names, ix),
                self.get_next_face_this_row(bottom_row_face_names, ix)
                ])
            self.adj_list[val].extend([
                self.get_prev_face_other_row(top_row_face_names, ix),
                self.get_next_face_other_row(top_row_face_names, ix)
                ])
            self.adj_list[val].sort()
        self.adj_list['L'] = bottom_row_face_names

    def get_face_names_this_row(self, row_id) -> list[str]:
        return self.face_names[row_id]

    @staticmethod
    def get_next_face_this_row(face_list, ix):
        return face_list[ix + 1] if ix < len(face_list) - 1 else face_list[0]

    @staticmethod
    def get_prev_face_this_row(face_list, ix):
        return face_list[ix - 1] if ix > 0 else face_list[len(face_list) - 1]

    @staticmethod
    def get_next_face_other_row(face_list, ix):
        return face_list[ix]

    @staticmethod
    def get_prev_face_other_row(face_list, ix):
        return face_list[ix - 1] if ix > 0 else face_list[len(face_list) - 1]

    def check_no_adjacent_blue_faces(self):
        for i in range(len(self.face_string)):
            face = self.dict_face_names_to_faces[self.face_string[i]]
            face_name = face.name
            assert face_name == self.face_string[i]
            if face.color == 'Red':
                continue
            for adj_face_name in self.adj_list[face_name]:
                adj_face = self.dict_face_names_to_faces[adj_face_name]
                if adj_face.color == 'Blue':    
                    return False
        return True

    def search_colors(self):
        pattern = self.set_colors()
        while pattern:
            if self.check_no_adjacent_blue_faces():
                print(f'Success:\n{self}')
                # self.reset_colors()  # not needed for this use case
                break
            self.reset_colors()
            pattern = self.set_colors()
        else:
            print('Failure')

def main():
    parser = argparse.ArgumentParser(description='Explore the dodecahedron')
    parser.add_argument('--blue', '-b', type=int, default=3,
                        help='Number of blue faces in a red dodecahedron')
    args = parser.parse_args()
    d1 = Dodeca(args.blue)
    d1.search_colors()


if __name__ == '__main__':
    main()
