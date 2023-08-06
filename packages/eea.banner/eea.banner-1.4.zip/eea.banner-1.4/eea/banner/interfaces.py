"""Module where all interfaces, events and exceptions live."""
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from eea.banner import EEAMessageFactory as _


class IEeaBannerLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IBannerSettings(Interface):
    """Client settings for EEA Banner."""

    static_banner_enabled = schema.Bool(
        title=_(u"Enable / disable static banner"),
        description=_(
            u"If STATIC_BANNER_ENABLED environment variable is 'on' "
            u"this flag has no effect"
        ),
        default=True,
        required=False,
    )

    static_banner_visible_to_all = schema.Bool(
        title=_(u"Show static banner to anonymous users?"),
        default=True,
        required=False,
    )

    static_banner_type = schema.Choice(
        title=_(u"Static banner type"),
        default="warning",
        vocabulary=SimpleVocabulary.fromValues(
            ["success", "warning", "error"]
        ),
    )

    static_banner_title = schema.TextLine(
        title=_(u"Static banner title"),
        default=u"This is a demo/test instance",
        required=False,
    )

    static_banner_message = schema.Text(
        title=_(u"Static banner message"),
        required=False,
        default=(
            u"Do not use it for operational purposes. "
            u"All changes will be regularly overwritten"
        ),
    )

    dynamic_banner_enabled = schema.Bool(
        title=_(u"Enable / disable dynamic banner"),
        default=True,
        required=False,
        description=_(
            u"It will appear only if status of at least one stack "
            u"is not 'active'. "
            u"If STATIC_BANNER_ENABLED environment variable is 'on' "
            u"this flag has no effect"
        ),
    )

    dynamic_banner_visible_to_all = schema.Bool(
        title=_(u"Show dynamic banner to anonymous users?"),
        default=True,
        required=False,
    )

    rancher_stacks = schema.List(
        title=_(u"Rancher stacks to monitor"),
        default=[],
        required=False,
        value_type=schema.TextLine(),
    )

    dynamic_banner_title = schema.TextLine(
        title=_(u"Dynamic banner title"),
        default=u"Web admins says:",
        required=False,
    )

    dynamic_banner_message = schema.Text(
        title=_(u"Dynamic banner message"),
        required=False,
        default=u"The system is {}",
        description=(
            u"Add suffix/prefix to rancher stacks status message. "
            u"Use {} for rancher stacks status placeholder"
        ),
    )
