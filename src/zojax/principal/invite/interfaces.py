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
from zope import schema, interface
from zope.component.interfaces import IObjectEvent, ObjectEvent
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zojax.principal.invite')


class IInvitation(interface.Interface):

    id = interface.Attribute('Unique ID')

    expires = interface.Attribute('Expiration date')

    principal = interface.Attribute('Invited principal')

    def isExpired():
        """ invitation expired """

    def reject():
        """ reject invitation """

    def accept():
        """ accept invitation """


class IObjectInvitation(IInvitation):
    """ object invitation """

    oid = interface.Attribute('Object id')
    object = interface.Attribute('Object')


class IInvitations(interface.Interface):

    expireDays = schema.Int(
        title = _(u'Expires in days'),
        description = _(u'Invitation expiration period.'),
        default = 10,
        required = True)

    def storeInvitation(invitation):
        """ store invitation, set unique id, expires date, etc """

    def removeObject(id):
        """ remove invitations for object """

    def getInvitationsByObject(object, type=None):
        """ invitations by object """

    def getInvitationsByOwner(owner, type=None):
        """ invitations by owner """

    def getInvitationsByPrincipal(principal, type=None):
        """ invitations by principal """

    def search(**kw):
        """ search invitations """


class IInvitationsCatalog(interface.Interface):
    """ invitations catalog """


class IInvitationEvent(IObjectEvent):
    """ invitaiton event """


class IInvitationAcceptedEvent(IInvitationEvent):
    """ invitation accepted """


class IInvitationRejectedEvent(IInvitationEvent):
    """ invitation rejected """


class InvitationAcceptedEvent(ObjectEvent):
    interface.implements(IInvitationAcceptedEvent)


class InvitationRejectedEvent(ObjectEvent):
    interface.implements(IInvitationRejectedEvent)
