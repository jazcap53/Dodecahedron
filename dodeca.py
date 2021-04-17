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
        top = 'A'
        bottom = 'L'
        top_row = 'BCDEF'
        bottom_row = 'GHIJK'
        adj_list = {'A': list(top_row)}
        return adj_list

if __name__ == '__main__':
    d = Dodeca()
    # print(d.faces)
    print(d)
    print(d.adj_list)
