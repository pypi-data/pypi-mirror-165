"""Module for syntax highlighting file content using pygments"""
import logging
import curses
import re

# pylint: disable=no-name-in-module
from pygments.formatters import TerminalFormatter
from pygments.lexers import get_lexer_for_filename, guess_lexer
from pygments import highlight
from pygments.util import ClassNotFound


FORMATTER = TerminalFormatter()


# ANSI style codes
# Not all codes are used currently, but keep them all here for completeness
ANSI_RESET = 0
ANSI_BOLD_ON = 1
ANSI_BOLD_OFF = 22
ANSI_ITALICS_ON = 3
ANSI_ITALICS_OFF = 23
ANSI_UNDERLINE_ON = 4
ANSI_UNDERLINE_OFF = 24
ANSI_INVERSE_ON = 7
ANSI_INVERSE_OFF = 27
ANSI_STRIKETHROUGH_ON = 9
ANSI_STRIKETHROUGH_OFF = 29

# ANSI colour codes
ANSI_COLOR_BLACK_FG = 30
ANSI_COLOR_BLACK_BG = 40
ANSI_COLOR_RED_FG = 31
ANSI_COLOR_RED_BG = 41
ANSI_COLOR_GREEN_FG = 32
ANSI_COLOR_GREEN_BG = 42
ANSI_COLOR_YELLOW_FG = 33
ANSI_COLOR_YELLOW_BG = 43
ANSI_COLOR_BLUE_FG = 34
ANSI_COLOR_BLUE_BG = 44
ANSI_COLOR_MAGENTA_FG = 35
ANSI_COLOR_MAGENTA_BG = 45
ANSI_COLOR_CYAN_FG = 36
ANSI_COLOR_CYAN_BG = 46
ANSI_COLOR_WHITE_FG = 37
ANSI_COLOR_WHITE_BG = 47
ANSI_COLOR_DEFAULT_FG = 39
ANSI_COLOR_DEFAULT_BG = 49

# New "Bright" colours, no need for bold
ANSI_COLOR_BRIGHT_BLACK_FG = 90
ANSI_COLOR_BRIGHT_BLACK_BG = 100
ANSI_COLOR_BRIGHT_RED_FG = 91
ANSI_COLOR_BRIGHT_RED_BG = 101
ANSI_COLOR_BRIGHT_GREEN_FG = 92
ANSI_COLOR_BRIGHT_GREEN_BG = 102
ANSI_COLOR_BRIGHT_YELLOW_FG = 93
ANSI_COLOR_BRIGHT_YELLOW_BG = 103
ANSI_COLOR_BRIGHT_BLUE_FG = 94
ANSI_COLOR_BRIGHT_BLUE_BG = 104
ANSI_COLOR_BRIGHT_MAGENTA_FG = 95
ANSI_COLOR_BRIGHT_MAGENTA_BG = 105
ANSI_COLOR_BRIGHT_CYAN_FG = 96
ANSI_COLOR_BRIGHT_CYAN_BG = 106
ANSI_COLOR_BRIGHT_WHITE_FG = 97
ANSI_COLOR_BRIGHT_WHITE_BG = 107

ANSI_FOREGROUND = frozenset({
    ANSI_COLOR_BLACK_FG,
    ANSI_COLOR_RED_FG,
    ANSI_COLOR_GREEN_FG,
    ANSI_COLOR_YELLOW_FG,
    ANSI_COLOR_BLUE_FG,
    ANSI_COLOR_MAGENTA_FG,
    ANSI_COLOR_CYAN_FG,
    ANSI_COLOR_WHITE_FG,
    ANSI_COLOR_DEFAULT_FG,
    ANSI_COLOR_BRIGHT_BLACK_FG,
    ANSI_COLOR_BRIGHT_RED_FG,
    ANSI_COLOR_BRIGHT_GREEN_FG,
    ANSI_COLOR_BRIGHT_YELLOW_FG,
    ANSI_COLOR_BRIGHT_BLUE_FG,
    ANSI_COLOR_BRIGHT_MAGENTA_FG,
    ANSI_COLOR_BRIGHT_CYAN_FG,
    ANSI_COLOR_BRIGHT_WHITE_FG,
})

