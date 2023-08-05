from enum import IntEnum
from typing import Any, Optional

from docutils.statemachine import StringList

from sphinx.application import Sphinx
from sphinx.ext.autodoc import FunctionDocumenter, ModuleDocumenter, bool_option
from sphinx.util import inspect

import logging

class TestDocumenter(FunctionDocumenter):
    objtype = 'test'
    directivetype = FunctionDocumenter.objtype
    priority = 10 + FunctionDocumenter.priority
    option_spec = dict(FunctionDocumenter.option_spec)

    @classmethod
    def can_document_member(cls,
                            member: Any, membername: str,
                            isattr: bool, parent: Any) -> bool:
        if FunctionDocumenter.can_document_member( member, membername,
                isattr, parent ):
            logging.debug( "TestDocumenter: {} {}".format(member,membername) )
            if membername.startswith('test_'):
                return True
        return False

    def add_directive_header(self, sig: str) -> None:
        """Add the directive header and options to the generated content."""
        domain = 'test'
        directive = 'test'
        name = self.format_name()
        sourcename = self.get_sourcename()

        # one signature per line, indented by column
        prefix = '.. %s:%s:: ' % (domain, directive)
        for i, sig_line in enumerate(sig.split("\n")):
            if name.startswith('test_'):
                name = name[5:]
            self.add_line('%s%s%s' % (prefix, name, sig_line),
                          sourcename)
            if i == 0:
                prefix = " " * len(prefix)

    def add_content(self,
                    more_content: Optional[StringList],
                    no_docstring: bool = False
                    ) -> None:

        if 'pytestmark' in dir(self.object):
            stext = ":suite: "
            first_s = True
            for mark in self.object.pytestmark:
                if not first_s:
                    stext += ','
                stext += mark.name
                first_s = False
            self.add_line( stext, self.get_sourcename() )

        super().add_content(more_content)


def setup(app: Sphinx) -> None:
    app.setup_extension('sphinx.ext.autodoc')  # Require autodoc extension
    app.add_autodocumenter(TestDocumenter)
