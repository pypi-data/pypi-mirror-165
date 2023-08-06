import sys
from typing import Callable, Type, Union, Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from mapping_shortcuts.utils import first, parse_args, get_arg_types

from . import consts

CliHandler = Union[Callable[[BaseModel], None], Callable[[dict[str, Union[str, bool]]], None]]


class Cmd(BaseModel):
    cmd: str
    desc: str
    func: CliHandler
    model: Optional[Type[BaseModel]] = None

    def __hash__(self) -> int:
        return hash(self.cmd)


CMD_HANDLERS = {}  # type: dict[str, Cmd]


def cli_handler(
    cmd: str,
    *,
    desc: str = '',
    model: Optional[Type[BaseModel]] = None,
) -> Callable[[CliHandler], CliHandler]:
    def decor(func: CliHandler) -> CliHandler:
        nonlocal model
        if not model:
            possible_model = first(get_arg_types(func))  # type: Optional[Type[BaseModel]]
            if possible_model:
                if BaseModel in possible_model.__mro__:
                    model = possible_model
        if cmd in CMD_HANDLERS:
            raise RuntimeError(f'key duplication for "{cmd}"')
        CMD_HANDLERS[cmd] = Cmd(cmd=cmd, desc=desc, func=func, model=model)
        return func
    return decor


def run_args(args: list[str]) -> None:
    raw_params = parse_args(args)

    if {'-h', '-?', '--help'} & set(raw_params):
        cmd = 'help'
    else:
        cmd = first(i for i in args if not i.startswith('-')) or 'help'
        if cmd not in CMD_HANDLERS:
            raise ValueError(f'unknown cmd: {cmd}')

    handler = CMD_HANDLERS[cmd]
    if handler.model:
        validated_args = handler.model(**raw_params)
        handler.func(validated_args)  # type: ignore[call-arg]
    else:
        handler.func(raw_params)  # type: ignore[call-arg]


def process_sysargv(
    args: Optional[list[str]] = None,
    help_msg_header: Optional[str] = None,
    help_msg_run_cmd: Optional[str] = None,
    help_msg_template: Optional[str] = None,
) -> None:
    args = args or sys.argv

    if help_msg_header:
        consts.HELP_MSG_TEMPLATE_HEADER = help_msg_header
    if help_msg_run_cmd:
        consts.HELP_MSG_RUN_CMD = help_msg_run_cmd
    if help_msg_template:
        consts.HELP_TEMPLATE = help_msg_template

    run_args(args[1:])
