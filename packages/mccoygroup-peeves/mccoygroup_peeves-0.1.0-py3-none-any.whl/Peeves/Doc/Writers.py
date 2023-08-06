"""
Implements a set of writer classes that document python objects
"""
import abc, os, sys, inspect, re, importlib, types
from collections import deque, defaultdict
from .TemplateEngine import ModuleTemplateHandler, ClassTemplateHandler
from .ExamplesParser import TestExamplesFormatter, ExamplesParser

__all__ = [
    "ModuleWriter",
    "ClassWriter",
    "FunctionWriter",
    "MethodWriter",
    "ObjectWriter",
    "IndexWriter"
]



class DocWriter(TemplateH):
    """
    A general writer class that writes a file based off a template and filling in object template specs

    :details: `DocWriter` objects are intended to do two things
     1. they manage the parsing logic to extract documentable parameters from objects
     2. they manage the process of loading the appropriate template and inserting the parameters
    This double-duty nature is likely to change in a future version of the package, being delegated to two
    subobjects that the writer then uses
    """

    template = "No template ;_;"
    template_root = "templates"
    template_name = ""
    default_template_base = os.path.dirname(__file__)
    examples_header = "## Examples"
    default_examples_root = "examples"
    default_tests_root = "tests"
    _template_cache = {}
    details_header = "## Details"
    preformat_field_handlers = {
        'examples': lambda ex,self=None:self.collapse_wrap_if_repo(self.examples_header, ex, include_opener=False) if (ex is not None and len(ex) > 0) else "",
        'details': lambda ex,self=None:self.collapse_wrap_if_repo(self.details_header, ex, open=False) if (ex is not None and len(ex) > 0) else "",
        'related': lambda objs,self=None:self.format_related_blob(objs)
    }
    protected_fields = {'id'}
    default_fields = {'details':"", "related":[]}
    def __init__(self,
                 obj,
                 out_file,
                 tree=None,

                 name=None,
                 parent=None,
                 spec=None, # extra parameters that can be used to get special behavior

                 template_directory=None,
                 examples_directory=None,
                 parent_tests=None,

                 template=None,
                 root=None,
                 ignore_paths=None,
                 examples=None,
                 tests=None,
                 formatter=None,
                 include_line_numbers=True,
                 include_link_bars=True,

                 extra_fields=None,
                 preformat_field_handlers=None,
                 ignore_missing=False,
                 strip_undocumented=False,
                 **ext
                 ):
        """
        :param obj: object to write
        :type obj:
        :param out_file: file to write to
        :type out_file: str | None
        :param tree: tree of written docs for looking stuff up
        :type tree:
        :param name: name to be used in the docs
        :type name:
        :param parent: parent object for docs purposes
        :type parent:
        :param spec: extra parameters that are usually inherited from the parent writer
        :type spec: dict | None
        :param template: template string to use when generating files
        :type template: str | None
        :param root: root directory to build off of
        :type root: str | None
        :param ignore_paths: paths to never write
        :type ignore_paths: Iterable[str]
        :param examples: path to examples to load
        :type examples: str | None
        :param tests: path to tests to load
        :type tests: str | None
        :param formatter: object that can format the stuff that Markdown supports
        :type formatter:
        """

        self.obj = obj
        self._id = None
        self._name = name
        self._parent = parent
        self._pobj = None
        self._chobj = None
        if extra_fields is None:
            extra_fields = {}
        self.extra_fields = dict(dict(self.default_fields, **ext), **extra_fields)

        self.tree = tree

        if out_file is None:
            out_file = sys.stdout
        elif isinstance(out_file, str) and os.path.isdir(out_file):
            if root is None:
                root = out_file
            out_file = os.path.join(root, *self.identifier.split("."))+".md"
        self.ignore_paths = ignore_paths if ignore_paths is not None else set()

        self.spec = {} if spec is None else spec
        self.extra_fields = dict(self.spec, **self.extra_fields)
        for k in self.extra_fields.keys() & set(self.protected_fields):
            del self.extra_fields[k]

        self.target = out_file
        if root is None:
            root = os.path.dirname(self.target)
        self.root = root

        self.fallback_template_root = 'repo_templates' if 'gh_repo' in self.extra_fields else 'templates'
        self.default_template_dir = os.path.join(self.default_template_base, self.fallback_template_root)
        self._templ_directory = (
                                    template_directory if isinstance(template_directory, str)
                                                          and os.path.isdir(template_directory) else None
        )
        self._exmpl_directory = examples_directory if isinstance(examples_directory, str) and os.path.isdir(examples_directory) else None

        self.template = self.find_template(template)
        self.examples_root = self.default_examples_root if examples is None else examples
        self.tests_root = self.default_tests_root if tests is None else tests
        self._tests = None
        self.include_line_numbers = include_line_numbers
        self.parent_tests = parent_tests

        self.include_link_bars = include_link_bars
        if preformat_field_handlers is not None:
            self.preformat_field_handlers = dict(self.preformat_field_handlers, **preformat_field_handlers)
        self.ignore_missing = ignore_missing
        self.strip_undocumented = strip_undocumented
        if strip_undocumented:
            raise NotImplementedError("currently no support for ignoring undocumented objects")
        self.formatter = MarkdownFormatter() if formatter is None else formatter

    def _clean_doc(self, doc):
        """
        Originally did a bunch of work. Now just an alias for `inspect.cleandoc`

        :param doc: a docstring
        :type doc: str
        :return: a cleaned docstring
        :rtype: str
        """
        return inspect.cleandoc(doc)

    @property
    def package_path(self):
        return self.get_package_and_url()

    @classmethod
    def load_template(cls, file):
        """
        Loads the documentation template
        for the object being documented

        :param file:
        :type file:
        :return:
        :rtype:
        """
        with open(file) as f:
            return f.read()

    def get_lineno(self):
        try:
            lineno = 1+inspect.findsource(self.obj)[1] if self.include_line_numbers else ""
        except:
            lineno = ""
        return lineno

    def resource_dir(self, spec_key, base_root):
        """
        Returns the directory for a given resource (e.g. examples or tests)
        by trying a number of different possible locations

        :param spec_key:
        :type spec_key:
        :param base_root:
        :type base_root:
        :return:
        :rtype:
        """
        if spec_key in self.spec:
            return os.path.abspath(self.spec[spec_key])
        elif os.path.isdir(os.path.abspath(base_root)):
            return base_root
        else:
            # try to inherit from the parent
            if (
                    self.tree is not None
                    and self._parent is not None
                    and self._parent in self.tree
            ):
                spec = self.tree[self._parent]
            else:
                spec = {}
            if spec_key in spec:
                return os.path.abspath(spec[spec_key])
            else:
                return os.path.join(self.root, base_root)

    def _find_template_by_name(self, name):
        test_dirs = []
        tdir = self.template_dir
        template = os.path.join(tdir, *self.identifier.split(".")) + ".md"
        if not os.path.exists(template):
            test_dirs.append(os.path.join(tdir, *self.identifier.split(".")))
            template = os.path.join(tdir, name)
        if not os.path.exists(template):
            test_dirs.append(tdir)
            def_dir = os.path.join(self.root, self.template_root)
            if not os.path.isdir(def_dir):
                def_dir = self.default_template_dir
            template = os.path.join(def_dir, name)
            if not os.path.isfile(template):
                test_dirs.append(def_dir)
                template = os.path.join(self.default_template_dir, name)
            # if os.path.isfile(template):
            #     print("no template found in {} for {}, using default".format(tdir, self.template_name))
        if os.path.exists(template):
            if template in self._template_cache:
                template = self._template_cache[template]
            else:
                tkey = template
                with open(template) as tf:
                    template = tf.read()
                self._template_cache[tkey] = template
        else:
            test_dirs.append(self.default_template_dir)
            print("no template found in {} for {}".format(test_dirs, name))
            template = self.template
        return template
    def find_template(self, template):
        """
        Finds the appropriate template for the object by looking
        in a variety of different locations

        :param template:
        :type template:
        :return:
        :rtype:
        """
        if template is None:
            template = self._find_template_by_name(self.template_name)
        elif (
            len(template.splitlines()) == 1 and
            len(os.path.split(template)) == 2
        ):
            template = self._find_template_by_name(template)

        return template

    @property
    def template_dir(self):
        if self._templ_directory is not None:
            return self._templ_directory
        elif os.path.isdir(os.path.join(self.root, self.template_root)):
            return os.path.join(self.root, self.template_root)
        else:
            return self.default_template_dir

    @property
    def examples_dir(self):
        """
        Returns the directory in which to look for examples
        :return:
        :rtype:
        """
        spec_key='examples_root'
        if self._exmpl_directory is None:
            return self.resource_dir(spec_key, self.examples_root)
        else:
            return self._exmpl_directory

    @property
    def examples_path(self):
        """
        Provides the default examples path for the object
        :return:
        :rtype:
        """
        splits = self.identifier.split(".")
        return os.path.join(*splits)+".md"
    def load_examples(self):
        """
        Loads examples for the stored object if provided
        :return:
        :rtype:
        """
        if hasattr(self.obj, '__examples__'):
            examples = os.path.join(self.examples_dir, self.obj.__examples__)
            if os.path.isfile(examples):
                with open(examples) as f:
                    return f.read()
            else:
                return self.obj.__examples__
        elif self.root is not None:
            examples = os.path.join(self.examples_dir, self.examples_path)
            if os.path.isfile(examples):
                with open(examples) as f:
                    return f.read()

    @property
    def tests_dir(self):
        """
        Returns the directory in which to look for tests
        :return:
        :rtype:
        """
        spec_key='tests_root'
        return self.resource_dir(spec_key, self.tests_root)
    @property
    def tests_path(self):
        """
        Provides the default tests path for the object
        :return:
        :rtype:
        """
        return os.path.join(*self.identifier.split(".")) + "Tests.py"
    def load_tests(self):
        """
        Loads tests for the stored object if provided
        :return:
        :rtype:
        """

        # print(">>>>", self.tests_dir, self.tests_path)
        test_str = None
        if hasattr(self.obj, '__tests__'):
            tests = os.path.join(self.tests_dir, self.obj.__tests__)
            if os.path.isfile(tests):
                with open(tests) as f:
                    test_str = f.read()
            else:
                test_str = self.obj.__tests__
        elif self.root is not None:
            tests = os.path.join(self.tests_dir, self.tests_path)
            if os.path.isfile(tests):
                with open(tests) as f:
                    test_str = f.read()
            else:
                tests = os.path.join(self.tests_dir, os.path.basename(self.tests_path))
                # print("....", tests)
                if os.path.isfile(tests):
                    with open(tests) as f:
                        test_str = f.read()

        return ExamplesParser(test_str) if test_str is not None else test_str
    @property
    def tests(self):
        if self._tests is None:
            self._tests = self.load_tests()
        return self._tests
    def get_test_markdown(self):
        tests = self.tests
        if tests is None and self.parent_tests is not None:
            tests = self.parent_tests.filter_by_name(self.name.split(".")[-1])

        formatted = TestExamplesFormatter(tests,
                                          template=self.find_template('tests.md'),
                                          example_template=self.find_template('test_example.md'),
                                          ).format() if tests is not None else ""
        # print(self.name, len(formatted))
        return formatted



    param_template = """  - `{name}`: `{type}`\n    >{description}"""
    def parse_doc(self, doc):
        """

        :param doc:
        :type doc: str
        :return:
        :rtype:
        """

        # parses a docstring based on reStructured text type specs but Markdown description
        splits = inspect.cleandoc(doc.strip()).splitlines()

        params = deque()
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
                        param_map[name] = {"name":name, "type":"Any", "description":[]}
                    desc = bits[1].strip() if len(bits) == 2 else ""
                    if len(desc) > 0:
                        param_map[name]["description"].append(desc)
                elif line.startswith(":type"):
                    bits = line.split(":", 2)[1:]
                    name = bits[0][4:].strip()
                    active_tag = name
                    if name not in param_map:
                        params.appendleft(name)
                        param_map[name] = {"name":name, "type":"Any", "description":[]}
                    t = bits[1].strip() if len(bits) == 2 else ""
                    if len(t) > 0:
                        param_map[name]["type"] = t
                elif line.startswith(":return"):
                    bits = line.split(":", 2)[1:]
                    name = ":returns"
                    active_tag = name
                    if name not in param_map:
                        params.appendleft(name)
                        param_map[name] = {"name":name, "type":"_", "description":[]}
                    t = bits[1].strip() if len(bits) == 2 else ""
                    if len(t) > 0:
                        param_map[name]["description"] = t
                elif line.startswith(":rtype"):
                    bits = line.split(":", 2)[1:]
                    name = ":returns"
                    active_tag = name
                    if name not in param_map:
                        params.appendleft(name)
                        param_map[name] = {"name":name, "type":"_", "description":[]}
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
        for k,v in extra_fields.items():
            extra_fields[k] = "\n".join(v)

        param = []
        for p in params:
            param.append(
                self.param_template.format(**param_map[p]).strip()
            )

        return "\n".join(param), "\n".join(description), extra_fields

    def collapse_wrap_if_repo(self, header, content, name=None, open=True, include_opener=True):
        if 'gh_repo' in self.extra_fields:
            return self.formatter.format_collapse_section(header, content, name=name, open=open, include_opener=include_opener)
        else:
            return header + "\n" + content

    def resolve_object_url(self, o):
        obj = self.resolve_object(o)
        path = DocWriter.get_identifier(obj).split('.')
        return self.formatter.format_link(path[-1], "/".join(path)+".md")
    def format_related_blob(self, related):
        links = [self.resolve_object_url(o) for o in related]
        joiner = '<a>#9642;</a>'
        header = "### See Also: "
        return header + joiner.join(links)

