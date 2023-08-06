"use strict";
(self["webpackChunkfigurl_jupyter"] = self["webpackChunkfigurl_jupyter"] || []).push([["lib_widget_js"],{

/***/ "./lib/FigInterface.js":
/*!*****************************!*\
  !*** ./lib/FigInterface.js ***!
  \*****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __classPrivateFieldSet = (this && this.__classPrivateFieldSet) || function (receiver, privateMap, value) {
    if (!privateMap.has(receiver)) {
        throw new TypeError("attempted to set private field on non-instance");
    }
    privateMap.set(receiver, value);
    return value;
};
var __classPrivateFieldGet = (this && this.__classPrivateFieldGet) || function (receiver, privateMap) {
    if (!privateMap.has(receiver)) {
        throw new TypeError("attempted to get private field on non-instance");
    }
    return privateMap.get(receiver);
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
var _viewUrl;
Object.defineProperty(exports, "__esModule", ({ value: true }));
const deserializeReturnValue_1 = __importDefault(__webpack_require__(/*! ./deserializeReturnValue */ "./lib/deserializeReturnValue.js"));
const MessageToParentTypes_1 = __webpack_require__(/*! ./viewInterface/MessageToParentTypes */ "./lib/viewInterface/MessageToParentTypes.js");
const urlFromUri_1 = __importDefault(__webpack_require__(/*! ./util/urlFromUri */ "./lib/util/urlFromUri.js"));
class FigInterface {
    constructor(a) {
        this.a = a;
        _viewUrl.set(this, void 0);
        this.a.electronInterface.onTaskStatusUpdate(({ taskType, taskName, taskJobId, status, errorMessage }) => {
            ;
            (() => __awaiter(this, void 0, void 0, function* () {
                let returnValue = undefined;
                if (status === 'finished') {
                    if (taskType === 'calculation') {
                        returnValue = yield this.a.electronInterface.getTaskReturnValue({ taskName, taskJobId });
                        if (returnValue === undefined) {
                            console.warn(taskName, taskJobId);
                            console.warn('Unexpected... calculation task is finished, but not able to load return value');
                            return;
                        }
                        // deserialize data here rather than in preload
                        // because Buffer may behave differently in preload
                        returnValue = yield deserializeReturnValue_1.default(returnValue);
                    }
                }
                this._sendMessageToChild({
                    type: 'taskStatusUpdate',
                    taskJobId,
                    status,
                    errorMessage,
                    returnValue
                });
            }))();
        });
        window.addEventListener('message', e => {
            const msg = e.data;
            if (msg.figureId !== this.a.figureId)
                return;
            if (MessageToParentTypes_1.isMessageToParent(msg)) {
                console.log('--- got message to parent', msg);
                if (msg.type === 'figurlRequest') {
                    this.a.electronInterface.handleFigurlRequest(msg.request).then(resp => {
                        ;
                        (() => __awaiter(this, void 0, void 0, function* () {
                            if (resp) {
                                // deserialize data here rather than in preload
                                // because Buffer may behave differently in preload
                                if (resp.type === 'getFigureData') {
                                    resp.figureData = yield deserializeReturnValue_1.default(resp.figureData);
                                }
                                if (resp.type === 'getFileData') {
                                    resp.fileData = yield deserializeReturnValue_1.default(resp.fileData);
                                }
                                if (resp.type === 'initiateTask') {
                                    if (resp.returnValue) {
                                        resp.returnValue = yield deserializeReturnValue_1.default(resp.returnValue);
                                    }
                                }
                                this._sendMessageToChild({
                                    type: 'figurlResponse',
                                    requestId: msg.requestId,
                                    response: resp
                                });
                            }
                            else {
                                console.warn('Did not handle request', msg.request.type);
                            }
                        }))();
                    });
                }
            }
        });
    }
    initialize(queryParameters) {
        return __awaiter(this, void 0, void 0, function* () {
            __classPrivateFieldSet(this, _viewUrl, queryParameters.viewUri ? urlFromUri_1.default(queryParameters.viewUri) : undefined);
            yield this.a.electronInterface.setQueryParameters(queryParameters);
        });
    }
    _sendMessageToChild(msg) {
        if (!this.a.iframeElement.current) {
            setTimeout(() => {
                // keep trying until iframe element exists
                this._sendMessageToChild(msg);
            }, 1000);
            return;
        }
        const cw = this.a.iframeElement.current.contentWindow;
        if (!cw)
            return;
        if (!__classPrivateFieldGet(this, _viewUrl)) {
            throw Error('No viewUrl in _sendMessageToChild');
        }
        cw.postMessage(msg, urlFromUri_1.default(__classPrivateFieldGet(this, _viewUrl)));
    }
}
_viewUrl = new WeakMap();
exports["default"] = FigInterface;
//# sourceMappingURL=FigInterface.js.map

/***/ }),

/***/ "./lib/FigureWidget.js":
/*!*****************************!*\
  !*** ./lib/FigureWidget.js ***!
  \*****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const jsx_runtime_1 = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
const react_1 = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
const FigInterface_1 = __importDefault(__webpack_require__(/*! ./FigInterface */ "./lib/FigInterface.js"));
const randomAlphaString_1 = __importDefault(__webpack_require__(/*! ./util/randomAlphaString */ "./lib/util/randomAlphaString.js"));
const urlFromUri_1 = __importDefault(__webpack_require__(/*! ./util/urlFromUri */ "./lib/util/urlFromUri.js"));
const parentOrigin = window.location.protocol + '//' + window.location.host;
const createElectronInterface_1 = __importDefault(__webpack_require__(/*! ./createElectronInterface */ "./lib/createElectronInterface.js"));
const sleepMsec_1 = __webpack_require__(/*! ./sleepMsec */ "./lib/sleepMsec.js");
const FigureWidget = ({ model, viewUri, dataUri, height }) => {
    const [width, setWidth] = react_1.useState(undefined);
    const iframeElement = react_1.useRef();
    const viewUrlBase = urlFromUri_1.default(viewUri);
    const viewUrl = viewUrlBase + '/index.html';
    const [figInterface, setFigInterface] = react_1.useState(undefined);
    // we need a unique figure ID for each figure interface
    const figureId = react_1.useMemo(() => (randomAlphaString_1.default(10)), []);
    const src = react_1.useMemo(() => {
        let ret = `${viewUrl}?parentOrigin=${parentOrigin}&figureId=${figureId}`;
        return ret;
    }, [parentOrigin, viewUrl]);
    react_1.useEffect(() => {
        const queryParameters = {
            viewUri,
            dataUri
        };
        const electronInterface = createElectronInterface_1.default(model);
        const figInterface = new FigInterface_1.default({ electronInterface, figureId, iframeElement });
        figInterface.initialize(queryParameters).then(() => {
            setFigInterface(figInterface);
        });
    }, [viewUri, dataUri, iframeElement, figureId, model]);
    react_1.useEffect(() => {
        function findAncestorElementWithClass(elmt, className) {
            if (!elmt)
                return undefined;
            if (elmt.className.split(' ').includes(className))
                return elmt;
            return findAncestorElementWithClass(elmt.parentElement || undefined, className);
        }
        function findDescendantElementWithClass(elmt, className) {
            if (!elmt)
                return undefined;
            if (elmt.className.split(' ').includes(className))
                return elmt;
            const childElements = elmt.children;
            for (let i = 0; i < childElements.length; i++) {
                const childElement = childElements[i];
                const d = findDescendantElementWithClass(childElement, className);
                if (d)
                    return d;
            }
            return undefined;
        }
        let canceled = false;
        (() => __awaiter(void 0, void 0, void 0, function* () {
            var _a, _b;
            let delay = 100; // start with a short delay and work up
            let lastWidth = 0;
            while (!canceled) {
                // It is tricky to compute the width properly
                // After thoroughly inspecting the DOM, I think this is the best way
                const outputArea = findAncestorElementWithClass(iframeElement.current || undefined, 'jp-Cell-outputArea');
                const outputAreaPrompt = findDescendantElementWithClass(outputArea, 'jp-OutputArea-prompt');
                const W1 = (_a = outputArea === null || outputArea === void 0 ? void 0 : outputArea.getBoundingClientRect()) === null || _a === void 0 ? void 0 : _a.width;
                const W2 = (_b = outputAreaPrompt === null || outputAreaPrompt === void 0 ? void 0 : outputAreaPrompt.getBoundingClientRect()) === null || _b === void 0 ? void 0 : _b.width;
                if ((W1) && (W2)) {
                    const newWidth = W1 - W2;
                    if (newWidth !== lastWidth) {
                        lastWidth = newWidth;
                        delay = 500; // detect rapidly once again
                        setWidth(newWidth);
                    }
                }
                yield sleepMsec_1.sleepMsec(delay);
                delay += 100;
                if (delay > 5000)
                    delay = 5000;
            }
        }))();
        return () => { canceled = true; };
    }, [iframeElement]);
    const H = height || 400;
    return (
    // important to use relative position rather than absolute (took me a while to figure that out)
    jsx_runtime_1.jsx("div", Object.assign({ style: { position: 'relative', width: width || 0, height: H, overflow: 'hidden' } }, { children: jsx_runtime_1.jsx("iframe", { ref: e => { iframeElement.current = e; }, title: "figure", src: src, width: width ? width - 15 : 0, height: H - 15 }, void 0) }), void 0));
};
exports["default"] = FigureWidget;
//# sourceMappingURL=FigureWidget.js.map

