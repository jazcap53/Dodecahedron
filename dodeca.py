from dataclasses import dataclass, field
from itertools import combinations
# from collections import namedtuple


@dataclass
class Pentagon:
    name: str
    colors: tuple[str] = ('Red', 'Blue')
    _color: str = colors[0]
    # edges: tuple[int] = (0, 1, 2, 3, 4)
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
    n_rows: int = 4
    face_names: list[list[str]] = field(init=False)
    faces: list[list[Pentagon]] = field(init=False)
    face_string: str = field(default='ABCDEFGHIJKL')
    adj_list: dict[str: list[str]] = field(init=False)
    alt_colors: iter = combinations([0,1,2,3,4,5,6,7,8,9,10,11], 3)

    def __post_init__(self):    
        self.face_names = [[self.face_string[0]], [self.face_string[i] for i in range(1, 6)],
                      [self.face_string[i] for i in range(6, 11)], [self.face_string[11]]]
        self.faces = [Pentagon(self.face_names[i][j]) 
                      for i in range(len(self.face_names))
                      for j in range(len(self.face_names[i]))]
        self.make_adj_list()  # {'A': list('BCDEF'), 'B': list('ACFGK'), ...}

    def __str__(self):
        return '\n'.join([face.__str__() for face in self.faces])

    def set_colors(self):
        try:
            blue_faces = next(self.alt_colors)
            for face_ix in blue_faces:
                self.faces[face_ix].color = self.faces[face_ix].colors[1]  # = Pentagon().colors[1]
        except StopIteration:
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
            self.adj_list[val].extend([self.get_prev_face_this_row(bottom_row_face_names, ix),
                                  self.get_next_face_this_row(bottom_row_face_names, ix)])
            self.adj_list[val].extend([self.get_prev_face_other_row(top_row_face_names, ix),
                                  self.get_next_face_other_row(top_row_face_names, ix)])
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
        pass


    def get_max_blue_faces(self):
        pass

    def set_blue_faces(self, ct):
        pass

    def find_adj_blue_faces(self):
        pass


if __name__ == '__main__':
    d = Dodeca()
    print(d)
    print()
    print(d.adj_list)
    # combo_list = combinations([0,1,2,3,4,5,6,7,8,9,10,11], 3)
    # for _ in range(150):
    #     next(combo_list)
    # print(next(combo_list))
    print()
    d.set_colors()
    print(d)
    print()
    d.reset_colors()
    print(d)
    print()
    d.set_colors()
    print(d)
