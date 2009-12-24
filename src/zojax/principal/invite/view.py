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
"""Catalog Views

$Id$
"""
from zope.proxy import removeAllProxies
from zojax.wizard.step import WizardStep
from zojax.statusmessage.interfaces import IStatusMessage


class Advanced(WizardStep):

    def update(self):
        catalog = self.context['catalog']

        if 'form.button.reindex' in self.request:
            catalog.clear()
            catalog.updateIndexes()
            IStatusMessage(self.request).add('Catalog has been reindexed.')

        self.catalog = catalog

    def getIndexInfo(self, id):
        index = removeAllProxies(self.catalog[id])
        return {'documents': index.documentCount, 'words': index.wordCount}
