""" Python introspection tool """


__version__ = "0.0.3"

from typing import Type

from .extractor import Extractor

from .abstract import AExporter
from .architect import FuncArchitect, StdTypesArchitect
from .exporter import HTMLExporter, JSExporter, JSONExporter


exporters: dict[str, Type[AExporter]] = {
    "js": JSExporter,
    "json": JSONExporter,
    "html": HTMLExporter,
}


def extract(targets, out: str | None = None):
    e = Extractor()
    e.append(StdTypesArchitect()).append(FuncArchitect())
    e.extract(targets)
    if not out:
        return e.maze

    try:
        _, ext = out.rsplit(".", 1)
        exporter = exporters[ext](e.maze)
    except Exception:
        exporter = JSONExporter(e.maze)

    exporter.export(out)
