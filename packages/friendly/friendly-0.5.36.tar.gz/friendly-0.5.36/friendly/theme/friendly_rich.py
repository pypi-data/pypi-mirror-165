"""Friendly-rich

All Rich-related imports and redefinitions are done here.

"""
import inspect
import re

from .friendly_pygments import friendly_dark, friendly_light
from . import colours
from friendly_traceback.utils import get_highlighting_ranges

import rich
from rich import pretty
from rich.markdown import Heading, CodeBlock
from rich.syntax import Syntax
from rich.text import Text
from rich.theme import Theme

from pygments.token import Comment, Generic, Keyword, Name, Number, Operator, String

from friendly_traceback import token_utils

dark_background_theme = Theme(friendly_dark.friendly_style)
light_background_theme = Theme(friendly_light.friendly_style)


def is_builtin(string):
    try:
        return inspect.isbuiltin(eval(string))
    except:  # noqa
        return False


def is_exception(string):
    try:
        return issubclass(eval(string), BaseException)
    except:  # noqa
        return False


def format_with_highlight(lines, error_lines, theme):
    """Formats lines, replacing code underlined by ^^ (on the following line)
    into highlighted code, and removing the ^^ from the end result.
    """
    # As we might process line by line, the tokenization will not work
    # when multiline triple-quoted strings are included;
    # we thus exclude them from our token by token highlighting.
    contain_triple_quoted = [
        index
        for index, line in enumerate(lines)
        if token_utils.untokenize(token_utils.tokenize(line)) != line
    ]
    # We ensure that any line that might include content from a triple-quoted
    # string is not included.
    if contain_triple_quoted:
        contain_triple_quoted = list(
            range(contain_triple_quoted[0], contain_triple_quoted[-1] + 1)
        )
    result = []

    for index, line in enumerate(lines):
        if index in error_lines:  # Skip over lines containing ^^
            continue
        if index + 1 in error_lines:
            if index in contain_triple_quoted:
                result.append(
                    simple_line_highlighting(line, error_lines[index + 1], theme)
                )
            else:
                result.append(highlight_by_tokens(line, error_lines[index + 1], theme))
        elif index in contain_triple_quoted:
            result.append(simple_line_highlighting(line, [], theme))
        else:
            result.append(Syntax(line, "python", theme=theme, word_wrap=True))
    return result


def simple_line_highlighting(line, line_parts, theme):
    """Fallback method for highlighting code when there might be some
    triple quoted strings spanning multiple lines. As the highlighting
    is done a singe line at a time, any tokenization of the line content
    might fail. We thus use Rich's Text() instead of Syntax() to highlight
    different part of each line.
    """
    error_style = colours.get_highlight()

    background = theme.background_color
    operator_style = f"{theme.styles[Operator]} on {background}"
    number_style = f"{theme.styles[Number]} on {background}"
    code_style = f"{theme.styles[Name]} on {background}"

    has_line_number = re.match(r"^\s*\d+\s*:", line) or re.match(
        r"^\s*-->\s*\d+\s*:", line
    )
    colon_position = line.find(":")
    highlighting = False
    text = None
    if not line_parts:
        line_parts = [(0, len(line))]

    for begin, end in line_parts:
        if highlighting:
            part = Text(line[begin:end], style=error_style)
            if not line[begin:end]:
                part.append(Text(" ", style=error_style))

        elif has_line_number and begin < colon_position:
            begin_line = line[begin : colon_position + 1]
            arrow_position = begin_line.find("-->")
            if arrow_position != -1:
                part = Text(line[begin : arrow_position + 3], style=operator_style)
                part.append(
                    Text(line[arrow_position + 3 : colon_position], style=number_style)
                )
            else:
                part = Text(line[begin:colon_position], style=number_style)
            part.append(
                Text(line[colon_position : colon_position + 1], style=operator_style)
            )
            part.append(Text(line[colon_position + 1 : end], style=code_style))
        elif line.strip() == "(...)":
            part = Text(line[begin:end], style=operator_style)
        else:
            part = Text(line[begin:end], style=code_style)
        if text is None:
            text = part
        else:
            text.append(part)
        highlighting = not highlighting
    return text