ANSI_BACKGROUND = frozenset({
    ANSI_COLOR_BLACK_BG,
    ANSI_COLOR_RED_BG,
    ANSI_COLOR_GREEN_BG,
    ANSI_COLOR_YELLOW_BG,
    ANSI_COLOR_BLUE_BG,
    ANSI_COLOR_MAGENTA_BG,
    ANSI_COLOR_CYAN_BG,
    ANSI_COLOR_WHITE_BG,
    ANSI_COLOR_DEFAULT_BG,
    ANSI_COLOR_BRIGHT_BLACK_BG,
    ANSI_COLOR_BRIGHT_RED_BG,
    ANSI_COLOR_BRIGHT_GREEN_BG,
    ANSI_COLOR_BRIGHT_YELLOW_BG,
    ANSI_COLOR_BRIGHT_BLUE_BG,
    ANSI_COLOR_BRIGHT_MAGENTA_BG,
    ANSI_COLOR_BRIGHT_CYAN_BG,
    ANSI_COLOR_BRIGHT_WHITE_BG,
})

ANSI_BRIGHT = frozenset({
    ANSI_COLOR_BRIGHT_BLACK_FG,
    ANSI_COLOR_BRIGHT_RED_FG,
    ANSI_COLOR_BRIGHT_GREEN_FG,
    ANSI_COLOR_BRIGHT_YELLOW_FG,
    ANSI_COLOR_BRIGHT_BLUE_FG,
    ANSI_COLOR_BRIGHT_MAGENTA_FG,
    ANSI_COLOR_BRIGHT_CYAN_FG,
    ANSI_COLOR_BRIGHT_WHITE_FG,
    ANSI_COLOR_BRIGHT_BLACK_BG,
    ANSI_COLOR_BRIGHT_RED_BG,
    ANSI_COLOR_BRIGHT_GREEN_BG,
    ANSI_COLOR_BRIGHT_YELLOW_BG,
    ANSI_COLOR_BRIGHT_BLUE_BG,
    ANSI_COLOR_BRIGHT_MAGENTA_BG,
    ANSI_COLOR_BRIGHT_CYAN_BG,
    ANSI_COLOR_BRIGHT_WHITE_BG,
})

ANSI_MODIFIERS = frozenset({
    ANSI_BOLD_ON,
    ANSI_ITALICS_ON,
    ANSI_UNDERLINE_ON,
    ANSI_INVERSE_ON,
})

# ANSI --> curses attributes map
ANSI_TO_CURSES = {
    ANSI_RESET: curses.A_NORMAL,
    ANSI_BOLD_ON: curses.A_BOLD,
    ANSI_UNDERLINE_ON: curses.A_UNDERLINE,
    ANSI_INVERSE_ON: curses.A_REVERSE,
    ANSI_COLOR_DEFAULT_FG: curses.A_NORMAL,
    ANSI_COLOR_DEFAULT_BG: curses.A_NORMAL,
    ANSI_COLOR_BLACK_FG: curses.COLOR_BLACK,
    ANSI_COLOR_RED_FG: curses.COLOR_RED,
    ANSI_COLOR_GREEN_FG: curses.COLOR_GREEN,
    ANSI_COLOR_YELLOW_FG: curses.COLOR_YELLOW,
    ANSI_COLOR_BLUE_FG: curses.COLOR_BLUE,
    ANSI_COLOR_MAGENTA_FG: curses.COLOR_MAGENTA,
    ANSI_COLOR_CYAN_FG: curses.COLOR_CYAN,
    ANSI_COLOR_WHITE_FG: curses.COLOR_WHITE,
    ANSI_COLOR_BRIGHT_BLACK_FG: curses.COLOR_BLACK,
    ANSI_COLOR_BRIGHT_RED_FG: curses.COLOR_RED,
    ANSI_COLOR_BRIGHT_GREEN_FG: curses.COLOR_GREEN,
    ANSI_COLOR_BRIGHT_YELLOW_FG: curses.COLOR_YELLOW,
    ANSI_COLOR_BRIGHT_BLUE_FG: curses.COLOR_BLUE,
    ANSI_COLOR_BRIGHT_MAGENTA_FG: curses.COLOR_MAGENTA,
    ANSI_COLOR_BRIGHT_CYAN_FG: curses.COLOR_CYAN,
    ANSI_COLOR_BRIGHT_WHITE_FG: curses.COLOR_WHITE,
}

