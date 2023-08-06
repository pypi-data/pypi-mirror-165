from .abstract import AArchitect
from .architect import CoreArchitect
from .maze import Maze


class Extractor:
    def __init__(self, coreparser=None):
        self.maze = Maze()
        self.chain = None
        self.parsers = []
        self.append(coreparser or CoreArchitect())

    def append(self, arch: AArchitect):
        arch.set_extractor(self)
        arch.set_next(self.chain)
        self.chain = arch
        self.parsers.append(arch)
        return self

    def parse(
        self,
        var: object,
        parse_as: str = "object",
        *,
        metadata: dict | None = None,
    ):
        if not self.chain:
            return None
        return self.chain.parse(var, parse_as, metadata=metadata)

    def extract(self, targets):
        for target in targets:
            res = self.parse(target, "object")
            if res is not None:
                self.maze.targets.append(res["id"])

