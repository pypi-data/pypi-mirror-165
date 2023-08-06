# -*- coding: utf-8 -*-
"""fluid_design_system implementation of startup views

:organization: Logilab
:copyright: 2013 LOGILAB S.A. (Paris, FRANCE), license is LGPL.
:contact: https://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

__docformat__ = "restructuredtext en"

from logilab.common.decorators import monkeypatch
from logilab.common.textutils import unormalize
from logilab.mtconverter import xml_escape

from cubicweb.web.views import startup, uicfg

startup.ManageView.box_html = """<div class="panel panel-default">
    <div class="panel-heading">
        <div class="panel-title">%s</div>
    </div>
    <div class="panel-body">%s</div>
    </div>"""


@monkeypatch(startup.ManageView)
def manage_actions(self):
    allactions = self._cw.vreg["actions"].possible_actions(self._cw)
    if allactions.get("manage"):
        html = []
        html.append("<ul>")
        for action in allactions["manage"]:
            html.append(
                '<li><a href="%s">%s</a></li>'
                % (action.url(), self._cw._(action.title))
            )
        html.append("</ul>")
        self.w(
            self.box_html,
            self._cw._("Manage"),
            "\n".join(html),
            escape=False,
        )


@monkeypatch(startup.ManageView)
def startup_views(self):
    views = [
        v
        for v in self._cw.vreg["views"].possible_views(self._cw, None)
        if v.category == "startupview" and v.__regid__ not in self.skip_startup_views
    ]
    if not views:
        return
    html = []
    html.append("<ul>")
    for v in sorted(views, key=lambda x: self._cw._(x.title)):
        html.append(
            '<li><a href="%s">%s</a></li>'
            % (xml_escape(v.url()), xml_escape(self._cw._(v.title).capitalize()))
        )
    html.append("</ul>")
    self.w(
        self.box_html,
        self._cw._("Startup views"),
        "\n".join(html),
        escape=False,
    )


@monkeypatch(startup.ManageView)
def entities(self):
    schema = self._cw.vreg.schema
    eschemas = [
        eschema
        for eschema in schema.entities()
        if uicfg.indexview_etype_section.get(eschema) == "application"
    ]
    if eschemas:
        html = self.entity_types_table(eschemas)
        self.w(
            self.box_html,
            self._cw._("Browse by entity type"),
            "\n".join(html),
            escape=False,
        )


@monkeypatch(startup.ManageView)
def entity_types_table(self, eschemas):
    infos = sorted(self.entity_types(eschemas), key=lambda t: unormalize(t[0]))
    q, r = divmod(len(infos), 2)
    html = []
    html.append('<div class="row">')
    for links in (infos[: q + r], infos[q + r :]):
        if links:
            html.append('<div class="col-md-6">')
            html.append('<ul class="list-unstyled">')
            for (_, etypelink, addlink) in links:
                html.append("<li>%s %s</li>" % (addlink, etypelink))
            html.append("</ul>")
            html.append("</div>")
    html.append("</div>")
    return html