# A_ITALIC was added in python3.7
try:
    curses_italics = curses.A_ITALIC
    ANSI_TO_CURSES[ANSI_ITALICS_ON] = curses.A_ITALIC
except AttributeError:
    pass


def get_lexer(lines, filename):
    """Given the lines of text for the file and filename, try find a lexer
    that matches, returning the lexer object or None"""
    text = '\n'.join(lines)
    lexer = None
    try:
        lexer = get_lexer_for_filename(filename)
    except ClassNotFound:
        try:
            # Guess the lexer by the content of the file
            lexer = guess_lexer(text)
        except ClassNotFound:
            logging.info('pygments couldn\'t determine lexer')

    return lexer


def highlight_lines(lines, lexer):
    """Take the lines of text to be highlighted and return a list of
    highlighted lines using pygments"""
    # Join into one string since pygments needs one string to properly
    # highlight multi line statements.
    text = '\n'.join(lines)
    highlighted_lines = highlight(text, lexer, FORMATTER).splitlines()
    # NOTE: pygments.highlight clobbers any blank lines at the beginning of the
    # file, count how many we should have and re add them.
    # Assemble a list of empty lists. Since parse_highlighed_line returns just
    # an empty list for an empty line.
    # Get empty lines at the beginning of the file
    empty_lines_start = []
    empty_lines_end = []
    curr_line_start = lines[0]
    curr_line_end = lines[-1]
    while '' in [curr_line_start, curr_line_end]:
        if curr_line_start == '':
            empty_lines_start.append([])
            curr_line_start = lines[len(empty_lines_start)]
        if curr_line_end == '':
            empty_lines_end.append([])
            curr_line_end = lines[-len(empty_lines_end)]

    return (empty_lines_start +
            # Parse each line into curses attributes
            [parse_highlighed_line(highlighted_line)
             for highlighted_line in highlighted_lines] +
            empty_lines_end)


def parse_highlighed_line(highlighted_line):
    """Takes an ANSI highlighted line of text and returns a list of tuples,
    each of which describing a section of the line and its associated curses
    attribute to colour it."""
    logging.debug('Working on line: %s:', highlighted_line)
    split_tokens = highlighted_line.split('\x1b[')
    saved_start = None
    if split_tokens[0] != '':
        # There was text before the first escape sequence, this portion does
        # not need to be coloured
        saved_start = split_tokens[0]
        split_tokens = split_tokens[1:]

    try:
        ansi_content_tuples = [re.match(r'(.*?)m(.*)', _s).groups()
                               for _s in split_tokens if _s]
    except AttributeError:
        # No ansi codes in this line. Just return a list of a single tuple,
        # that describes the whole line, with the default cureses attribute
        return [(highlighted_line, curses.A_NORMAL)]

    logging.debug('Tokenized line with ansi codes: %s', ansi_content_tuples)

    join_mergable_ansi_codes(ansi_content_tuples)

    logging.debug('Tokenized line with ansi codes AFTER merging: %s',
                  ansi_content_tuples)

    res = []

    # TODO: Time this code, if it's slow then parallelize it
    # Convert the ansi code portion of each tuple into curses attributes
    for ansi_codes, token_str in ansi_content_tuples:
        logging.debug('Working on ansi coded tuple: (%s, %s)',
                      ansi_codes, token_str)
        if ';' in ansi_codes:
            # There are multiple ansi codes for this string
            ansi_code_list = ansi_codes.split(';')
        else:
            ansi_code_list = [ansi_codes]

        # Up until now the codes were read in from strings, convert them to int
        # str --> int ansi codes
        ansi_code_list = map(int, ansi_code_list)

        # ansi --> curses
        # Sort the ansi codes into fg, bg and modifier. At the moment we don't
        # use the background, but may do so in the future.
        fg_colour, _, modifier = ansi_to_curses(ansi_code_list)

        curses_attrs = curses.A_NORMAL
        if fg_colour:
            curses_attrs = fg_colour
            if modifier:
                logging.debug('Applying modifier: %s', modifier)
                curses_attrs = curses_attrs | modifier

        res.append((token_str, curses_attrs))

    # Add the un-coloured portion of the line we saved earlier if any
    if saved_start:
        res = [(saved_start, curses.A_NORMAL)] + res

    return res


