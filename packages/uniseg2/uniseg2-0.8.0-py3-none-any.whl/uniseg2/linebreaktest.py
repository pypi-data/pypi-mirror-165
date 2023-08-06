import doctest
import unittest

from . import linebreak
from .db import iter_line_break_tests
from .test import implement_break_tests


skips = [
    # Tests to skip are specified in the form of (string, expect) so
    # as not to skip them when they are modified.
    # All these tests below will fail because they expect results based
    # on the regex-based algorithm on LB25 while we don't implement it yet.
    ("}$", [1, 2]),
    ("$(", [1, 2]),
    ("$(", [1, 2]),
    ("$\u0308(", [2, 3]),
    ("%(", [1, 2]),
    ("%\u0308(", [2, 3]),
    (")$", [1, 2]),
    (")%", [1, 2]),
    (")\u0308$", [2, 3]),
    (")\u0308%", [2, 3]),
    (",0", [1, 2]),
    (",\u03080", [2, 3]),
    ("/0", [1, 2]),
    ("/\u03080", [2, 3]),
    ("\ubd10\uc694. A.3 \ubabb", [1, 4, 6, 8, 9]),
    ("\ubd24\uc5b4. A.2 \ubcfc", [1, 4, 6, 8, 9]),
    ("\uc694. A.4 \ubabb", [3, 5, 7, 8]),
    ("A.1 \ubabb", [2, 4, 5]),
    ("a.2 ", [2, 4]),
    ("a.2 \u0915", [2, 4, 5]),
    ("a.2 \u672c", [2, 4, 5]),
    ("a.2\u30003", [2, 3, 4, 5]),
    ("a.2\u30003", [2, 3, 4, 5]),
    ("a.2\u3000\u300c", [2, 3, 4, 5]),
    ("a.2\u3000\u307e", [2, 3, 4, 5]),
    ("a.2\u3000\u672c", [2, 3, 4, 5]),
    ("code\\(s\\)", [4, 5, 7, 9]),
    ("code\\{s\\}", [4, 5, 7, 9]),
    ("equals .35 cents", [8, 11, 16]),
    ("}%", [1, 2]),
    ("}\u0308$", [2, 3]),
    ("}\u0308%", [2, 3]),
]


@implement_break_tests(linebreak.line_break_boundaries, iter_line_break_tests(), skips)
class LineBreakTest(unittest.TestCase):
    pass


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(linebreak))
    return tests


if __name__ == "__main__":
    unittest.main()
