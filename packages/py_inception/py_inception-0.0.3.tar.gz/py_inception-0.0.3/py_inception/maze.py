import json


class Maze:
    def __init__(self):
        self.objects = {}
        self.strings = {}
        self.lists = {}
        self.dicts = {}
        self.funcs = {}
        self.targets = []
        self.object = id(object)
        self.type = id(type)
        self.export = [
            "objects",
            "strings",
            "lists",
            "dicts",
            "funcs",
            "targets",
            "object",
            "type",
            ]

    def get_model(self):
        model = {}
        for i in self.export:
            model[i] = getattr(self, i)
        return model

    def get_js(self):
        model = self.get_json()
        js = "const model=" + model
        return js

    def get_json(self):
        return json.dumps(self.get_model(), indent=1)
