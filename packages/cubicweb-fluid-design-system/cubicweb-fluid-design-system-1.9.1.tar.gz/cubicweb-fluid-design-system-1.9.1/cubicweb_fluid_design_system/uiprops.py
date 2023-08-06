"""
:copyright 2012 CreaLibre (Monterrey, MEXICO), all rights reserved.
:contact http://www.crealibre.com/ -- mailto:info@crealibre.com

:organization: Logilab
:copyright: 2013 LOGILAB S.A. (Paris, FRANCE), license is LGPL.
:contact: https://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
# flake8: noqa

import pathlib


STYLESHEETS = [
    data("css/bootstrap.min.css"),
    data("css/fix.css"),
    data("cubes.bootstrap.css"),
    data("cubicweb.pictograms.css"),
    "https://cdn.jsdelivr.net/npm/@engie-group/fluid-design-system@latest/lib/fluid-design-system.css",
    "https://fonts.googleapis.com/css?family=Material+Icons|Lato:300,400,700,900&display=swap",
]

CW_COMPAT_STYLESHEETS = [data("cubes.bootstrap.cw_compat.css")]

JAVASCRIPTS.extend(
    (
        data("js/bootstrap.min.js"),
        data("cubes.bootstrap.js"),
        data("cubes.squareui.js"),
        "https://cdn.jsdelivr.net/npm/@engie-group/fluid-design-system@latest/lib/fluid-design-system.js",
        "https://cdn.jsdelivr.net/npm/@engie-group/fluid-design-system@latest/lib/auto-init.js",
    )
)
