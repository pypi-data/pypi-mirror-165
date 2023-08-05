from collections import defaultdict

from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, Index
from sphinx.roles import XRefRole
from sphinx.util.nodes import make_refnode

from sphinx.util.docfields import Field,GroupedField

from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Type, Union, cast
from docutils import nodes
from docutils.nodes import Node

from docutils.parsers.rst.states import Inliner
from sphinx.environment import BuildEnvironment

import logging

class EnumField(GroupedField):

    def make_field(self, types: Dict[str, List[Node]], domain: str,
                   items: Tuple, env: BuildEnvironment = None,
                   inliner: Inliner = None, location: Node = None) -> nodes.field:
        fieldname = nodes.field_name('', self.label)
        listnode = nodes.enumerated_list()
        for fieldarg, content in items:
            par = nodes.paragraph()
            par.extend(self.make_xrefs(self.rolename, domain, '',
                                       addnodes.literal_strong,
                                       env=env, inliner=inliner, location=location))
            par += content
            listnode += nodes.list_item('', par)

        if len(items) == 1 and self.can_collapse:
            list_item = cast(nodes.list_item, listnode[0])
            fieldbody = nodes.field_body('', list_item[0])
            return nodes.field('', fieldname, fieldbody)

        fieldbody = nodes.field_body('', listnode)
        return nodes.field('', fieldname, fieldbody)

class TestDirective(ObjectDescription):
    """A custom directive that describes a test."""

    has_content = True
    required_arguments = 1

    doc_field_types = [
        EnumField('steps', label='Steps',
              names=('step',), can_collapse=True),
        Field( 'reqs', label='Reqs',
              names=('reqs',), has_arg=False),
        Field( 'suite', label='Suite',
              names=('suite',), has_arg=False),
        EnumField('init', label='Init',
              names=('init','initial'), can_collapse=True),
        GroupedField('pass', label='Result', can_collapse=True,
              names=('passcrit', 'pass', 'result')),
    ]

    def handle_signature(self, sig, signode):
        signode += addnodes.desc_name(text=sig)
        return sig

    def _get_suite(self, field : str):
        suite_str = ":{}:".format(field)
        for ii in self.content.data:
            if ii.startswith(suite_str):
                return ii[len(suite_str):].strip().split(',')
        return None

    def add_target_and_index(self, name_cls, sig, signode):
        signode['ids'].append('test' + '-' + sig)

        suite = self._get_suite('suite')
        reqs = self._get_suite('reqs')
        tests = self.env.get_domain('test')
        tests.add_test(sig, reqs,suite)

    def transform_content(self, contentnode: addnodes.desc_content) -> None:
        counter = 1
        icount  = 1
        typemap = self.get_field_type_map()
        for child in contentnode:
            if isinstance(child, nodes.field_list):
                for field in cast(List[nodes.field], child):
                    if len(field) > 1:
                        field_name = cast(nodes.field_name, field[0])
                        if field_name.astext() == 'step':
                            fn_text = "step {}".format(counter)
                            field_name.replace_self( nodes.field_name(text=fn_text) )
                            counter += 1
                        if field_name.astext() == 'init':
                            fn_text = "init {}".format(icount)
                            field_name.replace_self( nodes.field_name(text=fn_text) )
                            icount += 1


class RequirementIndex(Index):
    """A custom index that creates an requirement matrix."""

    name = 'requirement'
    localname = 'Requirement Index'
    shortname = 'Requirement'

    def generate(self, docnames=None):
        content = defaultdict(list)

        tests = {name: (dispname, typ, docname, anchor)
                   for name, dispname, typ, docname, anchor, _
                   in self.domain.get_objects()}
        test_reqs = self.domain.data['test_reqs']
        requirement_tests = defaultdict(list)

        # flip from test_reqs to requirement_tests
        for test_name, reqs in test_reqs.items():
            if reqs:
                for requirement in reqs:
                    requirement_tests[requirement].append(test_name)

        # convert the mapping of requirement to tests to produce the expected
        # output, shown below, using the requirement name as a key to group
        #
        # name, subtype, docname, anchor, extra, qualifier, description
        for requirement, test_names in requirement_tests.items():
            for test_name in test_names:
                dispname, typ, docname, anchor = tests[test_name]
                content[requirement].append(
                    (dispname, 0, docname, anchor, docname, '', typ))

        # convert the dict to the sorted list of tuples expected
        content = sorted(content.items())

        return content, True