def ansi_to_curses(ansi_code_list):
    """
    Takes a list of ansi codes and split them into the foreground, backgroud
    and modifer (bold, underline, etc) components. Fetch the curses colour
    pair for the fg and bg components (applying bold if it is a "bright"
    version of the colour).
    """
    fg_colour = None
    bg_colour = None
    modifier = None
    for ansi_code in ansi_code_list:
        try:
            curses_attr = ANSI_TO_CURSES[ansi_code]
        except KeyError:
            logging.exception('Got an unknown ansi code from pygments')
            # We ran into an unexpected ansi code, just skip this one
            continue

        if ansi_code in ANSI_FOREGROUND:
            if ansi_code in ANSI_BRIGHT:
                fg_colour = curses.color_pair(curses_attr) | curses.A_BOLD
            else:
                fg_colour = curses.color_pair(curses_attr)
            logging.debug('Detected foreground ansi code: %s', ansi_code)
        elif ansi_code in ANSI_BACKGROUND:
            if ansi_code in ANSI_BRIGHT:
                bg_colour = curses.color_pair(curses_attr) | curses.A_BOLD
            else:
                bg_colour = curses_attr
            logging.debug('Detected background ansi code: %s', ansi_code)
        elif ansi_code in ANSI_MODIFIERS:
            modifier = curses_attr
            logging.debug('Detected modifier ansi code: %s', ansi_code)

    return fg_colour, bg_colour, modifier


def join_mergable_ansi_codes(ansi_content_tuples):
    """
    Sometimes we receive multiple ansi codes intended for a single piece of
    text that are in their own separate escape sequences, instead of being
    bundled together with semicolons.

    Example ansi escaped string:
    # noqa: E501
    [34mfromESC[39;49;00m ESC[04mESC[36m.bblameESC[39;49;00m ESC[34mimportESC[39;49;00m main

    After tokenizing, yields:
    [('34', 'from'), ('39;49;00', ' '), ('04', ''), ('36', '.bblame'), ('39;49;00', ' '), ('34', 'import'), ('39;49;00', ' main')]
                                        ^---------------------------^
                                                  ^^example^^

    You can see ansi code 04 (for underline) was in it's own escaped sequence
    with an empty string next to 36 (blue). Both are meant to apply to the text
    '.bblame', so in the loop below, join cases like this.
    """
    for index, (ansi_code, content) in enumerate(ansi_content_tuples):
        if not content:
            # Empty content, this code likely applies to the next item
            next_index = index + 1
            try:
                ansi_content_tuples[next_index]
            except IndexError:
                # Found an empty content tuple at the end of a line, no need to
                # handle this case.
                continue
            tuple_to_update = ansi_content_tuples[next_index]
            # join the ansi codes together with a semicolon since this is
            # common practice in ansi and the code below already knows how to
            # split it out and handle them.
            ansi_content_tuples[next_index] = (';'.join([ansi_code,
                                                         tuple_to_update[0]]),
                                               tuple_to_update[1])
