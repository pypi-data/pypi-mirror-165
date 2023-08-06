#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jeremy Magland.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from traitlets import Unicode
import kachery_cloud as kcl
from ._frontend import module_name, module_version


class FigurlFigure(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('FigurlFigureModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('FigurlFigureView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    # traitlets
    view_uri = Unicode('').tag(sync=True)
    data_uri = Unicode('').tag(sync=True)

    def __init__(self, *, view_uri: str, data_uri: str, download: bool=False):
        DOMWidget.__init__(self)

        def on_message(widget, content, buffers):
            widget.send({'type': 'reply', 'message': content})
            type0 = content['type']
            if type0 == 'loadFileDataRequest':
                uri = content['uri']
                x = kcl.load_text(uri, local_only=(not download))
                if x is not None:
                    widget.send({'type': 'loadFileDataResponse', 'uri': uri, 'fileData': x})
        self.on_msg(on_message)

        self._view_uri = view_uri
        self._data_uri = data_uri
        self.set_trait('view_uri', view_uri)
        self.set_trait('data_uri', data_uri)

