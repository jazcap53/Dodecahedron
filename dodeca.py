from dataclasses import dataclass, field


@dataclass
class Pentagon:
    name: str
    colors: tuple[str] = ('Red', 'Blue')
    # edges: tuple[int] = (0, 1, 2, 3, 4)
    color: str = colors[0]

    def __post_init__(self):
        assert len(self.name) == 1

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}: {self.color}"

@dataclass
class Dodeca:
    n_rows: int = 4
    faces: list[list[Pentagon]] = field(init=False)
    face_string: str = field(default='ABCDEFGHIJKL')
    adj_list: dict[str: list[str]] = field(init=False)

    def __post_init__(self):
        self.faces = [[self.face_string[0]], [self.face_string[i] for i in range(1, 6)],
                      [self.face_string[i] for i in range(6, 11)], [self.face_string[11]]]
        self.adj_list = self.make_adj_list()  # {'A': 'BCDEF'.split(), 'B': 'ACFGK'.split(), 'C': 'ABDGH', 'L': 'GHIJK'.split()}

    def __str__(self):
        return '\n'.join([face.__str__() for face in self.faces])

    def make_adj_list(self):
        top_face = self.get_faces_this_row(0)
        top_row_faces = self.get_faces_this_row(1)
        bottom_row_faces = self.get_faces_this_row(2)
        bottom_face = self.get_faces_this_row(3)
        adj_list = {'A': top_row_faces}
        for ix, val in enumerate(top_row_faces):
            adj_list[val] = [top_face[0]]
            adj_list[val].extend([self.get_prev_face_this_row(top_row_faces, ix),
                                  self.get_next_face_this_row(top_row_faces, ix)])
            adj_list[val].extend([self.get_prev_face_other_row(bottom_row_faces, ix),
                                  self.get_next_face_other_row(bottom_row_faces, ix)])
        adj_list['L'] = bottom_row_faces
        return adj_list

    def get_faces_this_row(self, row_id) -> list[str]:
        return self.faces[row_id]


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



if __name__ == '__main__':
    d = Dodeca()
    # print(d.faces)
    print(d)
    print(d.adj_list)
