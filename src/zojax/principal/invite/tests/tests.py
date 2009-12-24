##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" zojax.content.browser tests

$Id$
"""
import os, unittest, doctest
from persistent import Persistent
from zope import interface, component
from zope.app.rotterdam import Rotterdam
from zope.app.testing import setup, placelesssetup, functional
from zojax.layoutform.interfaces import ILayoutFormLayer


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


class Content(Persistent):
    pass


zojaxPrincipalInviteLayer = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxPrincipalInviteLayer', allow_teardown=True)


def test_suite():
    testbrowser = functional.FunctionalDocFileSuite(
        "testbrowser.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    testbrowser.layer = zojaxPrincipalInviteLayer

    return unittest.TestSuite((testbrowser,))
