"""Utility functions and objects"""


def substring_split(start, end, string):
    """Split string at start:end, returning all three substrings (beginning,
    middle, end) if available"""
    # print('substring_split, start: %d, end: %d' % (start, end))
    return string[:start], string[start:end], string[end:]


def left_str_strip(string, str_to_strip):
    """Strips whole string <str_to_strip> from <string> from the left side.
    Distinct from lstrip, since the latter strips all chars, in any order, from
    the string"""
    return string[len(str_to_strip):]


def check_string(string, msg):
    """Checks if <string> is a string type in a python 2 and 3 compatible way.
    Raises <msg> in the AssertionError """
    try:
        basestring
    except NameError:
        basestring = str
    assert isinstance(string, basestring), msg


# In this case I really do want an object pylint, but thanks...
# pylint: disable=R0903
class BidirectionalCycle(object):
    """A cycle iterator that can iterate in both directions (e.g. has next
    and prev).
    This is a simple object that supports the iterator protocol but it doesn't
    behave like one might expect a standard iterator to (e.g. a generator that
    lazily produces the next value) this object will keep the WHOLE LIST in
    memory, so use WITH CAUTION
    >>> bi_iter = BidirectionalCycle([0, 1, 2])
    >>> bi_iter.next()
    0
    >>> bi_iter.next()
    1
    >>> bi_iter.next()
    2
    >>> bi_iter.next()
    0
    >>> bi_iter.prev()
    2
    >>> bi_iter.prev()
    1
    >>> bi_iter.prev()
    0
    >>> bi_iter.prev()
    2
    >>> bi_iter = BidirectionalCycle([0, 1, 2], starting_index=1)
    >>> bi_iter.next()
    1
    >>> bi_iter = BidirectionalCycle([0, 1, 2], starting_index=1)
    >>> bi_iter.prev()
    1
    >>> bi_iter = BidirectionalCycle([0, 1, 2], starting_index=1, no_wrap=True)
    >>> bi_iter.next()
    1
    >>> bi_iter.next()
    2
    >>> bi_iter.next()
    Traceback (most recent call last):
    ...
    StopIteration
    """
    def __init__(self, list_seq, starting_index=0, no_wrap=False):
        self.current_index = self.init_index = starting_index
        # CURRENTLY ONLY SUPPORT LISTS
        assert isinstance(list_seq, list), 'Currently only supports lists'
        self.seq = list_seq
        self.no_wrap = no_wrap
        self.start_of_day = True

    def next(self):
        """Maintain support for python2 iterator"""
        return self.__next__()

    def __next__(self):
        """return the next item in the iteration"""
        self._check_len()
        if self.start_of_day:
            return self._start_of_day()

        self._move_index_next()
        next_item = self.seq[self.current_index]

        return next_item

    def prev(self):
        """return the previous item in the iteration"""
        self._check_len()
        if self.start_of_day:
            if self.no_wrap:
                raise StopIteration()
            return self._start_of_day()

        self._move_index_prev()
        prev_item = self.seq[self.current_index]

        return prev_item

    def curr(self):
        """Returns the current item in the iteration"""
        self._check_len()
        if self.start_of_day:
            return self._start_of_day()

        return self.seq[self.current_index]

    def _move_index_next(self):
        """Move the index in the next direction"""
        # check if we need to wrap around to the beginning
        if self.current_index == len(self.seq) - 1:
            if self.no_wrap:
                raise StopIteration()
            self.current_index = 0
        else:
            self.current_index = self.current_index + 1

    def _move_index_prev(self):
        """Move the index in the prev direction"""
        # check if we need to wrap around to the end
        if self.current_index == 0:
            if self.no_wrap:
                raise StopIteration()
            self.current_index = len(self.seq) - 1
        else:
            self.current_index = self.current_index - 1

    def _check_len(self):
        """As itertools.cycle does, raise StopIteration if the sequence
        is empty"""
        if len(self.seq) == 0:
            raise StopIteration

    def _start_of_day(self):
        """print out the init_index of the sequence and set start_of_day to
        false. This is needed to get the behaviour that after init-ing the
        iterator if you call either previous or next, you get the starting
        index."""
        self.start_of_day = False
        return self.seq[self.init_index]

    def __str__(self):
        return str(self.seq)

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.seq)

    def __contains__(self, item):
        return item in self.seq