class ModuleWriter(DocWriter):
    """A writer targeted to a module object. Just needs to write the Module metadata."""

    template_name = 'module.md'
    def __init__(self, obj, out_file, **kwargs):
        if isinstance(obj, str):
            obj = importlib.import_module(obj)
        super().__init__(obj, out_file, **kwargs)

    def get_template_params(self):
        """
        Provides module specific parameters
        :return:
        :rtype:
        """

        mod = self.obj # type: types.ModuleType
        name = mod.__name__
        ident = self.identifier
        ident_depth = len(ident.split("."))
        # get identifiers
        idents = [ DocWriter.get_identifier(getattr(mod, a)) for a in self.get_members(mod) ]
        # flattend them
        idents = [ i for i in idents if ident in i ]
        # split by qualified names
        # idents = [".".join(a.split(".")[ident_depth-1:]) for a in idents]
        # # format links
        # links = [ self.formatter.format_obj_link(l) for l in idents ]
        # if self.include_link_bars:
        #     num_cols = 3
        #     splits = []
        #     sub = []
        #     for x in links:
        #         sub.append(x)
        #         if len(sub) == num_cols:
        #             splits.append(sub)
        #             sub = []
        #     splits.append(sub + [""] * (3 - len(sub)))
        #     mems = self.formatter.format_grid_box(splits)
        # else:
        #     mems = "\n".join([ self.formatter.format_item(l) for l in links ])
        descr = mod.__doc__ if mod.__doc__ is not None else ''
        long_descr = mod.__long_doc__ if hasattr(mod, '__long_doc__') and mod.__long_doc__ is not None else ''

        ex = self.load_examples()
        tests = self.get_test_markdown()
        return {
            'id' : ident,
            'description' : descr.strip(),
            'long_description' : long_descr.strip(),
            'name': name,
            'members' : idents,
            'examples' : ex,
            'tests': tests
        }

    @classmethod
    def get_members(cls, mod):
        return (mod.__all__ if hasattr(mod, '__all__') else [])