/***/ }),

/***/ "./lib/createElectronInterface.js":
/*!****************************************!*\
  !*** ./lib/createElectronInterface.js ***!
  \****************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const randomAlphaString_1 = __importDefault(__webpack_require__(/*! ./util/randomAlphaString */ "./lib/util/randomAlphaString.js"));
const kacheryTypes_1 = __webpack_require__(/*! ./viewInterface/kacheryTypes */ "./lib/viewInterface/kacheryTypes.js");
const createElectronInterface = (model) => {
    let queryParameters = {};
    const setQueryParameters = (q) => __awaiter(void 0, void 0, void 0, function* () {
        queryParameters = q;
    });
    const taskStatusUpdateCallbacks = [];
    const loadFileDataCallbacks = {};
    const onFileData = (uri, callback) => {
        if (!loadFileDataCallbacks[uri])
            loadFileDataCallbacks[uri] = [];
        loadFileDataCallbacks[uri].push(callback);
    };
    const loadTaskReturnValueCallbacks = {};
    const onTaskReturnValue = (o, callback) => {
        const { taskName, taskJobId } = o;
        const key = `${taskName}.${taskJobId}`;
        if (!loadTaskReturnValueCallbacks[key])
            loadTaskReturnValueCallbacks[key] = [];
        loadTaskReturnValueCallbacks[key].push(callback);
    };
    model.on('msg:custom', msg => {
        console.info('Message from python', msg);
        if (msg.type === 'loadFileDataResponse') {
            const { fileData, uri } = msg;
            const callbacks = loadFileDataCallbacks[uri];
            if (callbacks) {
                loadFileDataCallbacks[uri] = [];
                for (let cb of callbacks) {
                    cb(fileData);
                }
            }
        }
        else if (msg.type === 'loadTaskReturnValueResponse') {
            const { data, taskName, taskJobId } = msg;
            const key = `${taskName}.${taskJobId}`;
            const callbacks = loadTaskReturnValueCallbacks[key];
            if (callbacks) {
                loadTaskReturnValueCallbacks[key] = [];
                for (let cb of callbacks) {
                    cb(data);
                }
            }
        }
        else if (msg.type === 'taskStatusUpdate') {
            const { taskType, taskName, taskJobId, status, error } = msg;
            for (let cb of taskStatusUpdateCallbacks) {
                cb({ taskType, taskName, taskJobId, status, errorMessage: error });
            }
        }
    });
    function loadFileData(uri) {
        return __awaiter(this, void 0, void 0, function* () {
            model.send({ type: 'loadFileDataRequest', uri }, () => { });
            return new Promise((resolve, reject) => {
                onFileData(uri, (fileData) => {
                    resolve(fileData ? JSON.parse(fileData) : undefined);
                });
            });
        });
    }
    function getTaskReturnValue(o) {
        return __awaiter(this, void 0, void 0, function* () {
            const { taskName, taskJobId } = o;
            model.send({ type: 'loadTaskReturnValue', taskName, taskJobId }, () => { });
            return new Promise((resolve, reject) => {
                onTaskReturnValue({ taskName, taskJobId }, (data) => {
                    resolve(data ? JSON.parse(data) : undefined);
                });
            });
        });
    }
    const handleFigurlRequest = (req) => __awaiter(void 0, void 0, void 0, function* () {
        if (req.type === 'getFigureData') {
            if (!queryParameters.dataUri)
                throw Error('dataUri is not set in preload.ts');
            const figureData = yield loadFileData(queryParameters.dataUri);
            return {
                type: 'getFigureData',
                figureData
            };
        }
        else if (req.type === 'getFileData') {
            const fileData = yield loadFileData(req.uri);
            return {
                type: 'getFileData',
                fileData
            };
        }
        else if (req.type === 'initiateTask') {
            const { taskInput, taskName, taskType } = req;
            const taskJobId = taskType === 'calculation' ? (kacheryTypes_1.sha1OfObject({ taskName, taskInput })) : (kacheryTypes_1.sha1OfString(randomAlphaString_1.default(100)));
            if (taskType === 'calculation') {
                // see if already finished
                const returnValue = yield getTaskReturnValue({ taskName, taskJobId: taskJobId.toString() });
                if (returnValue !== undefined) {
                    // already finished, no pubsub needed
                    return {
                        type: 'initiateTask',
                        taskJobId: taskJobId.toString(),
                        status: 'finished',
                        returnValue
                    };
                }
            }
            model.send({ type: 'requestTask', taskType, taskName, taskInput, taskJobId }, () => { });
            const ret = {
                type: 'initiateTask',
                taskJobId: taskJobId.toString(),
                status: 'waiting'
            };
            return ret;
        }
        else
            return undefined;
    });
    const onTaskStatusUpdate = (callback) => {
        taskStatusUpdateCallbacks.push(callback);
    };
    return {
        setQueryParameters,
        handleFigurlRequest,
        onTaskStatusUpdate,
        getTaskReturnValue
    };
};
exports["default"] = createElectronInterface;
//# sourceMappingURL=createElectronInterface.js.map

/***/ }),

/***/ "./lib/deserializeReturnValue.js":
/*!***************************************!*\
  !*** ./lib/deserializeReturnValue.js ***!
  \***************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const zlib = __importStar(__webpack_require__(/*! zlib */ "webpack/sharing/consume/default/zlib/zlib"));
