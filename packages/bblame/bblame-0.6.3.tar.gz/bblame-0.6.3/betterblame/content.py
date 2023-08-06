"""A module to contain objects and implementation which together are
the backbone of the internal representation of the text the user sees"""
import curses
import re
import logging
import gc
import zlib

from abc import ABCMeta, abstractmethod
from collections import defaultdict
from collections import namedtuple
from six import string_types

from .options import UserOptionManager, SHORTEN_FILEPATHS_OPT
from .util import substring_split

DEFAULT_CURSES_ATTR = curses.A_NORMAL


class ContentStack(object):
    """A class to represent the content added as users drill into git revs,
    cycle through git history, show commits, etc"""
    def __init__(self):
        self.content_stack = []

    # These frames also store the state necessary to move back to the
    # previous frame/screen when it is popped. Essentially storing a snapshot
    # of what the screen looked like before we add this frame
    StackFrame = namedtuple('StackFrame', ['content', 'last_current_line',
                                           'last_current_width',
                                           'last_cursor_line', 'last_mode'])

    def __len__(self):
        return len(self.content_stack)

    def peek(self):
        """Peek and return the content on the top of the stack,
        without removing it from the stack"""
        return self.content_stack[-1]

    def pop(self):
        """Pop content off the content stack, first checking if we have any
        extra content that can be popped (I.e. we don't want to be left]
        without any content to display to the user."""
        cstack = self.content_stack
        if len(cstack) <= 1:
            raise IndexError('No content to pop')
        frame_to_return = cstack.pop()
        self.content_stack[-1].content.decompress()
        return frame_to_return

    def add(self, newcontent_obj, current_line, current_width,
            cursor_line, mode):
        """Add a new frame object to the Content Stack, preserving some of our
        current state as we do that, so it can be restored when we pop this."""
        # compress current stack before adding the new stack
        if len(self.content_stack) >= 1:
            last_content = self.content_stack[-1].content
            # If the last content was a blame, then compress it as these can
            # be quite large.
            last_content.compress()
        stack_frame = self.StackFrame(newcontent_obj, current_line,
                                      current_width, cursor_line, mode)
        self.content_stack.append(stack_frame)


class BaseContent:
    """A base class for the git objects (blame and show)
    Comes with len and get/set overrides and the methods to compress and
    uncompress the lines attribute"""
    __metaclass__ = ABCMeta

    default_attr = curses.A_NORMAL
    default_str = '~'

    @abstractmethod
    def __init__(self):
        # To be called after subclasses __init__ work is done

        # self.lines comes from subclasses, init it again here to make pylint
        # happy
        self.lines = self.lines  # Satisfy pylint

        # lines will grow if any '~' padding is added
        self.numlines = len(self.lines)
        # Collect after any deleted objects
        gc.collect()

    @abstractmethod
    def buildlinesdict(self, lines):
        """build a default dict with schema:
        index --> Line(line or <defaultstr>, curses str attributes)
        The default string makes scrolling past the edge of the file much more
        graceful.
        I.e. having a default value rather than handling IndexError and then
        returning the default string.
        This function will add a default or the provided attribute to each
        line.  The lines can be further decorated at later times by logically
        OR-ing in other attributes to the attribute set here. Classes that need
        to do more advanced processing of the lines, should override this
        method"""
        logging.info('running base buildlinesdict')
        ret_lines_dict = self.gen_default_lines_dict()
        for idx, line in enumerate(lines):
            ret_lines_dict[idx] = Line([line], BaseContent.default_attr)

        return ret_lines_dict

    def gen_default_lines_dict(self):
        """Return a default dict with the proper schema to be used for a lines
        dictionary"""
        return defaultdict(lambda: (Line([BaseContent.default_str],
                                         BaseContent.default_attr)))

    def __len__(self):
        return self.numlines

    def __getitem__(self, index):
        return self.lines[index]

    def __setitem__(self, index, value):
        self.lines[index] = value

    def compress(self):
        """Compress the lines attribute which stores the content of the lines
        attribute. This makes storing each stack frame cheaper"""
        # XXX: compress/decompress currently broken by new Line Segments
        # feature. It's more difficult to compress the lines (with a good
        # compression ratio) as well as keeping the curses attributes for each
        # segment. Will address this feature at a later date (either fixing or
        # removing this feature)
        # pylint: disable=unreachable
        return

        blame_text = '\n'.join([line.full_text()
                                for line in self.lines.values()])
        compressed_lines = zlib.compress(blame_text.encode('utf-8'))
        del self.lines
        gc.collect()
        self.lines = compressed_lines

    def decompress(self):
        """Decompress the lines attribute which stores the content of the git
        blame."""
        # XXX: compress/decompress currently broken by new Line Segments
        # feature. It's more difficult to compress the lines (with a good
        # compression ratio) as well as keeping the curses attributes for each
        # segment. Will address this feature at a later date (either fixing or
        # removing this feature)
        # pylint: disable=unreachable
        return

        temp_lines = zlib.decompress(self.lines)
        # We don't need any special processing at this point, since it was
        # already done and we're just re-hydrating it from concentrate
        self.lines = BaseContent.buildlinesdict(self, temp_lines.splitlines())
        del temp_lines
        gc.collect()


