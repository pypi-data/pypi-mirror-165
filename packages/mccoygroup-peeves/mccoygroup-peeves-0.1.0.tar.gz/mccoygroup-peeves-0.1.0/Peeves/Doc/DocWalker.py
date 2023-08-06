"""
Provides a class that will walk through a set of objects & their children, as loaded into memory, and will generate Markdown for each.
The actual object Markdown is written by the things in the `Writers` module.
"""

import os, types, collections, inspect, importlib, re
from .TemplateEngine import *
from .ObjectWalker import ObjectSpec
from .ExamplesParser import ExamplesParser
from .MarkdownTemplates import MarkdownTemplateFormatter, MarkdownOps

__all__ = [
    "DocWalker",
    "ModuleWriter",
    "ClassWriter",
    "FunctionWriter",
    "MethodWriter",
    "ObjectWriter",
    "IndexWriter"
]

class DocSpec(ObjectSpec):
    """
    A specification for an object to document.
    Supports the fields given by `spec_fields`.
    """
    spec_fields = (
        'id', # name for resolving the object
        'parent', # parent object name for writing,
        'children',
        'examples_root',
        'tests_root'
    )

    def __repr__(self):
        return '{}({})'.format(
            type(self).__name__,
            super().__repr__()
        )

class ExamplesExtractor(TemplateResourceExtractor):
    resource_keys = ['examples']
    resource_attrs = ['__examples__']

class TestsExtractor(TemplateResourceExtractor):
    resource_keys = ['tests']
    resource_attrs = ['__tests__']
    extension = 'Tests.py'
    def path_extension(self, handler:TemplateHandler):
        """
        Provides the default examples path for the object
        :return:
        :rtype:
        """
        base = super().path_extension(handler)
        return [base, os.path.split(base)[1]]
    def load(self, handler:TemplateHandler):
        res = super().load(handler)
        if res is not None:
            res = ExamplesParser(res)
        return res

class TestExamplesFormatter:
    def __init__(self, parser):
        if isinstance(parser, str):
            parser = ExamplesParser(parser)
        self.parser = parser

    @classmethod
    def from_file(cls, tests_file):
        with open(tests_file) as f:
            return cls(f.read())

    def get_template_parameters(self):
        """
        Formats an examples file

        :return:
        :rtype:
        """
        imports = self.parser.setup
        setup = "\n".join(self.parser.format_node(node) for node in imports)

        cls = self.parser.class_spec
        class_setup = "\n".join(
            [
                "class {}({}):".format(
                    cls[0].name,
                    ",".join(x.id for x in cls[0].bases)
                ),
                *(self.parser.format_node(node) for node in cls[1])
            ]
        )

        return dict(
            names=list(self.parser.functions.keys()),
            tests=[self.parser.format_node(v) for v in self.parser.functions.values()],
            setup=setup,
            class_setup=class_setup
        )

class DocTemplateOps(MarkdownOps):
    ...

