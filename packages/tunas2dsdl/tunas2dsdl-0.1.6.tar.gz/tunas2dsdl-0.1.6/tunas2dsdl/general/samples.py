from .utils import Util


class DataSample:
    def __init__(self, struct, class_domain):
        self.sample_struct = struct
        self.class_domain = class_domain
        self.samples = []

    def add_item(self, item, pre_format=True):
        if pre_format:
            sample = item.copy()
            for k, v in sample.items():
                if Util.is_list_of(v, dict):
                    sample[k] = [Util.fmap(_) for _ in v]
                elif isinstance(v, str):
                    sample[k] = Util.add_quotes(v)
            self.samples.append(sample)
        else:
            self.samples.append(item)

    @property
    def sample_type(self):
        return f"{self.sample_struct.name}[{self.sample_struct.ARG}={self.class_domain.name}]"

    def format(self):
        content = {}
        content["sample-type"] = self.sample_type
        content["samples"] = self.samples
        return {"data": content}