class ClassWriter(DocWriter):
    """A writer targeted to a class"""

    template_name = 'class.md'
    def load_methods(self, function_writer=None):
        """
        Loads the methods supported by the class

        :param function_writer:
        :type function_writer:
        :return:
        :rtype:
        """

        if function_writer is None:
            function_writer = MethodWriter

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
                        function_writer(o,
                                        tree=self.tree, parent=self.identifier, name=k,
                                        out_file=None, root=self.root,
                                        template_directory=self.template_dir,
                                        examples_directory=self.examples_dir,
                                        extra_fields=extra_fields
                                        ).format().strip()
                    )
            else:
                if not k.startswith("_"):
                    props.append(self.format_prop(k, o).strip())

        return props, methods

    def get_package_and_url(self):
        pkg, rest = self.identifier.split(".", 1)
        rest, bleh = rest.rsplit(".", 1)
        file_url = rest.replace(".", "/") + ".py"
        if 'url_base' in self.extra_fields:
            file_url = self.extra_fields['url_base'] + "/" + file_url
        # lineno = inspect.findsource(self.obj)[1]
        return pkg, file_url #+ "#L" + str(lineno) # for GitHub links

    def format_prop(self, k, o):
        return '{}: {}'.format(k, type(o).__name__)

    def get_template_params(self, function_writer = None):
        """

        :param function_writer:
        :type function_writer:
        :return:
        :rtype:
        """

        cls = self.obj # type: type
        ex = self.load_examples()
        tests = self.get_test_markdown()
        name = cls.__name__
        ident = self.identifier
        props, methods = self.load_methods(function_writer=function_writer)
        param, descr, fields = self.parse_doc(cls.__doc__ if cls.__doc__ is not None else '')
        descr = self._clean_doc(descr)
        param = self._clean_doc(param)
        if len(param) > 0:
            param = "\n" + param
        props = "\n".join(props)
        if len(props) > 0:
            props = self.formatter.format_code_block(props)+"\n"
        lineno = self.get_lineno()

        return dict({
            'id': ident,
            'name': name,
            'lineno': lineno,
            'description' : descr,
            'parameters' : param,
            'props' : props,
            'methods' : "\n\n".join(methods),
            'examples' : ex if ex is not None else "",
            'tests': tests
        }, **fields)

