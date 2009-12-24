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
import random

from zope import interface, component
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIds
from zope.app.intid.interfaces import IIntIdAddedEvent, IIntIdRemovedEvent
from zojax.content.type.configlet import ContentContainerConfiglet

from catalog import InvitationsCatalog
from interfaces import IInvitation, IInvitations


class Invitations(ContentContainerConfiglet):
    interface.implements(IInvitations)

    _chars = '0123456789QWERTYUIOPASDFGHJKLZXCVBNM'

    @property
    def catalog(self):
        catalog = self.data.get('catalog')
        if catalog is None:
            catalog = InvitationsCatalog()
            self.data['catalog'] = catalog
        return catalog

    def storeInvitation(self, invitation):
        id = ''
        while not id and id not in self:
            id = ''
            for idx in range(24):
                id = id + random.choice(self._chars)

        self[id] = invitation

    def removeObject(self, object):
        catalog = self.catalog

        for invitation in self.catalog.search(object):
            del self[invitation.__name__]

    def getInvitationsByObject(self, object, type=None):
        query = {}
        if type:
            if isinstance(type, basestring):
                type = (type,)
            query['type'] = {'any_of': type}
        return self.catalog.search(object, **query)

    def getInvitationsByOwner(self, owner, type=None):
        query = {'owner': {'any_of': (owner,)}}
        if type:
            if isinstance(type, basestring):
                type = (type,)
            query['type'] = {'any_of': type}
        return self.catalog.search(**query)

    def getInvitationsByPrincipal(self, principal, type=None):
        query = {'principal': {'any_of': (principal,)}}
        if type:
            if isinstance(type, basestring):
                type = (type,)
            query['type'] = {'any_of': type}
        return self.catalog.search(**query)

    def search(self, **kw):
        return self.catalog.search(**kw)


@component.adapter(IInvitation, IIntIdAddedEvent)
def invitationAddedEvent(invitation, event):
    invitation = removeAllProxies(invitation)
    configlet = removeAllProxies(getUtility(IInvitations))

    configlet.catalog.index_doc(
        getUtility(IIntIds).getId(invitation), invitation)


@component.adapter(IInvitation, IIntIdRemovedEvent)
def invitationRemovedEvent(invitation, event):
    configlet = removeAllProxies(getUtility(IInvitations))

    configlet.catalog.unindex_doc(
        getUtility(IIntIds).getId(removeAllProxies(invitation)))


@component.adapter(IIntIdRemovedEvent)
def objectRemovedEvent(event):
    removeAllProxies(getUtility(IInvitations)).removeObject(event.object)