def highlight_by_tokens(line, line_parts, theme):
    """This is a simplified version of what Pygments does when highlighting
    some code.
    """
    background = theme.background_color
    operator_style = f"{theme.styles[Operator]} on {background}"
    number_style = f"{theme.styles[Number]} on {background}"
    code_style = f"{theme.styles[Name]} on {background}"
    keyword_style = f"{theme.styles[Keyword]} on {background}"
    constant_style = f"{theme.styles[Keyword.Constant]} on {background}"
    comment_style = f"{theme.styles[Comment]} on {background}"
    builtin_style = f"{theme.styles[Name.Builtin]} on {background}"
    exception_style = f"{theme.styles[Generic.Error]} on {background}"
    string_style = f"{theme.styles[String]} on {background}"

    def highlight_token(token):
        """Imitating pygment's styling of individual token."""
        if token.is_keyword():
            if token.string in ["True", "False", "None"]:
                sub_part = Text(token.string, style=constant_style)
            else:
                sub_part = Text(token.string, style=keyword_style)
        elif is_builtin(token.string):
            sub_part = Text(token.string, style=builtin_style)
        elif is_exception(token.string):
            sub_part = Text(token.string, style=exception_style)
        elif token.is_comment():
            sub_part = Text(token.string, style=comment_style)
        elif token.is_number():
            sub_part = Text(token.string, style=number_style)
        elif token.is_operator():
            sub_part = Text(token.string, style=operator_style)
        elif token.is_string():
            sub_part = Text(token.string, style=string_style)
        else:
            sub_part = Text(token.string, style=code_style)
        return sub_part

    error_style = colours.get_highlight()
    highlighting = False
    text = None
    tokens = token_utils.tokenize(line)
    last_column = 0
    for index, (begin, end) in enumerate(line_parts):
        if highlighting:
            part = Text(line[begin:end], style=error_style)
            if not line[begin:end]:
                part.append(Text(" ", style=error_style))
            last_column = end
        else:
            part = None
            for token in tokens:
                if token.start_col < begin:
                    continue
                if token.start_col >= end:
                    # After inserting some non-highlighted space,
                    # we are going to highlight the next token.
                    # However, we might want to highlight some spaces
                    # before that token, so we don't include them here.
                    start = token.start_col
                    if len(line_parts) > index + 1:  # should always be True
                        start = min(token.start_col, line_parts[index + 1][0])
                    inserted_space = " " * (start - last_column)
                    if part is None:
                        part = Text(inserted_space, style=code_style)
                    else:
                        part.append(Text(inserted_space, style=code_style))
                    last_column = start
                    break

                if token.start_col > last_column:
                    # We need to insert the required spaces between the tokens.
                    inserted_space = " " * (token.start_col - last_column)
                    if part is None:
                        part = Text(inserted_space, style=code_style)
                    else:
                        part.append(Text(inserted_space, style=code_style))
                last_column = token.end_col

                sub_part = highlight_token(token)
                if part is None:
                    part = sub_part
                else:
                    part.append(sub_part)
        if text is None:
            text = part
        elif part is not None:  # None can happen for EOF
            text.append(part)
        highlighting = not highlighting
    return text


def init_console(theme=friendly_dark, color_system="auto", force_jupyter=None):
    def _patch_heading(self, *_args):
        """By default, all headings are centered by Rich; I prefer to have
        them left-justified, except for <h3>
        """
        text = self.text
        text.justify = "left"
        if self.level == 3:
            yield Text("    ") + text
        else:
            yield text

    Heading.__rich_console__ = _patch_heading

    def _patch_code_block(self, *_args):
        if self.lexer_name == "default":
            self.lexer_name = "python"

        code = str(self.text).rstrip()
        lines = code.split("\n")
        error_lines = get_highlighting_ranges(lines)

        if (
            colours.get_highlight() is not None  # otherwise, use carets
            and self.lexer_name == "python"  # do not process pytb
            and error_lines
        ):
            yield from format_with_highlight(lines, error_lines, theme)
        else:
            yield Syntax(code, self.lexer_name, theme=theme, word_wrap=True)

    CodeBlock.__rich_console__ = _patch_code_block

    if theme == friendly_light:
        rich.reconfigure(
            theme=light_background_theme,
            color_system=color_system,
            force_jupyter=force_jupyter,
        )
    else:
        rich.reconfigure(
            theme=dark_background_theme,
            color_system=color_system,
            force_jupyter=force_jupyter,
        )
    console = rich.get_console()
    pretty.install(console=console, indent_guides=True)
    return console
