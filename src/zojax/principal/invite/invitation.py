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
from pytz import utc
from persistent import Persistent
from datetime import timedelta, datetime

from zope import interface, event
from zope.location import Location
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.app.security.interfaces import IAuthentication

from zojax.ownership.interfaces import IOwnerAware, IUnchangeableOwnership

from interfaces import IInvitation, IObjectInvitation, IInvitations
from interfaces import InvitationAcceptedEvent, InvitationRejectedEvent


class Invitation(Location, Persistent):
    interface.implements(
        IInvitation, IAttributeAnnotatable,
        IOwnerAware, IUnchangeableOwnership)

    def __init__(self, principal):
        self.principal = principal
        self.expires = datetime.now(utc) + timedelta(
            getUtility(IInvitations).expireDays)

    @property
    def id(self):
        return self.__name__

    def isExpired(self):
        return datetime.now(utc) > self.expires

    def accept(self):
        event.notify(InvitationAcceptedEvent(self))

        del self.__parent__[self.__name__]

    def reject(self):
        event.notify(InvitationRejectedEvent(self))

        del self.__parent__[self.__name__]


class ObjectInvitation(Invitation):
    interface.implements(IObjectInvitation)

    def __init__(self, principal, oid):
        self.oid = oid
        super(ObjectInvitation, self).__init__(principal)

    @property
    def object(self):
        return getUtility(IIntIds).queryObject(self.oid)
