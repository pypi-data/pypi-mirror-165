from .abstract import AExporter
from .htmltemplate import BODY, CSS, HEAD, SCRIPT


class JSONExporter(AExporter):
    """ Export data to single JSON file """
    def export(self, name: str, path: str = "."):
        with open(name, "wt") as f:
            f.write(self.maze.get_json())


class JSExporter(AExporter):
    """ Export data to single JS file """
    def export(self, name: str, path: str = "."):
        js = "const model=" + self.maze.get_json()
        with open(name, "wt") as f:
            f.write(js)


class HTMLExporter(AExporter):
    """ Export data to single HTML file """
    def export(self, name: str, path: str = "."):
        js = "<script>const model=" + self.maze.get_json() + "</script>"
        with open(name, "wt") as f:
            f.write(HEAD)
            f.write(CSS)
            f.write(js)
            f.write(BODY)
            f.write(SCRIPT)