const deserializeReturnValue = (x) => __awaiter(void 0, void 0, void 0, function* () {
    if (!x)
        return x;
    else if (typeof (x) === 'object') {
        if (Array.isArray(x)) {
            const ret = [];
            for (let a of x) {
                ret.push(yield deserializeReturnValue(a));
            }
            return ret;
        }
        else if (x._type === 'ndarray') {
            const shape = x.shape;
            const dtype = x.dtype;
            // let dataBuffer: Buffer
            let dataBuffer;
            if (x.data_b64) {
                const data_b64 = x.data_b64;
                dataBuffer = _base64ToArrayBuffer(data_b64);
                // dataBuffer = Buffer.from(data_b64, 'base64')
            }
            else if (x.data_gzip_b64) {
                const data_gzip_b64 = x.data_gzip_b64;
                const aa = _base64ToArrayBuffer(data_gzip_b64);
                // const aa = Buffer.from(data_gzip_b64, 'base64')
                dataBuffer = yield gunzipAsync(aa);
            }
            else {
                throw Error('Missing data_b64 or data_gzip_b64');
            }
            // const data_b64 = x.data_b64 as string
            // const dataBuffer = _base64ToArrayBuffer(data_b64)
            if (dtype === 'float32') {
                return applyShape(new Float32Array(dataBuffer), shape);
            }
            else if (dtype === 'int32') {
                return applyShape(new Int32Array(dataBuffer), shape);
            }
            else if (dtype === 'int16') {
                return applyShape(new Int16Array(dataBuffer), shape);
            }
            else if (dtype === 'uint8') {
                return applyShape(new Uint8Array(dataBuffer), shape);
            }
            else if (dtype === 'uint32') {
                return applyShape(new Uint32Array(dataBuffer), shape);
            }
            else if (dtype === 'uint16') {
                return applyShape(new Uint16Array(dataBuffer), shape);
            }
            else if (dtype === 'float64') {
                if (shapeProduct(shape) > 100) {
                    console.info('WARNING: Using float64 array. It may be a good idea to cast the array to float32 if you do not need the full precision', shape);
                }
                return applyShape(new Float64Array(dataBuffer), shape);
            }
            else {
                throw Error(`Datatype not yet implemented for ndarray: ${dtype}`);
            }
        }
        else {
            const ret = {};
            for (let k in x) {
                ret[k] = yield deserializeReturnValue(x[k]);
            }
            return ret;
        }
    }
    else
        return x;
});
const shapeProduct = (shape) => {
    let ret = 1;
    for (let a of shape)
        ret *= a;
    return ret;
};
const gunzipAsync = (x) => __awaiter(void 0, void 0, void 0, function* () {
    return new Promise((resolve, reject) => {
        zlib.inflate(x, (err, y) => {
            if (err) {
                reject(err);
                return;
            }
            resolve(y);
        });
    });
});
const applyShape = (x, shape) => {
    if (shape.length === 1) {
        if (shape[0] !== x.length)
            throw Error('Unexpected length of array');
        return Array.from(x);
    }
    else if (shape.length === 2) {
        const n1 = shape[0];
        const n2 = shape[1];
        if (n1 * n2 !== x.length)
            throw Error(`Unexpected length of array ${n1} x ${n2} <> ${x.length}`);
        const ret = [];
        for (let i1 = 0; i1 < n1; i1++) {
            ret.push(Array.from(x.slice(i1 * n2, (i1 + 1) * n2)));
        }
        return ret;
    }
    else if (shape.length === 3) {
        const n1 = shape[0];
        const n2 = shape[1];
        const n3 = shape[2];
        if (n1 * n2 * n3 !== x.length)
            throw Error('Unexpected length of array');
        const ret = [];
        for (let i1 = 0; i1 < n1; i1++) {
            const A = [];
            for (let i2 = 0; i2 < n2; i2++) {
                A.push(Array.from(x.slice(i1 * n2 * n3 + i2 * n3, i1 * n2 * n3 + (i2 + 1) * n3)));
            }
            ret.push(A);
        }
        return ret;
    }
    else if (shape.length === 4) {
        const n1 = shape[0];
        const n2 = shape[1];
        const n3 = shape[2];
        const n4 = shape[3];
        if (n1 * n2 * n3 * n4 !== x.length)
            throw Error('Unexpected length of array');
        const ret = [];
        for (let i1 = 0; i1 < n1; i1++) {
            const A = [];
            for (let i2 = 0; i2 < n2; i2++) {
                const B = [];
                for (let i3 = 0; i3 < n3; i3++) {
                    B.push(Array.from(x.slice(i1 * n2 * n3 * n4 + i2 * n3 * n4 + i3 * n4, i1 * n2 * n3 * n4 + i2 * n3 * n4 + (i3 + 1) * n4)));
                }
                A.push(B);
            }
            ret.push(A);
        }
        return ret;
    }
    else if (shape.length === 5) {
        const n1 = shape[0];
        const n2 = shape[1];
        const n3 = shape[2];
        const n4 = shape[3];
        const n5 = shape[4];
        if (n1 * n2 * n3 * n4 * n5 !== x.length)
            throw Error('Unexpected length of array');
        const ret = [];
        for (let i1 = 0; i1 < n1; i1++) {
            const A = [];
            for (let i2 = 0; i2 < n2; i2++) {
                const B = [];
                for (let i3 = 0; i3 < n3; i3++) {
                    const C = [];
                    for (let i4 = 0; i4 < n4; i4++) {
                        C.push(Array.from(x.slice(i1 * n2 * n3 * n4 * n5 + i2 * n3 * n4 * n5 + i3 * n4 * n5 + i4 * n5, i1 * n2 * n3 * n4 * n5 + i2 * n3 * n4 * n5 + i3 * n4 * n5 + (i4 + 1) * n5)));
                    }
                    B.push(C);
                }
                A.push(B);
            }
            ret.push(A);
        }
        return ret;
    }
    else {
        throw Error('Not yet implemented');
    }
};
const _base64ToArrayBuffer = (base64) => {
    var binary_string = window.atob(base64);
    var len = binary_string.length;
    var bytes = new Uint8Array(len);
    for (var i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes.buffer;
};
exports["default"] = deserializeReturnValue;
//# sourceMappingURL=deserializeReturnValue.js.map

/***/ }),

/***/ "./lib/sleepMsec.js":
/*!**************************!*\
  !*** ./lib/sleepMsec.js ***!
  \**************************/
/***/ (function(__unused_webpack_module, exports) {


var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.sleepMsecNum = exports.sleepMsec = void 0;
const sleepMsec = (msec, continueFunction = undefined) => __awaiter(void 0, void 0, void 0, function* () {
    return yield exports.sleepMsecNum(msec, continueFunction);
});
exports.sleepMsec = sleepMsec;
const sleepMsecNum = (msec, continueFunction = undefined) => __awaiter(void 0, void 0, void 0, function* () {
    const m = msec;
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve();
        }, m);
    });
});
exports.sleepMsecNum = sleepMsecNum;
//# sourceMappingURL=sleepMsec.js.map

/***/ }),

/***/ "./lib/util/randomAlphaString.js":
/*!***************************************!*\
  !*** ./lib/util/randomAlphaString.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
const randomAlphaString = (num_chars) => {
    if (!num_chars) {
        /* istanbul ignore next */
        throw Error('randomAlphaString: num_chars needs to be a positive integer.');
    }
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    for (var i = 0; i < num_chars; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
};
exports["default"] = randomAlphaString;
//# sourceMappingURL=randomAlphaString.js.map

/***/ }),

