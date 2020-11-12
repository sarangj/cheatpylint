import argparse
import dataclasses
import json
import typing

import libcst
import pylint.epylint


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--l', dest='lint', required=True)
    parser.add_argument('--f', dest='src_file', required=True)
    run_annotater(parser.lint, parser.src_file)


def run_annotater(lint_arg: str, src_file_arg: str):
    pylint_stdout, pylint_stderr = pylint.epylint.py_run(
        command_options=(
            f'{src_file_arg} '
            f'--disable=all --enable {lint_arg} '
            '--output-format=json'
        ),
        return_std=True,
    )
    lints = [Lint.from_dict(d) for d in json.load(pylint_stdout)]
    if lint_arg == 'too-many-arguments':
        transformer = DisableTooManyArgs(lints)
    elif lint_arg == 'too-many-instance-attributes':
        transformer = DisableTooManyInstanceAttributes(lints)
    else:
        raise ValueError

    with open(src_file_arg, 'r') as f:
        src = f.read()

    src_tree = libcst.parse_module(src)
    modified_tree = src_tree.visit(transformer)

    with open(src_file_arg, 'w') as f:
        f.write(modified_tree.code)


@dataclasses.dataclass
class Lint:

    type: str
    module: str
    obj: str
    line: int
    column: int
    path: str
    symbol: str
    message: str
    message_id: str

    @classmethod
    def from_dict(cls, d: dict) -> 'Lint':
        if 'message-id' in d:
            message_id = d['message-id']
            d = d.copy()
            d['message_id'] = message_id
            del d['message-id']

        return cls(**d)


class DisableTooManyArgs(libcst.CSTTransformer):

    def __init__(self, lints: typing.Iterable[Lint]):
        self.functions = set(
            lint.obj for lint in lints
            if lint.symbol == 'too-many-arguments'
        )
        self.class_stack: typing.List[str] = []

    def visit_ClassDef(self, node: libcst.ClassDef) -> typing.Optional[bool]:
        self.class_stack.append(node.name.value)

    def leave_ClassDef(
        self,
        original_node: libcst.ClassDef,
        updated_node: libcst.ClassDef,
    ) -> libcst.CSTNode:
        self.class_stack.pop()
        return updated_node

    def leave_FunctionDef(
        self,
        original_node: libcst.FunctionDef,
        updated_node: libcst.FunctionDef,
    ) -> libcst.CSTNode:
        full_name = (
            f'{self.class_stack[0]}.{original_node.name.value}'
            if self.class_stack
            else original_node.name.value
        )
        if full_name in self.functions:
            return updated_node.with_changes(
                lines_after_decorators=[
                    *original_node.lines_after_decorators,
                    libcst.EmptyLine(
                        comment=libcst.Comment('# pylint: disable=too-many-arguments'),
                    ),
                ],
                body=original_node.body.with_changes(
                    body=[
                        *original_node.body.body,
                        libcst.EmptyLine(
                            comment=libcst.Comment('# pylint: enable=too-many-arguments'),
                        ),
                    ],
                ),
            )

        return updated_node


class DisableTooManyInstanceAttributes(libcst.CSTTransformer):

    def __init__(self, lints: typing.Iterable[Lint]):
        self.classes = set(
            lint.obj for lint in lints
            if lint.symbol == 'too-many-instance-attributes'
        )
        self.class_stack: typing.List[str] = []

    def visit_ClassDef(self, node: libcst.ClassDef) -> typing.Optional[bool]:
        self.class_stack.append(node.name.value)

    def leave_ClassDef(
        self,
        original_node: libcst.ClassDef,
        updated_node: libcst.ClassDef,
    ) -> libcst.CSTNode:
        full_class_name = '.'.join(self.class_stack[::-1])
        self.class_stack.pop()
        if full_class_name in self.classes:
            return updated_node.with_changes(
                lines_after_decorators=[
                    *original_node.lines_after_decorators,
                    libcst.EmptyLine(
                        comment=libcst.Comment('# pylint: disable=too-many-instance-attributes'),
                    ),
                ],
                body=original_node.body.with_changes(
                    body=[
                        *original_node.body.body,
                        libcst.EmptyLine(
                            comment=libcst.Comment('# pylint: enable=too-many-instance-attributes'),
                        ),
                    ],
                ),
            )

        return updated_node


if __name__ == '__main__':
    main()