class DocTemplateHandler(TemplateHandler):
    protected_fields = {'id'}
    default_fields = {'details': "", "related": ""}
    def __init__(self,
                 obj,
                 *,
                 out=None,
                 engine: TemplateEngine=None,
                 root=None,
                 examples_loader:ExamplesExtractor=None,
                 tests_loader:TestsExtractor=None,
                 include_line_numbers=True,
                 walker:'TemplateWalker'=None,
                 **extra_fields
                 ):

        self.examples_loader = examples_loader
        self.tests_loader = tests_loader
        self.include_line_numbers = include_line_numbers
        super().__init__(obj, out=out, engine=engine, root=root, walker=walker, **extra_fields)

    def get_lineno(self):
        # try:
        if self.include_line_numbers:
            obj = self.obj
            if isinstance(obj, (classmethod, staticmethod, property, types.MethodDescriptorType)):
                obj = obj.fget
            elif not isinstance(obj, (type, types.ModuleType, types.FunctionType, types.MethodDescriptorType, types.MethodType)):
                obj = type(obj)
            try:
                lineno = 1 + inspect.findsource(obj)[1] if self.include_line_numbers else ""
            except:
                lineno = ""
        else:
            lineno = ""
        # except:
        #     lineno = ""
        return lineno

    def parse_doc(self, doc):
        """

        :param doc:
        :type doc: str
        :return:
        :rtype:
        """

        # parses a docstring based on reStructured text type specs but Markdown description
        splits = inspect.cleandoc(doc.strip()).splitlines()

        params = collections.deque()
        param_map = {}
        extra_fields = {}

        active_tag = None
        description = []
        for line in splits:
            if line.startswith(":"):
                if line.startswith(":param"):
                    bits = line.split(":", 2)[1:]
                    name = bits[0][5:].strip()
                    active_tag = name
                    if name not in param_map:
                        params.appendleft(name)
                        param_map[name] = {"name": name, "type": "Any", "description": []}
                    desc = bits[1].strip() if len(bits) == 2 else ""
                    if len(desc) > 0:
                        param_map[name]["description"].append(desc)
                elif line.startswith(":type"):
                    bits = line.split(":", 2)[1:]
                    name = bits[0][4:].strip()
                    active_tag = name
                    if name not in param_map:
                        params.appendleft(name)
                        param_map[name] = {"name": name, "type": "Any", "description": []}
                    t = bits[1].strip() if len(bits) == 2 else ""
                    if len(t) > 0:
                        param_map[name]["type"] = t
                elif line.startswith(":return"):
                    bits = line.split(":", 2)[1:]
                    name = ":returns"
                    active_tag = name
                    if name not in param_map:
                        params.appendleft(name)
                        param_map[name] = {"name": name, "type": "_", "description": []}
                    t = bits[1].strip() if len(bits) == 2 else ""
                    if len(t) > 0:
                        param_map[name]["description"] = t
                elif line.startswith(":rtype"):
                    bits = line.split(":", 2)[1:]
                    name = ":returns"
                    active_tag = name
                    if name not in param_map:
                        params.appendleft(name)
                        param_map[name] = {"name": name, "type": "_", "description": []}
                    t = bits[1].strip() if len(bits) == 2 else ""
                    if len(t) > 0:
                        param_map[name]["type"] = t
                else:
                    split = line.split()[0]
                    if len(split) > 2 and split.endswith(":"):
                        bits = line.split(":", 2)[1:]
                        name = bits[0]
                        active_tag = name
                        t = bits[1].strip() if len(bits) == 2 else ""
                        if len(t) > 0:
                            extra_fields[name] = [t]
                        else:
                            extra_fields[name] = []
            else:
                if active_tag is None:
                    description.append(line.strip())
                else:
                    if active_tag in param_map:
                        param_map[active_tag]['description'].append(line)
                    else:
                        extra_fields[active_tag].append(line)
        for v in param_map.values():
            v['description'] = "\n".join(v['description'])
        for k, v in extra_fields.items():
            extra_fields[k] = "\n".join(v)

        return inspect.cleandoc("\n".join(description)).strip(), param_map, extra_fields

    def load_examples(self):
        return self.examples_loader.load(self) if self.examples_loader is not None else None
    def load_tests(self):
        tests = self.tests_loader.load(self) if self.tests_loader is not None else None
        if tests is None:
            parent_tests = self.resolve_key('parent_tests')
            if parent_tests is not None:
                tests = parent_tests.filter_by_name(self.name.split(".")[-1])
        if tests is not None:
            self.extra_fields['parent_tests'] = tests
            tests = TestExamplesFormatter(tests).get_template_parameters()
        return tests

