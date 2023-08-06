import inspect
import traceback
from termcolor import cprint
from executing import Source


def _colored_print(variable, c, b, a, p, lineno, filename):
    if b:
        if p:
            cprint(f'~ {variable} :: line {lineno} :: file {filename}', c, b, attrs=[a])
        else:
            cprint(f'~ {variable} :: line {lineno}', c, b, attrs=[a])
    else:
        if p:
            cprint(f'~ {variable} :: line {lineno} :: file {filename}', c, attrs=[a])
        else:
            cprint(f'~ {variable} :: line {lineno}', c, attrs=[a])


def sprint(*args, c="white", b="", a="bold", s=False, p=False, r=False, **kwargs):

    # с ~ colors: grey, red, green, yellow, blue, magenta, cyan, white
    # b ~ backgrounds: on_grey, on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan
    # a ~ attributes: bold, dark, underline, blink, reverse, concealed
    # s ~ as string: print strings
    # p ~ path: show path to file    
    # r ~ raw: return value as string

    stack = traceback.extract_stack()
    filename, lineno, function_name, code = stack[-2]
    call_frame = inspect.currentframe().f_back
    call_node = Source.executing(call_frame).node
    source = Source.for_frame(call_frame)

    var_names = []
    for i in range(len(args)):
        try:
            var_names.append(source.asttokens().get_text(call_node.args[i]))
        except:
            continue

    if r:
        raw_string = []

    for i, arg in enumerate(args):

        try:
            var_name = var_names[i]
            if isinstance(arg, str) or s:
                variable = f"{arg}"
            else:
                variable = f"{var_name} = {arg}"
        except:
            if isinstance(arg, str) or s:
                variable = f"{arg}"
            else:
                variable = f"{arg} = {arg}"

        if r:
            if p:
                raw_string.append(f'~ {variable} :: line {lineno} :: file {filename}')
            else:
                raw_string.append(f'~ {variable} :: line {lineno}')
        else:
            _colored_print(variable, c, b, a, p, lineno, filename)
    
    if r:
        return '; '.join(raw_string)


def sprint_f(*args, **kwargs):
    # back compatibility for early versions
    return sprint(*args, **kwargs)