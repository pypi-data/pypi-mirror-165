# -*- coding: utf-8 -*-
"""fluid_design_system html helpers

:organization: Logilab
:copyright: 2013 LOGILAB S.A. (Paris, FRANCE), license is LGPL.
:contact: https://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

__docformat__ = "restructuredtext en"


class DropDownBox(object):
    ul_template = """
    <div class="nj-avatar nj-avatar--sm">
        <div class="nj-avatar__picture" data-toggle="collapse" href="#dropdownMenu" aria-expanded="false" aria-controls="dropdownMenu" role="button">
            <div class="nj-avatar__initials">%(title)s</div>
        </div>
        <div class="nj-collapse" id="dropdownMenu">
            <ul class="dropdown-menu nj-list-group nj-list-group--sm nj-list-group--no-border" role="menu">%(actions)s</ul>
        </div>
    </div>"""

    li_template = "<li>%(link)s<li>"

    def __init__(self, title, actions, klass=""):
        self.title = title
        self.actions = actions
        self.klass = klass

    def render(self, w):
        if not len(self.actions):
            return ""
        w(
            self.ul_template
            % {
                "title": self.title,
                "actions": "".join(self.render_items()),
            }
        )

    def render_items(self):
        for item in self.actions:
            yield self.li_template % {"link": self._item_value(item)}

    def _item_value(self, item):
        return item