class FunctionWriter(DocWriter):
    """
    Writer to dump functions to file
    """

    template_name = 'function.md'
    def get_signature(self):
        return str(inspect.signature(self.obj))
    def get_template_params(self, **kwargs):
        f = self.obj # type: types.FunctionType
        ident = self.identifier
        signature = self.get_signature()
        mem_obj_pat = re.compile(" object at \w+>")
        signature = re.sub(mem_obj_pat, " instance>", signature)
        name = self.get_name()
        param, descr, fields = self.parse_doc(f.__doc__ if f.__doc__ is not None else '')
        descr = descr.strip()
        param = param.strip()
        if len(param) > 0:
            param = "\n" + param
        ex = self.load_examples()
        tests = self.get_test_markdown()
        lineno = self.get_lineno()
        return dict({
            'id': ident,
            'name' : name,
            'lineno' : lineno,
            'signature' : signature,
            'parameters' : param,
            'description' : descr,
            'examples' : ex if ex is not None else "",
            'tests': tests
        }, **fields)

    def get_package_and_url(self):
        pkg, rest = self.identifier.split(".", 1)
        rest, bleh = rest.rsplit(".", 1)
        file_url = rest.replace(".", "/") + ".py"
        if 'url_base' in self.extra_fields:
            file_url = self.extra_fields['url_base'] + "/" + file_url
        # lineno = inspect.findsource(self.obj)[1]
        return pkg, file_url #+ "#L" + str(lineno) # for GitHub links

