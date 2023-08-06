from typing import List, Optional


class ClassDomain:
    DEF = "class_domain"

    def __init__(self, name, parent_domain=None):
        self._parent_domain = parent_domain
        self._name = name
        self._classes = []
        self._classes_names = []

    def _sort_label(self):
        self._classes = sorted(self._classes, key=lambda _: _.name)
        self._classes_names = sorted(self._classes_names)

    def set_parent(self, parent_domain):
        self._parent_domain = parent_domain

    @property
    def parent_domain(self):
        return self._parent_domain

    @property
    def name(self):
        return self._name

    def index(self, name):
        self._sort_label()
        return self._classes_names.index(name) + 1

    def add_label(self, item):
        if item.name in self._classes_names:
            return
        self._classes.append(item)
        self._classes_names.append(item.name)

    def __contains__(self, item):
        return item.name in self._classes_names

    def __bool__(self):
        if self._classes:
            return True
        return False

    def format(self):
        domain_name = self.name
        if self.parent_domain:
            domain_name += f"[{self.parent_domain.name}]"
        content = dict()
        content["$def"] = self.DEF
        self._sort_label()
        classes = [_.format() for _ in self._classes]
        content["classes"] = classes
        return {domain_name: content}


class Label:

    def __init__(self, name, supercategories: Optional[List] = None):
        self._name = name
        self._supercategories = []
        if supercategories is not None:
            self._supercategories = supercategories

    @property
    def name(self):
        return self._name

    def add_supercategory(self, label):
        self._supercategories.append(label)

    @property
    def supercategories(self):
        return self._supercategories

    def format(self):
        if not self._supercategories:
            return self._name

        else:
            return self._name + f"[{', '.join([_.name for _ in self.supercategories])}]"
