"""
A simple documentation framework, similar to Sphinx.
It builds off of a template engine (provided by the `TemplateEngine` package) and an object-tree traversal
class (`TemplateWalker`) to fill out templates for the different types of python objects.
These templates are exported as Markdown so that they can be turned into a final website by a more sophisticated
Markdown -> HTML static site generator, like Jekyll.
Templates are extremely customizable (down to the object-level) with a flexible and powerful template mini-language
that builds off of python's built-in AST module and syntax.
Examples are also possible to provide for individual objects/modules and can also be harvested automatically from
unit tests if provided.

:long_description:
The templates provided are for modules, classes, methods, functions, and generic objects.
The mini-language used extends standard python string formatting syntax but allows for the
evaluation of a whitelisted set of commands within templates.
A full HTML/Bootstrap generator is included to allow for total customization of the generated
Markdown.
See `TemplateOps`, `TemplateFormatDirective`, `MarkdownOps`, and `MarkdownFormatDirective` for more info.
"""

__all__ = []
from .DocsBuilder import *; from .DocsBuilder import __all__ as exposed
__all__ += exposed
from .DocWalker import *; from .DocWalker import __all__ as exposed
__all__ += exposed
from .ExamplesParser import *; from .ExamplesParser import __all__ as exposed
__all__ += exposed
from .TemplateEngine import *; from .TemplateEngine import __all__ as exposed
__all__ += exposed