class DocObjectTemplateHandler(DocTemplateHandler):
    def get_package_and_url(self, include_url_base=True):
        pkg, file_url=super().get_package_and_url(include_url_base=include_url_base)
        try:
            base_url, ext = file_url.rsplit("/", 1)
        except ValueError:
            pass
        else:
            if ext == '__init__.py':
                try:
                    base_url, ext = base_url.rsplit("/", 1)
                except ValueError:
                    pass
            file_url = base_url + '.py'
        return pkg, file_url

    def load_examples(self):
        return self.examples_loader.load(self) if self.examples_loader is not None else None
    def load_tests(self):
        tests = self.tests_loader.load(self) if self.tests_loader is not None else None
        if tests is None:
            parent_tests = self.resolve_key('parent_tests')
            if parent_tests is not None:
                tests = parent_tests.filter_by_name(self.name.split(".")[-1])
        if tests is not None:
            self.extra_fields['parent_tests'] = tests
            tests = TestExamplesFormatter(tests).get_template_parameters()
        return tests
class ModuleWriter(DocTemplateHandler):
    """A writer targeted to a module object. Just needs to write the Module metadata."""
    template = 'module.md'
    def __init__(self, obj, **kwargs):
        if isinstance(obj, str):
            obj = importlib.import_module(obj)
        super().__init__(obj, **kwargs)

    def get_template_params(self):
        """
        Provides module specific parameters
        :return:
        :rtype:
        """

        mod = self.obj  # type: types.ModuleType
        name = mod.__name__
        ident = self.identifier
        ident_depth = len(ident.split("."))
        # get identifiers
        idents = [".".join(self.get_target_extension(getattr(mod, a))) for a in self.get_members(mod)]
        # flattend them
        idents = [i for i in idents if ident in i]
        # split by qualified names
        idents = [".".join(a.split(".")[ident_depth-1:]) for a in idents]
        descr, _, fields = self.parse_doc(mod.__doc__ if mod.__doc__ is not None else '')
        # long_descr = mod.__long_doc__ if hasattr(mod, '__long_doc__') and mod.__long_doc__ is not None else ''

        ex = self.load_examples()
        tests = self.load_tests()
        return dict({
            'id': ident,
            'description': descr.strip(),
            # 'long_description': long_descr.strip(),
            'name': name,
            'members': idents,
            'examples': ex,
            'tests': tests,
            'lineno' : self.get_lineno()
        }, **fields)

    @classmethod
    def get_members(cls, mod):
        return (mod.__all__ if hasattr(mod, '__all__') else [])

class ClassWriter(DocObjectTemplateHandler):
    """A writer targeted to a class"""

    template = 'class.md'
    def load_methods(self, function_writer=None):
        """
        Loads the methods supported by the class

        :param function_writer:
        :type function_writer:
        :return:
        :rtype:
        """

        if function_writer is None:
            function_writer = self.walker.method_handler

        cls = self.obj
        keys = cls.__all__ if hasattr(cls, '__all__') else list(cls.__dict__.keys())

        props = []
        methods = []

        extra_fields = self.extra_fields.copy()
        pkg, file_url = self.package_path
        extra_fields['package_name'] = pkg
        extra_fields['file_url'] = file_url
        extra_fields['package_url'] = os.path.dirname(file_url)
        for k in keys:
            o = getattr(cls, k)
            if isinstance(o, (types.FunctionType, types.MethodType, classmethod, staticmethod, property)):
                if not k.startswith("_") or (k.startswith("__") and k.endswith("__")):
                    methods.append(
                        self.walker.get_handler(
                            o,
                            cls=function_writer,
                            name=k,
                            out_file=None,
                            extra_fields=extra_fields,
                            parent=self.identifier
                        )
                    )
            else:
                if not k.startswith("_"):
                    props.append((k, o))

        return props, methods

    def format_prop(self, k, o):
        return '{}: {}'.format(k, type(o).__name__)

    def get_template_params(self, function_writer=None):
        """

        :param function_writer:
        :type function_writer:
        :return:
        :rtype:
        """

        cls = self.obj  # type: type
        ex = self.load_examples()
        tests = self.load_tests()
        name = cls.__name__
        ident = self.identifier
        props, methods = self.load_methods(function_writer=function_writer)
        descr, param, fields = self.parse_doc(cls.__doc__ if cls.__doc__ is not None else '')
        lineno = self.get_lineno()

        return dict({
            'id': ident,
            'name': name,
            'lineno': lineno,
            'description': descr,
            'parameters': param,
            'props': props,
            'methods': methods,
            'examples': ex if ex is not None else "",
            'tests': tests
        }, **fields)