/***/ "./lib/util/urlFromUri.js":
/*!********************************!*\
  !*** ./lib/util/urlFromUri.js ***!
  \********************************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
const urlFromUri = (uri) => {
    if (uri.startsWith('gs://')) {
        const p = uri.slice("gs://".length);
        return `https://storage.googleapis.com/${p}`;
    }
    else
        return uri;
};
exports["default"] = urlFromUri;
//# sourceMappingURL=urlFromUri.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// Copyright (c) Jeremy Magland
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/viewInterface/FigurlRequestTypes.js":
/*!*************************************************!*\
  !*** ./lib/viewInterface/FigurlRequestTypes.js ***!
  \*************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.isFigurlResponse = exports.isFigurlRequest = exports.isSetUrlStateResponse = exports.isSetUrlStateRequest = exports.isStoreFileResponse = exports.isStoreFileRequest = exports.isSubscribeToFeedResponse = exports.isSubscribeToFeedRequest = exports.isInitiateTaskResponse = exports.isInitiateTaskRequest = exports.isGetMutableResponse = exports.isGetMutableRequest = exports.isGetFileDataUrlResponse = exports.isGetFileDataUrlRequest = exports.isGetFileDataResponse = exports.isGetFileDataRequest = exports.isGetFigureDataResponse = exports.isGetFigureDataRequest = void 0;
const MessageToChildTypes_1 = __webpack_require__(/*! ./MessageToChildTypes */ "./lib/viewInterface/MessageToChildTypes.js");
const validateObject_1 = __importStar(__webpack_require__(/*! ./validateObject */ "./lib/viewInterface/validateObject.js"));
const isGetFigureDataRequest = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('getFigureData')
    });
};
exports.isGetFigureDataRequest = isGetFigureDataRequest;
const isGetFigureDataResponse = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('getFigureData'),
        figureData: () => (true)
    });
};
exports.isGetFigureDataResponse = isGetFigureDataResponse;
const isGetFileDataRequest = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('getFileData'),
        uri: validateObject_1.optional(validateObject_1.isString)
    });
};
exports.isGetFileDataRequest = isGetFileDataRequest;
const isGetFileDataResponse = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('getFileData'),
        fileData: () => (true)
    });
};
exports.isGetFileDataResponse = isGetFileDataResponse;
const isGetFileDataUrlRequest = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('getFileDataUrl'),
        uri: validateObject_1.optional(validateObject_1.isString)
    });
};
exports.isGetFileDataUrlRequest = isGetFileDataUrlRequest;
const isGetFileDataUrlResponse = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('getFileDataUrl'),
        fileDataUrl: validateObject_1.isString
    });
};
exports.isGetFileDataUrlResponse = isGetFileDataUrlResponse;
const isGetMutableRequest = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('getMutable'),
        key: validateObject_1.isString
    });
};
exports.isGetMutableRequest = isGetMutableRequest;
const isGetMutableResponse = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('getMutable'),
        value: validateObject_1.isOneOf([validateObject_1.isNull, validateObject_1.isString])
    });
};
exports.isGetMutableResponse = isGetMutableResponse;
const isInitiateTaskRequest = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('initiateTask'),
        taskName: validateObject_1.isString,
        taskInput: () => (true),
        taskType: MessageToChildTypes_1.isTaskType
    });
};
exports.isInitiateTaskRequest = isInitiateTaskRequest;
const isInitiateTaskResponse = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('initiateTask'),
        taskJobId: validateObject_1.isString,
        status: MessageToChildTypes_1.isTaskJobStatus,
        errorMessage: validateObject_1.optional(validateObject_1.isString),
        returnValue: validateObject_1.optional(() => (true)),
        returnValueUrl: validateObject_1.optional(validateObject_1.isString)
    });
};
exports.isInitiateTaskResponse = isInitiateTaskResponse;
const isSubscribeToFeedRequest = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('subscribeToFeed'),
        feedId: validateObject_1.isString
    });
};
exports.isSubscribeToFeedRequest = isSubscribeToFeedRequest;
const isSubscribeToFeedResponse = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('subscribeToFeed'),
        messages: validateObject_1.isArrayOf(validateObject_1.isJSONObject)
    });
};
exports.isSubscribeToFeedResponse = isSubscribeToFeedResponse;
const isStoreFileRequest = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('storeFile'),
        fileData: validateObject_1.isString
    });
};
exports.isStoreFileRequest = isStoreFileRequest;
const isStoreFileResponse = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('storeFile'),
        uri: validateObject_1.optional(validateObject_1.isString)
    });
};
exports.isStoreFileResponse = isStoreFileResponse;
const isSetUrlStateRequest = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('setUrlState'),
        state: validateObject_1.isJSONObject
    });
};
exports.isSetUrlStateRequest = isSetUrlStateRequest;
const isSetUrlStateResponse = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('setUrlState')
    });
};
exports.isSetUrlStateResponse = isSetUrlStateResponse;
const isFigurlRequest = (x) => {
    return validateObject_1.isOneOf([
        exports.isGetFigureDataRequest,
        exports.isGetFileDataRequest,
        exports.isGetFileDataUrlRequest,
        exports.isGetMutableRequest,
        exports.isInitiateTaskRequest,
        exports.isSubscribeToFeedRequest,
        exports.isStoreFileRequest,
        exports.isSetUrlStateRequest
    ])(x);
};
exports.isFigurlRequest = isFigurlRequest;
const isFigurlResponse = (x) => {
    return validateObject_1.isOneOf([
        exports.isGetFigureDataResponse,
        exports.isGetFileDataResponse,
        exports.isGetFileDataUrlResponse,
        exports.isGetMutableResponse,
        exports.isInitiateTaskResponse,
        exports.isSubscribeToFeedResponse,
        exports.isStoreFileResponse,
        exports.isSetUrlStateResponse
    ])(x);
};
exports.isFigurlResponse = isFigurlResponse;
//# sourceMappingURL=FigurlRequestTypes.js.map

/***/ }),

/***/ "./lib/viewInterface/MessageToChildTypes.js":
/*!**************************************************!*\
  !*** ./lib/viewInterface/MessageToChildTypes.js ***!
  \**************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.isMessageToChild = exports.isFileDownloadProgressMessage = exports.isSetCurrentUserMessage = exports.isTaskStatusUpdateMessage = exports.isNewFeedMessagesMessage = exports.isFigurlResponseMessage = exports.isTaskJobStatus = exports.isTaskType = void 0;
const FigurlRequestTypes_1 = __webpack_require__(/*! ./FigurlRequestTypes */ "./lib/viewInterface/FigurlRequestTypes.js");
const kacheryTypes_1 = __webpack_require__(/*! ./kacheryTypes */ "./lib/viewInterface/kacheryTypes.js");
const validateObject_1 = __importStar(__webpack_require__(/*! ./validateObject */ "./lib/viewInterface/validateObject.js"));
const isTaskType = (x) => (['calculation', 'action'].includes(x));
exports.isTaskType = isTaskType;
const isTaskJobStatus = (x) => (['waiting', 'started', 'error', 'finished'].includes(x));
exports.isTaskJobStatus = isTaskJobStatus;
const isFigurlResponseMessage = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('figurlResponse'),
        requestId: validateObject_1.isString,
        response: FigurlRequestTypes_1.isFigurlResponse
    });
};
exports.isFigurlResponseMessage = isFigurlResponseMessage;
const isNewFeedMessagesMessage = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('newFeedMessages'),
        feedId: validateObject_1.isString,
        position: validateObject_1.isNumber,
        messages: validateObject_1.isArrayOf(validateObject_1.isJSONObject)
    });
};
exports.isNewFeedMessagesMessage = isNewFeedMessagesMessage;
const isTaskStatusUpdateMessage = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('taskStatusUpdate'),
        taskJobId: validateObject_1.isString,
        status: exports.isTaskJobStatus,
        errorMessage: validateObject_1.optional(validateObject_1.isString),
        returnValue: validateObject_1.optional(() => (true))
    });
};
exports.isTaskStatusUpdateMessage = isTaskStatusUpdateMessage;
const isSetCurrentUserMessage = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('setCurrentUser'),
        userId: validateObject_1.optional(kacheryTypes_1.isUserId),
        googleIdToken: validateObject_1.optional(validateObject_1.isString)
    });
};
exports.isSetCurrentUserMessage = isSetCurrentUserMessage;
const isFileDownloadProgressMessage = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('fileDownloadProgress'),
        uri: validateObject_1.isString,
        loaded: validateObject_1.isNumber,
        total: validateObject_1.isNumber
    });
};
exports.isFileDownloadProgressMessage = isFileDownloadProgressMessage;
const isMessageToChild = (x) => {
    return validateObject_1.isOneOf([
        exports.isFigurlResponseMessage,
        exports.isNewFeedMessagesMessage,
        exports.isTaskStatusUpdateMessage,
        exports.isSetCurrentUserMessage,
        exports.isFileDownloadProgressMessage
    ])(x);
};
exports.isMessageToChild = isMessageToChild;
//# sourceMappingURL=MessageToChildTypes.js.map

/***/ }),

/***/ "./lib/viewInterface/MessageToParentTypes.js":
/*!***************************************************!*\
  !*** ./lib/viewInterface/MessageToParentTypes.js ***!
  \***************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.isMessageToParent = exports.isFigurlRequestMessage = void 0;
const FigurlRequestTypes_1 = __webpack_require__(/*! ./FigurlRequestTypes */ "./lib/viewInterface/FigurlRequestTypes.js");
const validateObject_1 = __importStar(__webpack_require__(/*! ./validateObject */ "./lib/viewInterface/validateObject.js"));
const isFigurlRequestMessage = (x) => {
    return validateObject_1.default(x, {
        type: validateObject_1.isEqualTo('figurlRequest'),
        figureId: validateObject_1.isString,
        requestId: validateObject_1.isString,
        request: FigurlRequestTypes_1.isFigurlRequest
    });
};
exports.isFigurlRequestMessage = isFigurlRequestMessage;
const isMessageToParent = (x) => {
    return validateObject_1.isOneOf([
        exports.isFigurlRequestMessage
    ])(x);
};
exports.isMessageToParent = isMessageToParent;
//# sourceMappingURL=MessageToParentTypes.js.map

/***/ }),

