try:
    import ruamel_yaml as yaml
    from ruamel_yaml import YAML
except ImportError:
    import ruamel.yaml as yaml
    from ruamel.yaml import YAML

class Util:

    @staticmethod
    def is_list_of(obj, cls):
        if isinstance(obj, list):
            return isinstance(obj[0], cls)
        return False

    @staticmethod
    def add_quotes(string):
        # string = f'"{string}"'
        string = yaml.scalarstring.DoubleQuotedScalarString(string)
        return string

    @staticmethod
    def flist(x):
        x = [Util.add_quotes(_) for _ in x]
        retval = yaml.comments.CommentedSeq(x)
        retval.fa.set_flow_style()  # fa -> format attribute
        return retval

    @staticmethod
    def fmap(x):
        retval = yaml.comments.CommentedMap(x)
        retval.fa.set_flow_style()  # fa -> format attribute
        return retval