class SuiteIndex(Index):
    """A custom index that creates an suite matrix."""

    name = 'suite'
    localname = 'Suite Index'
    shortname = 'Suite'

    def generate(self, docnames=None):
        content = defaultdict(list)

        tests = {name: (dispname, typ, docname, anchor)
                   for name, dispname, typ, docname, anchor, _
                   in self.domain.get_objects()}
        test_suite = self.domain.data['test_suite']
        suite_tests = defaultdict(list)

        # flip from test_suite to suite_tests
        for test_name, suite in test_suite.items():
            for suite in suite:
                suite_tests[suite].append(test_name)

        # convert the mapping of suite to tests to produce the expected
        # output, shown below, using the suite name as a key to group
        #
        # name, subtype, docname, anchor, extra, qualifier, description
        for suite, test_names in suite_tests.items():
            for test_name in test_names:
                dispname, typ, docname, anchor = tests[test_name]
                content[suite].append(
                    (dispname, 0, docname, anchor, docname, '', typ))

        # convert the dict to the sorted list of tuples expected
        content = sorted(content.items())

        return content, True

class TestIndex(Index):
    """A custom index that creates an test matrix."""

    name = 'test'
    localname = 'Test Index'
    shortname = 'Test'

    def generate(self, docnames=None):
        content = defaultdict(list)

        # sort the list of tests in alphabetical order
        tests = self.domain.get_objects()
        tests = sorted(tests, key=lambda test: test[0])

        # generate the expected output, shown below, from the above using the
        # first letter of the test as a key to group thing
        #
        # name, subtype, docname, anchor, extra, qualifier, description
        for _name, dispname, typ, docname, anchor, _priority in tests:
            content[dispname[0].lower()].append(
                (dispname, 0, docname, anchor, docname, '', typ))

        # convert the dict to the sorted list of tuples expected
        content = sorted(content.items())

        return content, True

class TestDomain(Domain):

    name = 'test'
    label = 'Test Sample'
    roles = {
        'ref': XRefRole()
    }
    directives = {
        'test': TestDirective,
    }
    indices = {
        TestIndex,
        RequirementIndex,
        SuiteIndex
    }
    initial_data = {
        'tests': [],  # object list
        'test_reqs': {},  # name -> object
        'test_suite': {},  # name -> object
    }

    def get_full_qualified_name(self, node):
        return '{}.{}'.format('test', node.arguments[0])

    def get_objects(self):
        for obj in self.data['tests']:
            yield(obj)

    def resolve_xref(self, env, fromdocname, builder, typ, target, node,
                     contnode):
        match = [(docname, anchor)
                 for name, sig, typ, docname, anchor, prio
                 in self.get_objects() if sig == target]

        if len(match) > 0:
            todocname = match[0][0]
            targ = match[0][1]

            return make_refnode(builder, fromdocname, todocname, targ,
                                contnode, targ)
        else:
            print('Awww, found nothing')
            return None

    def add_test(self, signature, reqs,suite=None):
        """Add a new test to the domain."""
        name = '{}.{}'.format('test', signature)
        anchor = 'test-{}'.format(signature)

        self.data['test_reqs'][name] = reqs
        if suite:
            self.data['test_suite'][name] = suite
        # name, dispname, type, docname, anchor, priority
        self.data['tests'].append(
            (name, signature, 'Test', self.env.docname, anchor, 0))

def setup(app):
    app.add_domain(TestDomain)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