/***/ "./lib/viewInterface/kacheryTypes.js":
/*!*******************************************!*\
  !*** ./lib/viewInterface/kacheryTypes.js ***!
  \*******************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

/* provided dependency */ var process = __webpack_require__(/*! process/browser */ "./node_modules/process/browser.js");

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.isRequestId = exports.isFindFileResult = exports.isFindLiveFeedResult = exports.fileKeyHash = exports.isFileKeyHash = exports.isFileKey = exports.errorMessage = exports.isErrorMessage = exports.taskKwargs = exports.isTaskKwargs = exports.userId = exports.isUserId = exports.pubsubChannelName = exports.isPubsubChannelName = exports.isTaskFunctionId = exports.channelName = exports.isChannelName = exports.subfeedHash = exports.isSubfeedHash = exports.isFeedId = exports.isNodeId = exports.isSignature = exports.isTaskFunctionType = exports.isTaskStatus = exports.toTaskId = exports.isTaskId = exports.isSha1Hash = exports.isPrivateKeyHex = exports.isPublicKeyHex = exports.isHexadecimal = exports.isKeyPair = exports.isPrivateKey = exports.isPublicKey = exports.elapsedSince = exports.zeroTimestamp = exports.nowTimestamp = exports.isTimestamp = exports.isAddress = exports.nodeLabel = exports.isNodeLabel = exports.urlString = exports.isUrlString = exports.hostName = exports.isHostName = exports.toPort = exports.portToNumber = exports.isPort = exports.isDaemonVersion = exports.mapToObject = exports.objectToMap = void 0;
exports.nodeIdToPublicKeyHex = exports.publicKeyHexToFeedId = exports.JSONStringifyDeterministic = exports.sha1OfString = exports.sha1OfObject = exports.pathifyHash = exports.channelConfigUrl = exports.isChannelConfigUrl = exports.isFileManifest = exports.isFileManifestChunk = exports.localFilePath = exports.exampleByteCount = exports.addByteCount = exports.byteCount = exports.byteCountToNumber = exports.isByteCount = exports.exampleDurationMsec = exports.durationGreaterThan = exports.scaleDurationBy = exports.maxDuration = exports.minDuration = exports.addDurations = exports.unscaledDurationMsec = exports.scaledDurationMsec = exports.durationMsecToNumber = exports.isDurationMsec = exports.isBuffer = exports.urlPath = exports.toSubfeedWatches = exports.toSubfeedWatchesRAM = exports.isSubfeedWatches = exports.isSubfeedWatch = exports.messageCount = exports.messageCountToNumber = exports.isMessageCount = exports.subfeedPosition = exports.subfeedPositionToNumber = exports.isSubfeedPosition = exports.isSubfeedWatchName = exports.submittedSubfeedMessageToSubfeedMessage = exports.isSubmittedSubfeedMessage = exports.isSignedSubfeedMessage = exports.isSubfeedMessageMetaData = exports.isSubfeedMessage = exports.isFeedSubfeedId = exports.feedSubfeedId = exports.feedName = exports.isFeedName = exports.channelLabel = exports.isChannelLabel = void 0;
exports.isUserConfig = exports.publicKeyHexToNodeId = exports.feedIdToPublicKeyHex = void 0;
const crypto = __importStar(__webpack_require__(/*! crypto */ "webpack/sharing/consume/default/crypto/crypto"));
const validateObject_1 = __importStar(__webpack_require__(/*! ./validateObject */ "./lib/viewInterface/validateObject.js"));
const assert = (x) => {
    if (!x)
        throw Error('Assertion error');
};
// objectToMap and mapToObject
const objectToMap = (obj) => {
    return new Map(Object.keys(obj).map(k => {
        return [k, obj[k]];
    }));
};
exports.objectToMap = objectToMap;
const mapToObject = (m) => {
    const ret = {};
    m.forEach((v, k) => {
        ret[k.toString()] = v;
    });
    return ret;
};
exports.mapToObject = mapToObject;
const isDaemonVersion = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return (/^[0-9a-zA-z. -]{4,40}?$/.test(x));
};
exports.isDaemonVersion = isDaemonVersion;
const isPort = (x) => {
    if (!validateObject_1.isNumber(x))
        return false;
    return x > 0 && x < 65536; // port numbers must be in 16-bit positive range
};
exports.isPort = isPort;
const portToNumber = (x) => {
    return x;
};
exports.portToNumber = portToNumber;
const toPort = (x) => {
    if (!exports.isPort(x))
        throw Error(`Not a valid port: ${x}`);
    return x;
};
exports.toPort = toPort;
const isHostName = (x) => {
    // can we be even more precise here? e.g. restrict number of elements?
    if (!validateObject_1.isString(x))
        return false;
    let result = true;
    x.split(".").forEach((element) => {
        if (element.length === 0)
            result = false;
        if (!/^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$/.test(element))
            result = false;
    });
    // we cannot short-circuit by returning false from the anonymous function in the forEach loop.
    // Doing so returns false *from that function*, then ignores the result (since nothing is checking
    // the result of the anonymous function) and moves on to check the next chunk.
    return result;
};
exports.isHostName = isHostName;
const hostName = (x) => {
    if (!exports.isHostName(x))
        throw Error(`Not a valid host name: ${x}`);
    return x;
};
exports.hostName = hostName;
const isUrlString = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    if ((x.startsWith('http://') || (x.startsWith('https://')))) {
        if (x.length > 10000)
            return false;
        return true;
    }
    else {
        return false;
    }
};
exports.isUrlString = isUrlString;
const urlString = (x) => {
    if (!exports.isUrlString(x))
        throw Error(`Not a valid url string: ${x}`);
    return x;
};
exports.urlString = urlString;
const isNodeLabel = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    if (x.length > 20)
        return false;
    let result = true;
    x.split(".").forEach((element) => {
        if (element.length === 0)
            result = false;
        if (!/^[a-zA-Z0-9@]([a-zA-Z0-9@-]*[a-zA-Z0-9@])?$/.test(element))
            result = false;
    });
    return result;
};
exports.isNodeLabel = isNodeLabel;
const nodeLabel = (x) => {
    if (!exports.isNodeLabel(x))
        throw Error(`Not a valid node label: ${x}`);
    return x;
};
exports.nodeLabel = nodeLabel;
const isAddress = (x) => {
    if (!validateObject_1.default(x, {
        hostName: validateObject_1.optional(exports.isHostName),
        port: validateObject_1.optional(exports.isPort),
        url: validateObject_1.optional(exports.isUrlString)
    })) {
        return false;
    }
    if ((x.hostName) && (x.port)) {
        return x.url ? false : true;
    }
    else if (x.url) {
        return ((x.hostName) || (x.port)) ? false : true;
    }
    else {
        return false;
    }
};
exports.isAddress = isAddress;
const isTimestamp = (x) => {
    if (!validateObject_1.isNumber(x))
        return false;
    if (x < 0)
        return false; // For our purposes, timestamps should never be negative
    if (!Number.isInteger(x))
        return false; // our timestamps should be whole numbers
    return true;
};
exports.isTimestamp = isTimestamp;
const nowTimestamp = () => {
    const ret = Number(new Date()) - 0;
    return ret;
};
exports.nowTimestamp = nowTimestamp;
const zeroTimestamp = () => {
    return 0;
};
exports.zeroTimestamp = zeroTimestamp;
const elapsedSince = (timestamp) => {
    return exports.nowTimestamp() - timestamp;
};
exports.elapsedSince = elapsedSince;
const isPublicKey = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return checkKeyblockHeader(x, 'PUBLIC');
};
exports.isPublicKey = isPublicKey;
const isPrivateKey = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return checkKeyblockHeader(x, 'PRIVATE');
};
exports.isPrivateKey = isPrivateKey;
const checkKeyblockHeader = (key, type) => {
    // note we need to double-escape the backslashes here.
    const pattern = new RegExp(`-----BEGIN ${type} KEY-----[\\s\\S]*-----END ${type} KEY-----\n*$`);
    return (pattern.test(key));
};
const isKeyPair = (x) => {
    return validateObject_1.default(x, {
        publicKey: exports.isPublicKey,
        privateKey: exports.isPrivateKey
    });
};
exports.isKeyPair = isKeyPair;
const isHexadecimal = (x, length) => {
    const basePattern = '[0-9a-fA-F]';
    let pattern = `^${basePattern}*$`;
    if (length !== undefined) {
        assert(Number.isInteger(length));
        assert(length > 0);
        pattern = `^${basePattern}{${length}}$`;
    }
    const regex = new RegExp(pattern);
    return (regex.test(x));
};
exports.isHexadecimal = isHexadecimal;
const isPublicKeyHex = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return exports.isHexadecimal(x, 64);
};
exports.isPublicKeyHex = isPublicKeyHex;
const isPrivateKeyHex = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return exports.isHexadecimal(x, 64);
};
exports.isPrivateKeyHex = isPrivateKeyHex;
const isSha1Hash = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return exports.isHexadecimal(x, 40); // Sha1 should be 40 hex characters
};
exports.isSha1Hash = isSha1Hash;
const isTaskId = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    if (x.length > 40)
        return false;
    return true;
};
exports.isTaskId = isTaskId;
const toTaskId = (x) => {
    if (!exports.isTaskId(x)) {
        throw Error(`Not a valid task ID: ${x}`);
    }
    return x;
};
exports.toTaskId = toTaskId;
const isTaskStatus = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return ['waiting', 'pending', 'queued', 'running', 'finished', 'error'].includes(x);
};
exports.isTaskStatus = isTaskStatus;
const isTaskFunctionType = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return ['pure-calculation', 'query', 'action'].includes(x);
};
exports.isTaskFunctionType = isTaskFunctionType;
const isSignature = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return exports.isHexadecimal(x, 128);
};
exports.isSignature = isSignature;
const isNodeId = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return exports.isHexadecimal(x, 64);
};
exports.isNodeId = isNodeId;
const isFeedId = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return exports.isHexadecimal(x, 64);
};
exports.isFeedId = isFeedId;
const isSubfeedHash = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return (/^[0-9a-fA-F]{40}?$/.test(x));
};
exports.isSubfeedHash = isSubfeedHash;
const subfeedHash = (x) => {
    if (exports.isSubfeedHash(x))
        return x;
    else
        throw Error(`Invalid subfeed hash: ${x}`);
};
exports.subfeedHash = subfeedHash;
const isChannelName = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    if (x.length > 40)
        return false;
    if (x.length < 3)
        return false;
    let result = true;
    x.split(".").forEach((element) => {
        if (element.length === 0)
            result = false;
        if (!/^[a-zA-Z0-9_-]([a-zA-Z0-9_-]*[a-zA-Z0-9_-])?$/.test(element))
            result = false;
    });
    return result;
};
exports.isChannelName = isChannelName;
const channelName = (x) => {
    if (!exports.isChannelName(x))
        throw Error(`Invalid channel name: ${x}`);
    return x;
};
exports.channelName = channelName;
const isTaskFunctionId = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    if (x.length > 400)
        return false;
    let result = true;
    x.split(".").forEach((element) => {
        if (element.length === 0)
            result = false;
        if (!/^[a-zA-Z0-9@_-]([a-zA-Z0-9@_-]*[a-zA-Z0-9@_-])?$/.test(element))
            result = false;
    });
    return result;
};
exports.isTaskFunctionId = isTaskFunctionId;
const isPubsubChannelName = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    if (x.length > 40)
        return false;
    return true;
};
exports.isPubsubChannelName = isPubsubChannelName;
const pubsubChannelName = (x) => {
    if (!exports.isPubsubChannelName(x))
        throw Error(`Invalid pubsub channel name: ${x}`);
    return x;
};
exports.pubsubChannelName = pubsubChannelName;
const isUserId = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    if (x.length > 80)
        return false;
    return true;
};
exports.isUserId = isUserId;
const userId = (x) => {
    if (!exports.isUserId(x))
        throw Error(`Invalid user ID: ${x}`);
    return x;
};
exports.userId = userId;
const isTaskKwargs = (x) => {
    if (!validateObject_1.isJSONObject(x))
        return false;
    return true;
};
exports.isTaskKwargs = isTaskKwargs;
const taskKwargs = (x) => {
    if (!exports.isTaskKwargs(x))
        throw Error('Invalid task kwargs');
    return x;
};
exports.taskKwargs = taskKwargs;
const isErrorMessage = (x) => {
    return (validateObject_1.isString(x)) && (x.length < 1000);
};
exports.isErrorMessage = isErrorMessage;
const errorMessage = (x) => {
    if (exports.isErrorMessage(x))
        return x;
    else {
        throw Error('Invalid error message: messages cannot exceed 1000 characters.');
    }
};
exports.errorMessage = errorMessage;
const isFileKey = (x) => {
    return validateObject_1.default(x, {
        sha1: exports.isSha1Hash,
        manifestSha1: validateObject_1.optional(exports.isSha1Hash),
        chunkOf: validateObject_1.optional({
            fileKey: exports.isFileKey,
            startByte: exports.isByteCount,
            endByte: exports.isByteCount
        })
    });
};
exports.isFileKey = isFileKey;
const isFileKeyHash = (x) => {
    return exports.isSha1Hash(x) ? true : false;
};
exports.isFileKeyHash = isFileKeyHash;
const fileKeyHash = (fileKey) => {
    return exports.sha1OfObject(fileKey);
};
exports.fileKeyHash = fileKeyHash;
const isFindLiveFeedResult = (x) => {
    return validateObject_1.default(x, {
        nodeId: exports.isNodeId
    });
};
exports.isFindLiveFeedResult = isFindLiveFeedResult;
const isFindFileResult = (x) => {
    if (!validateObject_1.default(x, {
        nodeId: exports.isNodeId,
        fileKey: exports.isFileKey,
        fileSize: exports.isByteCount
    }))
        return false;
    return (x.fileSize >= 0);
};
exports.isFindFileResult = isFindFileResult;
const isRequestId = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return (/^[A-Za-z]{10}$/.test(x));
};
exports.isRequestId = isRequestId;
const isChannelLabel = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return (/^[0-9a-zA-Z_\-.]{4,160}?$/.test(x));
};
exports.isChannelLabel = isChannelLabel;
const channelLabel = (x) => {
    if (!exports.isChannelLabel(x)) {
        throw Error(`Invalid channel label: ${x}`);
    }
    return x;
};
exports.channelLabel = channelLabel;
const isFeedName = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return ((x.length > 0) && (x.length <= 100));
};
exports.isFeedName = isFeedName;
const feedName = (x) => {
    if (exports.isFeedName(x))
        return x;
    else
        throw Error(`Invalid feed name: ${x}`);
};
exports.feedName = feedName;
const feedSubfeedId = (feedId, subfeedHash, channelName) => {
    return (feedId.toString() + ':' + subfeedHash.toString() + ':' + channelName.toString());
};
exports.feedSubfeedId = feedSubfeedId;
const isFeedSubfeedId = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    const parts = x.split(':');
    return (parts.length === 2) &&
        (exports.isFeedId(parts[0])) &&
        (exports.isSubfeedHash(parts[1]));
};
exports.isFeedSubfeedId = isFeedSubfeedId;
;
const isSubfeedMessage = (x) => {
    return validateObject_1.isObject(x);
};
exports.isSubfeedMessage = isSubfeedMessage;
const isSubfeedMessageMetaData = (x) => {
    return validateObject_1.isObject(x);
};
exports.isSubfeedMessageMetaData = isSubfeedMessageMetaData;
const isSignedSubfeedMessage = (x) => {
    if (!validateObject_1.default(x, {
        body: {
            previousSignature: validateObject_1.optional(exports.isSignature),
            messageNumber: validateObject_1.isNumber,
            message: validateObject_1.isObject,
            timestamp: exports.isTimestamp,
            metaData: validateObject_1.optional(exports.isSubfeedMessageMetaData)
        },
        signature: exports.isSignature
    }))
        return false;
    return true;
};
exports.isSignedSubfeedMessage = isSignedSubfeedMessage;
;
const isSubmittedSubfeedMessage = (x) => {
    return ((validateObject_1.isJSONObject(x)) && (JSON.stringify(x).length < 10000));
};
exports.isSubmittedSubfeedMessage = isSubmittedSubfeedMessage;
const submittedSubfeedMessageToSubfeedMessage = (x) => {
    return x;
};
exports.submittedSubfeedMessageToSubfeedMessage = submittedSubfeedMessageToSubfeedMessage;
const isSubfeedWatchName = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    return x.length > 0;
};
exports.isSubfeedWatchName = isSubfeedWatchName;
const isSubfeedPosition = (x) => {
    if (!validateObject_1.isNumber(x))
        return false;
    return (x >= 0);
};
exports.isSubfeedPosition = isSubfeedPosition;
const subfeedPositionToNumber = (x) => {
    return x;
};
exports.subfeedPositionToNumber = subfeedPositionToNumber;
const subfeedPosition = (x) => {
    return x;
};
exports.subfeedPosition = subfeedPosition;
const isMessageCount = (x) => {
    if (!validateObject_1.isNumber(x))
        return false;
    return (x >= 0);
};
exports.isMessageCount = isMessageCount;
const messageCountToNumber = (x) => {
    return x;
};
exports.messageCountToNumber = messageCountToNumber;
const messageCount = (x) => {
    return x;
};
exports.messageCount = messageCount;
const isSubfeedWatch = (x) => {
    return validateObject_1.default(x, {
        feedId: exports.isFeedId,
        subfeedHash: exports.isSubfeedHash,
        position: exports.isSubfeedPosition,
        channelName: validateObject_1.isString
    });
};
exports.isSubfeedWatch = isSubfeedWatch;
const isSubfeedWatches = (x) => {
    return validateObject_1.isObjectOf(exports.isSubfeedWatchName, exports.isSubfeedWatch)(x);
};
exports.isSubfeedWatches = isSubfeedWatches;
const toSubfeedWatchesRAM = (x) => {
    return exports.objectToMap(x);
};
exports.toSubfeedWatchesRAM = toSubfeedWatchesRAM;
const toSubfeedWatches = (x) => {
    return exports.mapToObject(x);
};
exports.toSubfeedWatches = toSubfeedWatches;
const urlPath = (x) => {
    return x;
};
exports.urlPath = urlPath;
const isBuffer = (x) => {
    return ((x !== null) && (x instanceof Buffer));
};
exports.isBuffer = isBuffer;
const isDurationMsec = (x) => {
    if (!validateObject_1.isNumber(x))
        return false;
    if (x < 0)
        return false;
    return true;
};
exports.isDurationMsec = isDurationMsec;
const durationMsecToNumber = (x) => {
    return x;
};
exports.durationMsecToNumber = durationMsecToNumber;
const scaledDurationMsec = (n) => {
    if (process.env.KACHERY_TEST_SPEEDUP_FACTOR) {
        n /= Number(process.env.KACHERY_TEST_SPEEDUP_FACTOR);
    }
    return n;
};
exports.scaledDurationMsec = scaledDurationMsec;
const unscaledDurationMsec = (n) => {
    return n;
};
exports.unscaledDurationMsec = unscaledDurationMsec;
const addDurations = (a, b) => {
    return (a + b);
};
exports.addDurations = addDurations;
const minDuration = (a, b) => {
    return Math.min(a, b);
};
exports.minDuration = minDuration;
const maxDuration = (a, b) => {
    return Math.max(a, b);
};
exports.maxDuration = maxDuration;
const scaleDurationBy = (a, factor) => {
    return a * factor;
};
exports.scaleDurationBy = scaleDurationBy;
const durationGreaterThan = (a, b) => {
    return a > b;
};
exports.durationGreaterThan = durationGreaterThan;
exports.exampleDurationMsec = exports.scaledDurationMsec(3000);
const isByteCount = (x) => {
    if (!validateObject_1.isNumber(x))
        return false;
    if (x < 0)
        return false;
    return true;
};
exports.isByteCount = isByteCount;
const byteCountToNumber = (x) => {
    return x;
};
exports.byteCountToNumber = byteCountToNumber;
const byteCount = (n) => {
    return n;
};
exports.byteCount = byteCount;
const addByteCount = (n1, n2) => {
    return exports.byteCount(exports.byteCountToNumber(n1) + exports.byteCountToNumber(n2));
};
exports.addByteCount = addByteCount;
exports.exampleByteCount = exports.byteCount(4000);
const localFilePath = (p) => {
    return p;
};
exports.localFilePath = localFilePath;
const isFileManifestChunk = (x) => {
    return validateObject_1.default(x, {
        start: exports.isByteCount,
        end: exports.isByteCount,
        sha1: exports.isSha1Hash
    });
};
exports.isFileManifestChunk = isFileManifestChunk;
const isFileManifest = (x) => {
    return validateObject_1.default(x, {
        size: exports.isByteCount,
        sha1: exports.isSha1Hash,
        chunks: validateObject_1.isArrayOf(exports.isFileManifestChunk)
    });
};
exports.isFileManifest = isFileManifest;
const isChannelConfigUrl = (x) => {
    if (!validateObject_1.isString(x))
        return false;
    if ((x.startsWith('http://') || (x.startsWith('https://')))) {
        if (x.length > 500)
            return false;
        return true;
    }
    else {
        return false;
    }
};
exports.isChannelConfigUrl = isChannelConfigUrl;
const channelConfigUrl = (x) => {
    if (!exports.isChannelConfigUrl(x))
        throw Error(`Not a valid channel config url string: ${x}`);
    return x;
};
exports.channelConfigUrl = channelConfigUrl;
const pathifyHash = (x) => {
    return `${x[0]}${x[1]}/${x[2]}${x[3]}/${x[4]}${x[5]}/${x}`;
};
exports.pathifyHash = pathifyHash;
const sha1OfObject = (x) => {
    return exports.sha1OfString(exports.JSONStringifyDeterministic(x));
};
exports.sha1OfObject = sha1OfObject;
const sha1OfString = (x) => {
    const sha1sum = crypto.createHash('sha1');
    sha1sum.update(x);
    return sha1sum.digest('hex');
};
exports.sha1OfString = sha1OfString;
// Thanks: https://stackoverflow.com/questions/16167581/sort-object-properties-and-json-stringify
const JSONStringifyDeterministic = (obj, space = undefined) => {
    var allKeys = [];
    JSON.stringify(obj, function (key, value) { allKeys.push(key); return value; });
    allKeys.sort();
    return JSON.stringify(obj, allKeys, space);
};
exports.JSONStringifyDeterministic = JSONStringifyDeterministic;
const publicKeyHexToFeedId = (publicKeyHex) => {
    return publicKeyHex;
};
exports.publicKeyHexToFeedId = publicKeyHexToFeedId;
const nodeIdToPublicKeyHex = (nodeId) => {
    return nodeId.toString();
};
exports.nodeIdToPublicKeyHex = nodeIdToPublicKeyHex;
const feedIdToPublicKeyHex = (feedId) => {
    return feedId;
};
exports.feedIdToPublicKeyHex = feedIdToPublicKeyHex;
const publicKeyHexToNodeId = (x) => {
    return x;
};
exports.publicKeyHexToNodeId = publicKeyHexToNodeId;
const isUserConfig = (x) => {
    return validateObject_1.default(x, {
        admin: validateObject_1.optional(validateObject_1.isBoolean)
    }, {
        allowAdditionalFields: true
    });
};
exports.isUserConfig = isUserConfig;
//# sourceMappingURL=kacheryTypes.js.map

