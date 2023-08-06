// Copyright (c) Jeremy Magland
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers
} from '@jupyter-widgets/base';

import React from 'react';
import ReactDOM from 'react-dom';
import FigureWidget from './FigureWidget';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
// import '../css/widget.css';

export class FigurlFigureModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: FigurlFigureModel.model_name,
      _model_module: FigurlFigureModel.model_module,
      _model_module_version: FigurlFigureModel.model_module_version,
      _view_name: FigurlFigureModel.view_name,
      _view_module: FigurlFigureModel.view_module,
      _view_module_version: FigurlFigureModel.view_module_version,
      view_uri: '',
      data_uri: '',
      height: 0
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'FigurlFigureModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'FigurlFigureView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class FigurlFigureView extends DOMWidgetView {
  render() {
    this.el.classList.add('custom-widget')

    this.onChange()
    this.model.on('change:view_uri', this.onChange, this)
    this.model.on('change:data_uri', this.onChange, this)
    this.model.on('change:height', this.onChange, this)
    

    // this.el.innerHTML = '<div style="position:absolute;width:300px;height:300px;background:green;" />'
  }

  onChange() {
    const viewUri = this.model.get('view_uri')
    const dataUri = this.model.get('data_uri')
    const height = this.model.get('height')
    if ((viewUri) && (dataUri)) {
      const component = React.createElement(FigureWidget, {model: this.model, viewUri, dataUri, height})
      ReactDOM.render(component, this.el)
    }
    else {
      this.el.innerHTML = '<h3>Waiting for widget properties</h3>'
    }
    // this.el.innerHTML = `
    //   <iframe src="https://www.figurl.org/f?v=gs://figurl/draculus-1&d=sha1://2b9330656b2cf1993716cd615950754945ea16d0&project=lqhzprbdrq&hide=1&label=draculus%20sortingview%20example" />
    // `;
    // this.el.textContent = this.model.get('value') + ' test4';
  }
}
