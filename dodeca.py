from dataclasses import dataclass, field


@dataclass
class Pentagon:
    name: str
    colors: tuple[str] = ('Red', 'Blue')
    edges: tuple[int] = (0, 1, 2, 3, 4)
    color: str = colors[0]

    def __post_init__(self):
        assert len(self.name) == 1

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}: {self.color}"

@dataclass
class Dodeca:
    faces: list[Pentagon] = field(init=False)
    face_string: str = field(default='ABCDEFGHIJKL')
    adj_list: dict[str: list[str]] = field(init=False)

    def __post_init__(self):
        self.faces = [Pentagon(ch) for ch in list(self.face_string)]
        self.adj_list = self.make_adj_list()  # {'A': 'BCDEF'.split(), 'B': 'ACFGK'.split(), 'C': 'ABDGH', 'L': 'GHIJK'.split()}

    def __str__(self):
        return '\n'.join([face.__str__() for face in self.faces])

    def make_adj_list(self):
        top_face = self.face_string[0]
        top_row_faces = list(self.face_string[1: 6])
        bottom_row_faces = list(self.face_string[6: 11])
        bottom_face = self.face_string[11]
        adj_list = {'A': top_row_faces}
        for ix, val in enumerate(top_row_faces):
            adj_list[val] = [top_face]
            adj_list[val].extend([self.get_prev_face(top_row_faces, ix), self.get_next_face(top_row_faces, ix)])
            # adj_list[val] = [top].extend([top_row_faces[(ix + 1) % len(top_row_faces)],  
        return adj_list

    def get_faces_this_row():
        pass


    @staticmethod
    def get_next_face(face_list, ix):
        return face_list[ix + 1] if ix < len(face_list) - 1 else face_list[0]

    @staticmethod
    def get_prev_face(face_list, ix):
        return face_list[ix - 1] if ix > 0 else face_list[len(face_list) - 1]
        





if __name__ == '__main__':
    d = Dodeca()
    # print(d.faces)
    print(d)
    print(d.adj_list)