class FunctionWriter(DocObjectTemplateHandler):
    """
    Writer to dump functions to file
    """

    template = 'function.md'

    def get_signature(self):
        return str(inspect.signature(self.obj))

    def get_template_params(self, **kwargs):
        f = self.obj  # type: types.FunctionType
        ident = self.identifier
        signature = self.get_signature()
        mem_obj_pat = re.compile(" object at \w+>")
        signature = re.sub(mem_obj_pat, " instance>", signature)
        name = self.get_name()
        descr, param, fields = self.parse_doc(f.__doc__ if f.__doc__ is not None else '')
        ex = self.load_examples()
        tests = self.load_tests()
        lineno = self.get_lineno()
        return dict({
            'id': ident,
            'name': name,
            'lineno': lineno,
            'signature': signature,
            'parameters': param,
            'description': descr,
            'examples': ex if ex is not None else "",
            'tests': tests
        }, **fields)

class MethodWriter(FunctionWriter):
    """
    Writes class methods to file
    (distinct from functions since not expected to exist solo)
    """

    template = 'method.md'

    def get_template_params(self, **kwargs):
        params = super().get_template_params(**kwargs)
        meth = self.obj  # type: types.MethodType
        decorator = ""
        if isinstance(meth, classmethod):
            decorator = 'classmethod'
        elif isinstance(meth, property):
            decorator = 'property'
        elif isinstance(meth, staticmethod):
            decorator = 'staticmethod'
        if len(decorator) > 0:
            decorator = "@" + decorator + "\n"
        params['decorator'] = decorator
        return params

    def get_signature(self):
        try:
            signature = str(inspect.signature(self.obj))
        except TypeError:  # dies on properties
            signature = "(self)"
        return signature

    @property
    def identifier(self):
        if isinstance(self.obj, property):
            return self.get_identifier(self.resolve_parent(check_tree=False)) + "." + self.get_name()
        else:
            return self.get_identifier(self.obj)

class ObjectWriter(DocObjectTemplateHandler):
    """
    Writes general objects to file.
    Basically a fallback to support singletons and things
    of that nature.
    """

    template = 'object.md'

    @property
    def identifier(self):
        try:
            qualname = self.obj.__qualname__
        except AttributeError:
            qualname = self.get_identifier(type(self.obj)) + "." + self.get_name()
        qn = qualname.split(".")
        qualname = ".".join(qn[:-2] + qn[-1:])  # want to drop the class name
        return qualname

    def check_should_write(self):
        """
        Determines whether the object really actually should be
        documented (quite permissive)
        :return:
        :rtype:
        """
        return (
                hasattr(self.obj, "__doc__")
                and hasattr(self.obj, "__name__")
                and super().check_should_write()
        )

    def get_template_params(self):

        try:
            doc = self.obj.__doc__
        except AttributeError:
            descr = "instance of " + type(self.obj).__name__
            fields = {}
        else:
            descr, _, fields = self.parse_doc(doc if doc is not None else '')

        if descr is None:
            descr = ''

        ex = self.load_examples()
        lineno = self.get_lineno()
        return dict({
            'id': self.identifier,
            'lineno': lineno,
            'name': self.get_name(),
            'description': descr.strip(),
            'examples': ex if ex is not None else "",
            'tests': None
        }, **fields)