/***/ }),

/***/ "./lib/viewInterface/validateObject.js":
/*!*********************************************!*\
  !*** ./lib/viewInterface/validateObject.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.isJSONSerializable = exports.tryParseJsonObject = exports.isJSONValue = exports.isJSONObject = exports.isObjectOf = exports.isObject = exports.isArrayOf = exports.isEqualTo = exports.optional = exports.isOneOf = exports.isBoolean = exports.isNull = exports.isNumber = exports.isFunction = exports.isString = void 0;
// string
const isString = (x) => {
    return ((x !== null) && (typeof x === 'string'));
};
exports.isString = isString;
// function
const isFunction = (x) => {
    return ((x !== null) && (typeof x === 'function'));
};
exports.isFunction = isFunction;
// number
const isNumber = (x) => {
    return ((x !== null) && (typeof x === 'number'));
};
exports.isNumber = isNumber;
// null
const isNull = (x) => {
    return x === null;
};
exports.isNull = isNull;
// boolean
const isBoolean = (x) => {
    return ((x !== null) && (typeof x === 'boolean'));
};
exports.isBoolean = isBoolean;
// isOneOf
const isOneOf = (testFunctions) => {
    return (x) => {
        for (let tf of testFunctions) {
            if (tf(x))
                return true;
        }
        return false;
    };
};
exports.isOneOf = isOneOf;
const optional = (testFunctionOrSpec) => {
    if (exports.isFunction(testFunctionOrSpec)) {
        const testFunction = testFunctionOrSpec;
        return (x) => {
            return ((x === undefined) || (testFunction(x)));
        };
    }
    else {
        return (x) => {
            const obj = testFunctionOrSpec;
            return ((x === undefined) || (validateObject(x, obj)));
        };
    }
};
exports.optional = optional;
// isEqualTo
const isEqualTo = (value) => {
    return (x) => {
        return x === value;
    };
};
exports.isEqualTo = isEqualTo;
// isArrayOf
const isArrayOf = (testFunction) => {
    return (x) => {
        if ((x !== null) && (Array.isArray(x))) {
            for (let a of x) {
                if (!testFunction(a))
                    return false;
            }
            return true;
        }
        else
            return false;
    };
};
exports.isArrayOf = isArrayOf;
// object
const isObject = (x) => {
    return ((x !== null) && (typeof x === 'object'));
};
exports.isObject = isObject;
// isObjectOf
const isObjectOf = (keyTestFunction, valueTestFunction) => {
    return (x) => {
        if (exports.isObject(x)) {
            for (let k in x) {
                if (!keyTestFunction(k))
                    return false;
                if (!valueTestFunction(x[k]))
                    return false;
            }
            return true;
        }
        else
            return false;
    };
};
exports.isObjectOf = isObjectOf;
const isJSONObject = (x) => {
    if (!exports.isObject(x))
        return false;
    return exports.isJSONSerializable(x);
};
exports.isJSONObject = isJSONObject;
const isJSONValue = (x) => {
    return exports.isJSONSerializable(x);
};
exports.isJSONValue = isJSONValue;
const tryParseJsonObject = (x) => {
    let a;
    try {
        a = JSON.parse(x);
    }
    catch (_a) {
        return null;
    }
    if (!exports.isJSONObject(a))
        return null;
    return a;
};
exports.tryParseJsonObject = tryParseJsonObject;
const isJSONSerializable = (obj) => {
    if (typeof (obj) === 'string')
        return true;
    if (typeof (obj) === 'number')
        return true;
    if (!exports.isObject(obj))
        return false;
    const isPlainObject = (a) => {
        return Object.prototype.toString.call(a) === '[object Object]';
    };
    const isPlain = (a) => {
        return (a === null) || (typeof a === 'undefined' || typeof a === 'string' || typeof a === 'boolean' || typeof a === 'number' || Array.isArray(a) || isPlainObject(a));
    };
    if (!isPlain(obj)) {
        return false;
    }
    for (let property in obj) {
        if (obj.hasOwnProperty(property)) {
            if (!isPlain(obj[property])) {
                return false;
            }
            if (obj[property] !== null) {
                if (typeof obj[property] === "object") {
                    if (!exports.isJSONSerializable(obj[property])) {
                        return false;
                    }
                }
            }
        }
    }
    return true;
};
exports.isJSONSerializable = isJSONSerializable;
const validateObject = (x, spec, opts) => {
    const o = opts || {};
    if (!x) {
        o.callback && o.callback('x is undefined/null.');
        return false;
    }
    if (typeof (x) !== 'object') {
        o.callback && o.callback('x is not an Object.');
        return false;
    }
    for (let k in x) {
        if (!(k in spec)) {
            if (!o.allowAdditionalFields) {
                o.callback && o.callback(`Key not in spec: ${k}`);
                return false;
            }
        }
    }
    for (let k in spec) {
        const specK = spec[k];
        if (exports.isFunction(specK)) {
            if (!specK(x[k])) {
                o.callback && o.callback(`Problem validating: ${k}`);
                return false;
            }
        }
        else {
            if (!(k in x)) {
                o.callback && o.callback(`Key not in x: ${k}`);
                return false;
            }
            if (!validateObject(x[k], specK, { callback: o.callback })) {
                o.callback && o.callback(`Value of key > ${k} < itself failed validation.`);
                return false;
            }
        }
    }
    return true;
};
exports["default"] = validateObject;
//# sourceMappingURL=validateObject.js.map

/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


// Copyright (c) Jeremy Magland
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.FigurlFigureView = exports.FigurlFigureModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_dom_1 = __importDefault(__webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom"));
const FigureWidget_1 = __importDefault(__webpack_require__(/*! ./FigureWidget */ "./lib/FigureWidget.js"));
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
// Import the CSS
// import '../css/widget.css';
class FigurlFigureModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: FigurlFigureModel.model_name, _model_module: FigurlFigureModel.model_module, _model_module_version: FigurlFigureModel.model_module_version, _view_name: FigurlFigureModel.view_name, _view_module: FigurlFigureModel.view_module, _view_module_version: FigurlFigureModel.view_module_version, view_uri: '', data_uri: '', height: 0 });
    }
}
exports.FigurlFigureModel = FigurlFigureModel;
FigurlFigureModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
FigurlFigureModel.model_name = 'FigurlFigureModel';
FigurlFigureModel.model_module = version_1.MODULE_NAME;
FigurlFigureModel.model_module_version = version_1.MODULE_VERSION;
FigurlFigureModel.view_name = 'FigurlFigureView'; // Set to null if no view
FigurlFigureModel.view_module = version_1.MODULE_NAME; // Set to null if no view
FigurlFigureModel.view_module_version = version_1.MODULE_VERSION;
class FigurlFigureView extends base_1.DOMWidgetView {
    render() {
        this.el.classList.add('custom-widget');
        this.onChange();
        this.model.on('change:view_uri', this.onChange, this);
        this.model.on('change:data_uri', this.onChange, this);
        this.model.on('change:height', this.onChange, this);
        // this.el.innerHTML = '<div style="position:absolute;width:300px;height:300px;background:green;" />'
    }
    onChange() {
        const viewUri = this.model.get('view_uri');
        const dataUri = this.model.get('data_uri');
        const height = this.model.get('height');
        if ((viewUri) && (dataUri)) {
            const component = react_1.default.createElement(FigureWidget_1.default, { model: this.model, viewUri, dataUri, height });
            react_dom_1.default.render(component, this.el);
        }
        else {
            this.el.innerHTML = '<h3>Waiting for widget properties</h3>';
        }
        // this.el.innerHTML = `
        //   <iframe src="https://www.figurl.org/f?v=gs://figurl/draculus-1&d=sha1://2b9330656b2cf1993716cd615950754945ea16d0&project=lqhzprbdrq&hide=1&label=draculus%20sortingview%20example" />
        // `;
        // this.el.textContent = this.model.get('value') + ' test4';
    }
}
exports.FigurlFigureView = FigurlFigureView;
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = JSON.parse('{"name":"figurl-jupyter","version":"0.2.1","description":"View figurl figures in jupyterlab","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/scratchrealm/figurl-jupyter","bugs":{"url":"https://github.com/scratchrealm/figurl-jupyter/issues"},"license":"BSD-3-Clause","author":{"name":"Jeremy Magland","email":"jmagland@flatironinstitute.org"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/scratchrealm/figurl-jupyter"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf figurl_jupyter/labextension","clean:nbextension":"rimraf figurl_jupyter/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","react":"^18.2.0","react-dom":"^18.2.0","crypto":"npm:crypto-browserify","zlib":"npm:zlib-browserify","stream":"npm:stream-browserify","path":"npm:path-browserify","buffer":"npm:buffer-browserify","assert":"npm:assert-browserify"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/node":"^18.7.14","@types/react":"^18.0.18","@types/react-dom":"^18.0.6","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"figurl_jupyter/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.e6bb70e167ef630cb578.js.map