class Segment(object):
    """A class to represent a single segment of a line. Segments represent a
    portion of the text of a line and have their own curses attributes and
    colours"""
    def __init__(self, text, curses_attrs, syntax_attrs):
        """
        <text>: The text the user will see that this segment represents
        <curses_attrs>: Specific curses attributes for this segment
        <syntax_attrs>: Syntax highlighting attributes for colouring text
        This allows you to have a single line be coloured differently or have
        portions standout or bold, etc"""
        assert type(curses_attrs) is int

        self._text = text
        self.curses_attrs = curses_attrs
        self.syntax_attrs = syntax_attrs
        self.opt_mngr = UserOptionManager()

    @property
    def text(self):
        """Getter for text. Must have a getter in this case, because other
        Segment types inherit from this one, so if it sets text when it is
        being called from a super init, it will cause an attribute error"""
        return self._text


class FilepathSegment(Segment):
    """A segment that represents a file path. Which can return the full path or
    just file name depending on user options"""
    def __init__(self, filepath_text, curses_attrs, syntax_attrs,
                 filename_text):
        # The first arg passed to init will be set as self._text
        super(FilepathSegment, self).__init__(filepath_text, curses_attrs,
                                              syntax_attrs)
        self.filename_text = filename_text

    @property
    def text(self):
        """Getter method for text. Depending on the current state and user
        options enabled this will return different text"""
        shorten_paths_opt = self.opt_mngr.get_option(SHORTEN_FILEPATHS_OPT)
        if shorten_paths_opt.is_enabled():
            return self.filename_text

        return self._text


