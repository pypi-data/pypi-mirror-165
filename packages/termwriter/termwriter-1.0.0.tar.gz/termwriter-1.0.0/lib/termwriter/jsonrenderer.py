__copyright__ = "Copyright 2019-2022 Mark Kim"
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__author__ = "Mark Kim"
__all__ = [ "JsonRenderer" ]

import json


class JsonRenderer:
    def __init__(self, **opts):
        self.opts = opts

    def __call__(self, widget):
        if hasattr(widget, "jsonable"):
            jsonable = widget.jsonable()
        else:
            jsonable = widget

        return json.dumps(jsonable, **self.opts)

