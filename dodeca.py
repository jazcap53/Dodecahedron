from dataclasses import dataclass, field


@dataclass
class Pentagon:
    name: str
    colors: tuple[str] = ('Red', 'Blue')

    def __post_init__(self):
        assert len(self.name) == 1


@dataclass
class Dodeca:
    faces: list[Pentagon] = field(init=False)
    face_string: str = field(default='ABCDEFGHIJKL')

    def __post_init__(self):
        self.faces = [Pentagon(ch) for ch in list(self.face_string)]


if __name__ == '__main__':
    d = Dodeca()
    print(d.faces)
