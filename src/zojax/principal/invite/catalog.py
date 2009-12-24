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
"""

$Id$
"""
from BTrees.IFBTree import IFBTree

from zope import component, interface, event
from zope.proxy import removeAllProxies
from zope.component import getUtility, getAdapter, getAdapters
from zope.app.catalog import catalog
from zope.app.intid.interfaces import IIntIds
from zope.app.container.interfaces import IObjectAddedEvent
from zope.lifecycleevent import ObjectCreatedEvent
from zope.dublincore.interfaces import ICMFDublinCore
from zc.catalog.catalogindex import SetIndex, ValueIndex

from zojax.catalog.utils import getRequest
from zojax.catalog.result import ResultSet, ReverseResultSet
from zojax.catalog.interfaces import ICatalogIndexFactory
from zojax.catalog.index import DateTimeValueIndex
from zojax.ownership.interfaces import IOwnership
from zojax.content.type.interfaces import IContentType

from interfaces import IInvitation, IObjectInvitation
from interfaces import IInvitations, IInvitationsCatalog


class InvitationsCatalog(catalog.Catalog):
    interface.implements(IInvitationsCatalog)

    def createIndex(self, name, factory):
        index = factory()
        event.notify(ObjectCreatedEvent(index))
        self[name] = index

        return self[name]

    def getIndex(self, indexId):
        if indexId in self:
            return self[indexId]

        return self.createIndex(
            indexId, getAdapter(self, ICatalogIndexFactory, indexId))

    def getIndexes(self):
        names = []

        for index in self.values():
            names.append(removeAllProxies(index.__name__))
            yield index

        for name, indexFactory in getAdapters((self,), ICatalogIndexFactory):
            if name not in names:
                yield self.createIndex(name, indexFactory)

    def clear(self):
        for index in self.getIndexes():
            index.clear()

    def index_doc(self, docid, texts):
        for index in self.getIndexes():
            index.index_doc(docid, texts)

    def unindex_doc(self, docid):
        for index in self.getIndexes():
            index.unindex_doc(docid)

    def updateIndexes(self):
        indexes = list(self.getIndexes())

        for uid, obj in self._visitSublocations():
            for index in indexes:
                index.index_doc(uid, obj)

    def _visitSublocations(self):
        ids = getUtility(IIntIds)
        configlet = getUtility(IInvitations)

        for id, invitation in removeAllProxies(configlet).items():
            if IInvitation.providedBy(invitation):
                yield ids.getId(invitation), invitation

    def search(self, object=None, **kw):
        ids = getUtility(IIntIds)

        query = dict(kw)

        # invitations for object
        if type(object) is not type({}) and object is not None:
            oid = ids.queryId(removeAllProxies(object))
            if oid is None:
                return ResultSet(IFBTree(), ids)

            query['object'] = {'any_of': (oid,)}

        # apply searh terms
        results = self.apply(query)
        if results is None:
            results = IFBTree()

        return ResultSet(results, ids)


@component.adapter(IInvitationsCatalog, IObjectAddedEvent)
def handleCatalogAdded(catalog, ev):
    catalog['type'] = ValueIndex('value', IndexableContentType)
    catalog['owner'] = ValueIndex('ownerId', IOwnership)
    catalog['principal'] = ValueIndex('principal')
    catalog['object'] = ValueIndex('value', IndexableObject)
    catalog['expires'] = DateTimeValueIndex('expires', resolution=4)
    catalog['created'] = DateTimeValueIndex('created', ICMFDublinCore, resolution=4)


class IndexableObject(object):

    def __init__(self, invitation, default=None):
        info = IObjectInvitation(invitation, None)

        if info is not None:
            self.value = info.oid
        else:
            self.value = default


class IndexableContentType(object):

    def __init__(self, content, default=None):
        tp = IContentType(content, None)
        if tp is None:
            self.value = default
        else:
            self.value = tp.name
