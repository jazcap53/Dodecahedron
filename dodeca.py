"""
Check the maximum number of faces in a red dodecahedron that
can be changed to blue such that no two adjoining faces are blue
"""
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
        """The color of the face"""
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    def __post_init__(self):
        assert len(self.name) == 1

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}: {self.color}"


@dataclass
class Dodecahedron:
    """Represents a dodecahedron: each face may be red or blue"""
    # face_names: [['A'], ['B','C','D','E','F'],
    #              ['G','H','I','J','K'], ['L']]
    face_names: list[list[str]] = field(init=False)
    # faces: [Pentagon(name='A'...), Pentagon(name='B'...),
    #        ...Pentagon(name='L'...)]]
    faces: list[Pentagon] = field(init=False)
    face_string: str = field(default='ABCDEFGHIJKL')
    # face name => [adjacent face names]
    adj_list: dict[str: list[str]] = field(init=False)
    n_blues: int = field(init=False)
    second_colors: iter = field(init=False)  # yields [int]: list of blue faces
    dict_face_names_to_faces: dict = field(init=False)

    def __init__(self, blues: int):  # blues: c.l.a., defaults to 3
        self.__post_init__(blues)

    def __post_init__(self, blues: int):  # blues: c.l.a., defaults to 3
        self.face_names = [[self.face_string[0]],  # the top face
                           list(self.face_string[1: 6]),  # 2 'rows' in between
                           list(self.face_string[6: 11]),
                           [self.face_string[11]]]  # the bottom face
        # flatten self.face_names
        self.faces = [Pentagon(face)
                      for face in chain.from_iterable(self.face_names)]
        self.n_blues = blues
        self.second_colors = combinations(range(12), self.n_blues)
        self.make_adj_list()  # {'A': list('BCDEF'), 'B': list('ACFGK'), ...}
        self.dict_face_names_to_faces = {self.face_string[i]: self.faces[i]
                                   for i in range(len(self.face_string))}

    def __str__(self):
        return '\n'.join([face.__str__() for face in self.faces])

    def set_colors(self):
        """Set colors to the next combination we will test """
        try:
            # blue_faces: a list of self.n_blues ints
            blue_faces = next(self.second_colors)
            for face_index in blue_faces:
                self.faces[face_index].color = self.faces[face_index].colors[1]
        except StopIteration:
            return False
        return True

    def reset_colors(self):
        """Set all faces to the default color"""
        for face in self.faces:
            face.color = face.colors[0]

    def make_adj_list(self):
        row_1_faces = self.face_names[1]
        self.adj_list = {'A':  row_1_faces}
        for row_faces in self.face_names:
            for index, val in enumerate(row_faces):
                self.adj_list[val] = [self.get_next_face_this_row(row_faces, index)]
                self.adj_list[val].append(self.get_prev_face_this_row(row_faces, index))
                if index < len(row_faces) - 1: # No neighbor above on top row.
                    self.adj_list[val].append(row_faces[index + 1])
        self.adj_list['L'] = row_2_faces = self.face_names[2] # row_2_faces: a list with one element
        for index, val in enumerate(row_1_faces):
            self.adj_list[val].extend(self.get_other_adjacent_faces(row_1_faces, row_2_faces, index))

    def get_other_adjacent_faces(self, this_row_faces, other_row_faces, index):
        """Retrieve adjacent faces from this row and other row"""
        return [self.get_prev_face_this_row(this_row_faces, index),
                self.get_next_face_this_row(this_row_faces, index),
                self.get_prev_face_other_row(other_row_faces, index),
                self.get_next_face_other_row(other_row_faces, index)]

    @staticmethod
    def get_next_face_this_row(face_list, index):
        """Get next adjoining face from this row"""
        return face_list[index + 1] if index < len(face_list) - 1 else face_list[0]

    @staticmethod
    def get_prev_face_this_row(face_list, index):
        """Get previous adjoining face from this row"""
        return face_list[index - 1] if index > 0 else face_list[len(face_list) - 1]

    @staticmethod
    def get_next_face_other_row(face_list, index):
        """Get next adjoining face from other row"""
        return face_list[index]

    @staticmethod
    def get_prev_face_other_row(face_list, index):
        """Get previous adjoining face from other row"""
        return face_list[index - 1] if index > 0 else face_list[len(face_list) - 1]

    def check_no_adjacent_blue_faces(self):
        """Check that no two blue faces are adjacent"""
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
        """Try each combination of face colors"""
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
    """Run the program"""
    parser = argparse.ArgumentParser(description='Explore the dodecahedron')
    parser.add_argument('--blue', '-b', type=int, default=3,
                        help='Number of blue faces in a red dodecahedron')
    args = parser.parse_args()
    d_1 = Dodecahedron(args.blue)
    d_1.search_colors()


if __name__ == '__main__':
    main()
