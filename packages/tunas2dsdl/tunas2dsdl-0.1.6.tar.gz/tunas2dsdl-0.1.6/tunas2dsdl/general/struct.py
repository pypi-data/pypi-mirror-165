from .utils import Util


class Field:
    FIELD_MAPPING = {
        "bbox": "BBox",
        "int": "Int",
        "float": "Num",
        "str": "Str",
        "points": "Polygon",
        "list": "List",
        "media": "Image",
        "bool": "Bool",
        "category": f"Label",
    }

    def __init__(self, name, field_value=None, field_type=None, is_attr=None, param=None):
        self._name = name
        self._is_attr = is_attr
        self.param = param
        self.arg = None
        if field_type is not None:
            self.field_type = self.FIELD_MAPPING[field_type]
        elif field_value is not None:
            self.field_type = self.FIELD_MAPPING[field_value.__class__.__name__]
            if self.field_type == "List":
                self.arg = "etype"
                self.param = self.FIELD_MAPPING[field_value[0].__class__.__name__]
        else:
            raise RuntimeError("not supported field type")
        if field_type == "category":
            self.arg = "dom"
            assert isinstance(self.param, str)
        elif field_type == "list":
            self.arg = "etype"
            assert isinstance(self.param, str)

    @property
    def is_attr(self):
        return self._is_attr

    @property
    def name(self):
        return self._name

    def format(self):
        if not self._is_attr and not self.arg:
            return {self._name: self.field_type}
        elif self.is_attr and not self.arg:
            return {self._name: f"{self.field_type}[is_attr=True]"}
        elif not self.is_attr and self.arg:
            return {self._name: f"{self.field_type}[{self.arg}={self.param}]"}
        else:
            return {self._name: f"{self.field_type}[is_attr=True, {self.arg}={self.param}]"}


class Struct:
    DEF = "struct"
    ARG = "cdom"

    def __init__(self, name, arg=None):
        self._name = name
        self.fields = []
        self.field_names = []
        self._optional = []
        if arg is not None:
            self.ARG = arg

    def add_field(self, item, optional=False):
        if item.name in self.field_names:
            return
        self.fields.append(item)
        self.field_names.append(item.name)
        if optional:
            self._optional.append(item.name)

    def set_optional(self, name):
        if name in self.field_names:
            self._optional.append(name)
            return
        else:
            raise RuntimeError(f"field {name} not exists.")

    @property
    def name(self):
        return self._name

    def format(self):
        content = dict()
        content["$def"] = self.DEF
        content["$params"] = Util.flist([self.ARG])
        content["$fields"] = {}
        for field in self.fields:
            content["$fields"].update(field.format())
        optional_lst = list(set(self._optional))
        if optional_lst:
            content["$optional"] = Util.flist(optional_lst)
        return {self.name: content}

    def as_others_param(self, other_struct):
        return f"{self._name}[{self.ARG}=${other_struct.ARG}]"
