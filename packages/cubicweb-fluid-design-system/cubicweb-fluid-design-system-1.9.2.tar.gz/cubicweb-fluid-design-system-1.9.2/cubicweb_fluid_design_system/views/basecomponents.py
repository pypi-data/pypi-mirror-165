# -*- coding: utf-8 -*-
"""fluid_design_system implementation of base components

:organization: Logilab
:copyright: 2013 LOGILAB S.A. (Paris, FRANCE), license is LGPL.
:contact: https://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

__docformat__ = "restructuredtext en"

from logilab.common.decorators import monkeypatch
from logilab.mtconverter import xml_escape

from cubicweb import tags
from cubicweb.web.component import Link
from cubicweb.web.views import basecomponents
from cubicweb.uilib import js

from cubicweb_fluid_design_system.views import utils


basecomponents.CookieLoginComponent._html = (
    '<a class="icon-login" data-toggle="modal" href="#loginModal">%s</a>'
)


@monkeypatch(basecomponents.CookieLoginComponent)
def call(self):
    self.w(self._html, self._cw._("i18n_login_popup"))
    self._cw.add_onload(
        js.jQuery("body").append(
            self._cw.view(
                "logform",
                rset=self.cw_rset,
                id=self.loginboxid,
                klass=self.loginboxid,
                title=True,
                showmessage=False,
                showonload=False,
            )
        )
    )
    self._cw.add_onload(
        """
       $('#loginModal').on('shown.bs.modal', function () {
           $('#__login:visible').focus();
       });"""
    )


# NOTE: CW 3.18 may introduce render_messages(). This would be the
#       the only method to override
@monkeypatch(basecomponents.ApplicationMessage)  # noqa: F811
def call(self, msg=None):
    if msg is None:
        msg = self._cw.message  # XXX don't call self._cw.message twice
    if msg:
        self.w(
            '<div class="alert alert-info" id="%s">'
            '<button class="close" data-dismiss="alert" type="button">x</button>'
            " %s</div>",
            self.domid,
            msg,
            escape=False,
        )


@monkeypatch(basecomponents.ApplLogo)
def render(self, w):
    w('<a id="logo" href="%s"></a>' % self._cw.base_url())


@monkeypatch(basecomponents.ApplicationName)  # noqa: F811
def render(self, w, **kwargs):
    title = self._cw.property_value("ui.site-title")
    if title:
        w(
            '<a class="cw-site-title" href="%s">%s</a>'
            % (self._cw.base_url(), xml_escape(title))
        )


class BSAuthenticatedUserStatus(basecomponents.AuthenticatedUserStatus):
    divider_html = '<li class="divider"></li>'

    def render(self, w):
        # display useractions and siteactions
        actions = self._cw.vreg["actions"].possible_actions(
            self._cw, rset=self.cw_rset, view=self.cw_extra_kwargs["view"]
        )
        html = []
        for action in actions.get("useractions", ()):
            self.render_actions(html.append, action)
        if actions.get("useractions") and actions.get("siteactions"):
            html.append(self.divider_html)
        for action in actions.get("siteactions", ()):
            self.render_actions(html.append, action)
        title = self.generate_initial_from_user(self._cw.user)
        ddb = AUSDropDownBox(title, "\n".join(html))
        ddb.render(w=w)

    def generate_initial_from_user(self, user):
        firstname = "" if user.firstname is None else user.firstname.strip()
        lastname = "" if user.surname is None else user.surname.strip()

        if firstname and lastname:
            return lastname[0].upper() + firstname[0].upper()
        elif firstname and not lastname:
            return firstname[0].upper()
        elif not firstname and lastname:
            return lastname[0].upper()

        return user.login[:2].upper()

    def render_actions(self, w, action):
        self.action_link(action).render(w=w)

    def action_link(self, action):
        kwargs = {}
        if action.title == "logout":
            kwargs["icon"] = "logout"
        return self.link(self._cw._(action.title), action.url(), **kwargs)

    def link(self, title, url, **kwargs):
        kwargs["klass"] = "nj-list-group__item"
        return FDSLink(url, title, **kwargs)


class FDSLink(Link):

    def render(self, w):
        label = self.label
        if "icon" in self.attrs:
            label = f"<i class='material-icons mr-1'>{self.attrs['icon']}</i>{self.label}"
        w(f"<a href='{self.href}' class='{self.attrs.get('klass', '')}'>{label}</a>")


class AUSDropDownBox(utils.DropDownBox):
    def render(self, w):
        if not len(self.actions):
            return ""
        w(
            self.ul_template
            % {"title": self.title, "actions": self.actions, "klass": self.klass}
        )


class BSRQLInputForm(basecomponents.RQLInputForm):
    """build the rql input form, usually displayed in the header"""

    __regid__ = "rqlinput"
    cw_property_defs = basecomponents.VISIBLE_PROP_DEF
    visible = False
    formdef = """<form id="rqlinput" action="%s" class="%s" role="search">
    <input type="text" id="rql" name="rql" value="%s" placeholder="%s" class="form-control"
       title="%s" tabindex="%s" accesskey="q" />
    %s</form>"""

    def call(self, view=None):
        req = self._cw
        if hasattr(view, "filter_box_context_info"):
            rset = view.filter_box_context_info()[0]
        else:
            rset = self.cw_rset
        # display multilines query as one line
        rql = rset is not None and rset.printable_rql() or req.form.get("rql", "")
        rql = rql.replace("\n", " ")
        rql_suggestion_comp = self._cw.vreg["components"].select_or_none(
            "rql.suggestions", self._cw
        )
        if rql_suggestion_comp is not None:
            # enable autocomplete feature only if the rql
            # suggestions builder is available
            self._cw.add_css("jquery.ui.css")
            self._cw.add_js(("cubicweb.ajax.js", "jquery.ui.js"))
            self._cw.add_onload(
                '$("#rql").autocomplete({source: "%s"});'
                % (req.build_url("json", fname="rql_suggest"))
            )
        hidden = ""
        if req.search_state[0] != "normal":
            hidden = '<input type="hidden" name="__mode" value="%s"/>' % ":".join(
                req.search_state[1]
            )
        self.w(
            self.formdef,
            req.build_url("view"),
            not self.cw_propval("visible") and "hidden" or "",
            rql,
            req._("full text or RQL query"),
            "",
            "",
            hidden,
        )


def registration_callback(vreg):
    components = (
        (BSAuthenticatedUserStatus, basecomponents.AuthenticatedUserStatus),
        (BSRQLInputForm, basecomponents.RQLInputForm),
    )
    vreg.register_all(globals().values(), __name__, [new for (new, old) in components])
    for new, old in components:
        vreg.register_and_replace(new, old)
    vreg.unregister(basecomponents.AnonUserStatusLink)