class Line(object):
    """A class to represent each line of the git object being shown (blame,
    show, etc)
    """

    def __init__(self, list_of_segments=None, default_attr=curses.A_NORMAL):
        """Can provide a list of strings, each string will become one segment
        with its own curses attributes, segments passed this way will get the
        default curses attributes"""
        if not list_of_segments:
            list_of_segments = []
        self.line_segments = []  # a list of line_segment tuples

        # Set the default attribute for this line
        self.default_attr = default_attr

        assert not isinstance(list_of_segments, string_types), \
            'Argument to Line must be a list of strings'

        for segment in list_of_segments:
            if isinstance(segment, Segment):
                # This is already a segment type, so just add it to the list
                self.line_segments.append(segment)
            else:
                # Otherwise init a new segment
                self.add_segment(segment)

    def add_segment(self, segment_text, segment_attributes=None,
                    syntax_attrs=None):
        """Add a new segment to the line. See the Segment class for more
        information"""
        if not segment_attributes:
            segment_attributes = self.default_attr

        self.line_segments.append(Segment(segment_text,
                                          segment_attributes,
                                          syntax_attrs))

    def add_filepath_segment(self, filepath_text, filename_text,
                             segment_attributes=None,
                             syntax_attrs=None):
        """Add a new filepath segment to the line. This type of segment has two
        texts the full path and just the name"""
        if not segment_attributes:
            segment_attributes = self.default_attr

        self.line_segments.append(FilepathSegment(filepath_text,
                                                  segment_attributes,
                                                  syntax_attrs, filename_text))

    def full_text(self):
        """Returns the entire text of the line, combining all text from each
        segments. This returns the line with no default_attr"""
        ret = ''

        for segment in self.line_segments:
            ret = ret + segment.text

        return ret

    def prepare_line_for_printing(self, start, end):
        """Prepare a line that is ready for printing to the screen for the
        user. This involves trimming the line to fit within the <width> of the
        screen, mutating segments or even discarding them if the users wishes)
        """
        num_chars_so_far = 0
        # A throw away line that will be used to print to the screen and
        # discarded
        ret_line = Line()

        if start < 0 or start > end:
            raise Exception('Invalid start arg given')

        for segment in self.line_segments:
            # Mutate the segment or discard it before we use it for length
            # any calculations:
            seg_text = segment.text

            if start > num_chars_so_far:
                # Check if we should begin collecting segments
                if len(seg_text) + num_chars_so_far > start:
                    # Check how much of this segment that just pushes into the
                    # collection range should be included. This is the latter
                    # portion of the segment text
                    chars_to_take = ((len(seg_text) + num_chars_so_far) -
                                     start)
                    ret_line.add_segment(seg_text[-chars_to_take:],
                                         segment.curses_attrs,
                                         segment.syntax_attrs)
            else:
                if len(seg_text) + num_chars_so_far < end:
                    # The whole segment can fit
                    ret_line.add_segment(seg_text,
                                         segment.curses_attrs,
                                         segment.syntax_attrs)
                else:
                    # We can't fit the entirety of the next segment, but check
                    # if a subset will fit. This is the former portion of the
                    # segment.
                    num_chars_remaining = end - num_chars_so_far
                    if num_chars_remaining:
                        ret_line.add_segment(seg_text[:num_chars_remaining],
                                             segment.curses_attrs,
                                             segment.syntax_attrs)
                    break
            num_chars_so_far += len(seg_text)

        return ret_line

    def highlight_str(self, str_to_highlight, highlight_attr):
        """Takes an input string to highlight and searches for instances of it
        (even across segment boundaries), creating a new segment for each hit
        and changing it's curses attribute to highlight.
        Returns a new Line object"""
        # print('string to highlight: %s' % str_to_highlight)
        search_str_re = re.escape(str_to_highlight)
        # print('string to highlight re: %s' % search_str_re)
        segments = self.line_segments
        for start_pos in [match.start() for match in
                          re.finditer('(%s)' % search_str_re,
                                      self.full_text())]:
            # print('working on start_pos: %d' % start_pos)
            segments = self._split_new_segment(start_pos,
                                               start_pos+len(str_to_highlight),
                                               highlight_attr, segments)
        return Line(segments)

    def _split_new_segment(self, start, end, curses_attrs, segments):
        """Cut a new segment out at <start>, <end>, giving it the curses
        attributes <curses_attrs>.
        Returns a new segment list"""
        new_segments = []
        new_seg_len = end-start
        done_split = False
        if start < 0 or start > end:
            raise Exception('Invalid start arg given')

        num_chars_so_far = 0
        remaining_chars = -1
        # print('start %d' % start)
        # print('end %d' % end)
        # print('full_text:  %s' % ':'.join([seg.text for seg in segments]))
        segments = iter(segments)
        for segment in segments:
            # Mutate the segment or discard it before we use it for length
            # calculations
            seg_text = segment.text
            seg_len = len(seg_text)
            # print('working on seg %s, with len: %d' % (segment, seg_len))
            # print('num_chars_so_far: %d' % num_chars_so_far)
            if not done_split and start >= num_chars_so_far:
                # print('checking if we\'ve reached start yet')
                if seg_len + num_chars_so_far > start:
                    # print('we\'ve reached the start!')
                    # We've found the split point
                    (prev_s, new_s,
                     next_s) = substring_split(start-num_chars_so_far,
                                               end-num_chars_so_far,
                                               seg_text)
                    # print('prev_s: %s' % prev_s)
                    if prev_s:
                        prev_seg = Segment(prev_s,
                                           segment.curses_attrs,
                                           segment.syntax_attrs)
                        # print('prev_seg: %s' % prev_seg.text)
                        new_segments.append(prev_seg)

                    # print('new_s: %s' % new_s)
                    # grab the full substring here. We'll skip all segments
                    # that fall into this range down below
                    if not curses_attrs:
                        curses_attrs = segment.curses_attrs
                    new_segments.append(
                        Segment(self.full_text()[start:end],
                                curses_attrs, None))

                    # print('next_s: %s' % next_s)
                    if next_s:
                        next_seg = Segment(next_s,
                                           segment.curses_attrs,
                                           segment.syntax_attrs)
                        # print('next_seg: %s' % next_seg.text)
                        new_segments.append(next_seg)

                    remaining_chars = new_seg_len - len(new_s)
                    done_split = True
                    num_chars_so_far += len(seg_text)
                    continue

            if remaining_chars > 0:
                # print('remaining_chars: %d' % remaining_chars)
                if remaining_chars < seg_len:
                    # print('We need a portion of this segment')
                    # We need a portion of this line
                    # Modify the segment following this one to remove any
                    # pieces that belong to the new segment
                    next_seg = Segment(
                        segment.text[remaining_chars:],
                        segment.curses_attrs,
                        segment.syntax_attrs)
                    new_segments.append(next_seg)
                else:
                    # print('we need all of the chars from this seg, continue'
                    #       ' skipping this line')
                    pass
                remaining_chars -= seg_len
                num_chars_so_far += len(seg_text)
                continue

            new_segments.append(segment)
            num_chars_so_far += len(seg_text)

        return new_segments

    def __len__(self):
        return len(self.line_segments)

    def __getitem__(self, index):
        return self.line_segments[index]

    def __setitem__(self, index, value):
        raise NotImplementedError('__setitem__ not implemented, please use the'
                                  'add_segment method')
