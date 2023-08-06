# pylint: disable=W0622
"""cubicweb-fluid-design-system application packaging information"""

modname = "fluid_design_system"
distname = "cubicweb-fluid-design-system"

numversion = (1, 9, 2)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = ""
web = "https://www.cubicweb.org/project/%s" % distname

__depends__ = {
    "cubicweb": ">= 3.35.0",
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: JavaScript",
]