class IndexWriter(DocTemplateHandler):
    """
    Writes an index file with all of the
    written documentation files.
    Needs some work to provide more useful info by default.
    """
    template = 'index.md'

    def __init__(self, *args, description=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = description if description is not None else "# Documentation"

    def get_identifier(cls, o):
        return 'index'

    def get_file_paths(self):
        rl = len(os.path.split(self.root))
        fs = ["/".join(os.path.split(f)[rl - 1:]) for f in self.obj]
        return fs

    # def format_item(self, f):
    #     self.formatter.format_item(
    #         self.formatter.format_link(os.path.splitext(f.split("/")[-1])[0], f)
    #     )

    def get_template_params(self):
        descr, _, fields = self.parse_doc(self.description if self.description is not None else '')
        return dict({
            'index_files': [[os.path.splitext(os.path.basename(f))[0], f] for f in self.get_file_paths()],
            'description': descr,
            'examples': self.load_examples()
        }, **fields)

class DocWalker(TemplateWalker):
    """
    A class that walks a module structure, generating `.md` files for every class inside it as well as for global functions,
    and a Markdown index file.

    Takes a set of objects & writers and walks through the objects, generating files on the way.

    :details: A `DocWalker` object is a light subclass of a `TemplateWalker`, but specialized for documentation & with specialized handlers
    :related: .DocsBuilder.DocBuilder, ModuleWriter, ClassWriter, FunctionWriter, MethodWriter, ObjectWriter, IndexWriter
    """

    module_handler = ModuleWriter
    class_handler = ClassWriter
    function_handler = FunctionWriter
    method_handler = MethodWriter
    object_handler = ObjectWriter
    index_handler = IndexWriter
    spec = DocSpec
    def __init__(self,
                 out=None,
                 engine=None,
                 verbose=True,
                 template_locator=None,
                 examples_directory=None,
                 tests_directory=None,
                 **extra_fields
                 ):
        """
        :param objects: the objects to write out
        :type objects: Iterable[Any]
        :param out: the directory in which to write the files (`None` means `sys.stdout`)
        :type out: None | str
        :param out: the directory in which to write the files (`None` means `sys.stdout`)
        :type out: None | str
        :param: writers
        :type: DispatchTable
        :param ignore_paths: a set of paths not to write (passed to the objects)
        :type ignore_paths: None | Iterable[str]
        """

        if engine is None:
            engine = self.get_engine(template_locator)
        self.examples_loader = self.get_examples_loader(examples_directory)
        self.tests_loader = self.get_tests_loader(tests_directory)
        self.verbose = verbose

        super().__init__(engine, out=out, **extra_fields)

    def get_engine(self, locator):
        if not isinstance(locator, TemplateEngine):
            locator = TemplateEngine(locator, template_pattern="*.md", formatter_class=MarkdownTemplateFormatter)
        return locator
    def get_examples_loader(self, examples_directory):
        examples_loader = examples_directory
        if examples_loader is not None and not isinstance(examples_loader, ExamplesExtractor):
            examples_loader = ExamplesExtractor(examples_loader)
        return examples_loader
    def get_tests_loader(self, tests_directory):
        tests_loader = tests_directory
        if tests_loader is not None and not isinstance(tests_loader, TestsExtractor):
            tests_loader = TestsExtractor(tests_loader)
        return tests_loader
    def get_handler(self, *args, examples_loader=None, tests_loader=None, **kwargs):
        return super().get_handler(
            *args,
            examples_loader=self.examples_loader if examples_loader is None else examples_loader,
            tests_loader=self.tests_loader if tests_loader is None else tests_loader,
            **kwargs
        )

    def visit_root(self, o, tests_directory=None, examples_directory=None, **kwargs):
        if tests_directory is None and isinstance(o, dict):
            tests_directory = o.get('tests_directory', None)
        old_tl = self.tests_loader
        if tests_directory is not None:
            self.tests_loader = self.get_tests_loader(tests_directory)
        if examples_directory is None and isinstance(o, dict):
            examples_directory = o.get('examples_directory', None)
        old_el = self.examples_loader
        if examples_directory is not None:
            self.examples_loader = self.get_examples_loader(examples_directory)
        try:
            return super().visit_root(o, **kwargs)
        finally:
            self.tests_loader = old_tl
            self.examples_loader = old_el