class MethodWriter(FunctionWriter):
    """
    Writes class methods to file
    (distinct from functions since not expected to exist solo)
    """

    template_name = 'method.md'
    def get_template_params(self, **kwargs):
        params = super().get_template_params(**kwargs)
        meth = self.obj # type: types.MethodType
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

class ObjectWriter(DocWriter):
    """
    Writes general objects to file.
    Basically a fallback to support singletons and things
    of that nature.
    """

    template_name = 'object.md'
    @property
    def identifier(self):
        try:
            qualname = self.obj.__qualname__
        except AttributeError:
            qualname = self.get_identifier(type(self.obj)) + "." + self.get_name()
        qn = qualname.split(".")
        qualname = ".".join(qn[:-2] + qn[-1:]) # want to drop the class name
        # print(qualname)
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
            descr = self.obj.__doc__
        except AttributeError:
            descr = "instance of "+type(self.obj).__name__

        if descr is None:
            descr = ''

        ex = self.load_examples()
        lineno = self.get_lineno()
        return {
            'id': self.identifier,
            'lineno': lineno,
            'name': self.get_name(),
            'description' : descr.strip(),
            'examples' : ex if ex is not None else ""
        }

class IndexWriter(DocWriter):
    """
    Writes an index file with all of the
    written documentation files.
    Needs some work to provide more useful info by default.
    """

    template_name = 'index.md'
    def __init__(self, *args, description=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = description if description is not None else "# Documentation"

    def get_identifier(cls, o):
        return 'index'

    def get_file_paths(self):
        rl = len(os.path.split(self.root))
        fs = [ "/".join(os.path.split(f)[rl-1:]) for f in self.obj ]
        return fs

    def get_template_params(self):
        files = [
            self.formatter.format_item(
                self.formatter.format_link(os.path.splitext(f.split("/")[-1])[0], f)
            ) for f in self.get_file_paths()
        ]
        return {
            'index_files' : "\n".join(files),
            'description' : self.description
        }