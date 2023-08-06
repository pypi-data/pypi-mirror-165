#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jeremy Magland.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

import os
from typing import Dict
from ipywidgets import DOMWidget
from traitlets import Unicode, Int
import kachery_cloud as kcl
from ._frontend import module_name, module_version
from kachery_cloud.TaskBackend.TaskBackend import TaskHandler
from kachery_cloud._json_stringify_deterministic import _json_stringify_deterministic
from kachery_cloud._serialize import _serialize

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
    height = Int(0).tag(sync=True)

    def __init__(self, *, view_uri: str, data_uri: str, height: int=600, download: bool=False, task_handlers: Dict[str, TaskHandler]={}):
        DOMWidget.__init__(self)

        def on_message(widget, content, buffers):
            widget.send({'type': 'reply', 'message': content})
            type0 = content['type']
            if type0 == 'loadFileDataRequest':
                uri = content['uri']
                x = kcl.load_text(uri, local_only=(not download))
                resp = {'type': 'loadFileDataResponse', 'uri': uri}
                if x is not None:
                    resp['fileData'] = x
                widget.send(resp)
            elif type0 == 'loadTaskReturnValue':
                task_name = content['taskName']
                task_job_id = content['taskJobId']
                s = task_job_id
                fname = f'{kcl.get_kachery_cloud_dir()}/task_results/{task_name}/{s[0]}{s[1]}/{s[2]}{s[3]}/{s[4]}{s[5]}/{s}'
                if os.path.exists(fname):
                    with open(fname, 'r') as f:
                        data = f.read()
                else:
                    data = None
                resp = {'type': 'loadTaskReturnValueResponse', 'taskName': task_name, 'taskJobId': task_job_id}
                if data is not None:
                    resp['data'] = data
                widget.send(resp)
            elif type0 == 'requestTask':
                task_type = content['taskType']
                task_name = content['taskName']
                task_input = content['taskInput']
                task_job_id = content['taskJobId']
                if task_type == 'calculation':
                    th = task_handlers.get(task_name, None)
                    try:
                        if th is None:
                            raise Exception('Task handler not found')
                        result = th.run_task(task_input=task_input)
                        if result is None:
                            raise Exception('Result is None')
                        result_serialized = _serialize(result)
                        result_text = _json_stringify_deterministic(result_serialized)                            
                        s = task_job_id
                        fname = f'{kcl.get_kachery_cloud_dir()}/task_results/{task_name}/{s[0]}{s[1]}/{s[2]}{s[3]}/{s[4]}{s[5]}/{s}'
                        parent_dir = os.path.dirname(fname)
                        if not os.path.exists(parent_dir):
                            os.makedirs(parent_dir)
                        with open(fname, 'w') as f:
                            f.write(result_text)
                    except Exception as err:
                        widget.send({
                            'type': 'taskStatusUpdate',
                            'taskType': task_type,
                            'taskName': task_name,
                            'taskJobId': task_job_id,
                            'status': 'error',
                            'error': str(err)
                        })
                        return
                    widget.send({
                        'type': 'taskStatusUpdate',
                        'taskType': task_type,
                        'taskName': task_name,
                        'taskJobId': task_job_id,
                        'status': 'finished'
                    })

        self.on_msg(on_message)

        self._view_uri = view_uri
        self._data_uri = data_uri
        self._height = height
        self.set_trait('view_uri', view_uri)
        self.set_trait('data_uri', data_uri)
        self.set_trait('height', height)

