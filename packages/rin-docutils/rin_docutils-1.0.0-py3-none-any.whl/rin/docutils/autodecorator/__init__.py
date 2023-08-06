import os.path
from typing import Any, Dict

import sphinx.ext.autosummary.generate
from sphinx.application import Sphinx
from sphinx.ext.autodoc import FunctionDocumenter, ClassDocumenter, DecoratorDocumenter

from .. import __version__
from ._modified_generate_autosummary_content import modified_generate_autosummary_content

try:
    import sphinx_toolbox

    has_sphinx_toolbox = True
except ImportError:
    has_sphinx_toolbox = False


class PatchedFunctionDocumenter(FunctionDocumenter):
    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        return (not getattr(member, "__is_decorator__", False) and
                super().can_document_member(member, membername, isattr, parent))


if has_sphinx_toolbox:
    from sphinx_toolbox.more_autosummary import PatchedAutoSummClassDocumenter


    class PatchedSphinxToolboxClassDocumenter(PatchedAutoSummClassDocumenter):
        @classmethod
        def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
            return (not getattr(member, "__is_decorator__", False) and
                    super().can_document_member(member, membername, isattr, parent))


class PatchedClassDocumenter(ClassDocumenter):
    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        return (not getattr(member, "__is_decorator__", False) and
                super().can_document_member(member, membername, isattr, parent))


class PatchedDecoratorDocumenter(DecoratorDocumenter):

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        return (
                getattr(member, "__is_decorator__", False) and
                (super().can_document_member(member, membername, isattr, parent) or hasattr(member, "__get__"))
        )


def setup(app: Sphinx) -> Dict[str, Any]:
    """
    Setup :mod:`rin.docutils.autodecorator`.

    :param app: The Sphinx application.
    """

    app.setup_extension("sphinx.ext.autodoc")
    sphinx.ext.autosummary.generate.generate_autosummary_content = modified_generate_autosummary_content
    app.config.init_values()
    app.config.templates_path.append(os.path.abspath(os.path.join(__file__, "..", "templates")))
    app.setup_extension("sphinx.ext.autosummary")

    use_sphinx_toolbox = "sphinx_toolbox.more_autosummary" in app.extensions
    if use_sphinx_toolbox:
        app.setup_extension("sphinx_toolbox.more_autosummary")

    app.add_autodocumenter(PatchedFunctionDocumenter, override=True)
    if use_sphinx_toolbox:
        app.add_autodocumenter(PatchedSphinxToolboxClassDocumenter, override=True)
    else:
        app.add_autodocumenter(PatchedClassDocumenter, override=True)
    app.add_autodocumenter(PatchedDecoratorDocumenter, override=True)

    return {"version": __version__, "parallel_read_safe": True}
