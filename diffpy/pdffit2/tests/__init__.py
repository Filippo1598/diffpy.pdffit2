#!/usr/bin/env python
##############################################################################
#
# diffpy.pdffit2    by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2012 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Pavol Juhas
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

"""Unit tests for the diffpy.pdffit2 package.
"""

import unittest

def testsuite(pattern=''):
    '''Create a unit tests suite for the diffpy.pdffit2 package.

    Parameters
    ----------
    pattern : str, optional
        Regular expression pattern for selecting test cases.
        Select all tests when empty.  Ignore the pattern when
        any of unit test modules fails to import.

    Returns
    -------
    suite : `unittest.TestSuite`
        The TestSuite object containing the matching tests.
    '''
    import re
    from os.path import dirname
    from itertools import chain
    from pkg_resources import resource_filename
    loader = unittest.defaultTestLoader
    thisdir = resource_filename(__name__, '')
    depth = __name__.count('.') + 1
    topdir = thisdir
    for i in range(depth):
        topdir = dirname(topdir)
    suite_all = loader.discover(thisdir, pattern='*Test*.py',
                                top_level_dir=topdir)
    # always filter the suite by pattern to test-cover the selection code.
    suite = unittest.TestSuite()
    rx = re.compile(pattern)
    tsuites = list(chain.from_iterable(suite_all))
    tsok = all(isinstance(ts, unittest.TestSuite) for ts in tsuites)
    if not tsok:    # pragma: no cover
        return suite_all
    tcases = chain.from_iterable(tsuites)
    for tc in tcases:
        tcwords = tc.id().rsplit('.', 2)
        shortname = '.'.join(tcwords[-2:])
        if rx.search(shortname):
            suite.addTest(tc)
    # verify all tests are found for an empty pattern.
    assert pattern or suite_all.countTestCases() == suite.countTestCases()
    return suite


def test():
    '''Execute all unit tests for the diffpy.pdffit2 package.

    Returns
    -------
    result : `unittest.TestResult`
    '''
    suite = testsuite()
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return result


def testdeps():
    '''Execute all unit tests for diffpy.pdffit2 and its dependencies.

    Returns
    -------
    result : `unittest.TestResult`
    '''
    modulenames = '''
        diffpy.pdffit2.tests
        diffpy.Structure.tests
    '''.split()
    suite = unittest.TestSuite()
    t = None
    for mname in modulenames:
        exec ('from %s import testsuite as t' % mname)
        suite.addTests(t())
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return result


# End of file
