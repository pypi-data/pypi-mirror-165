"use strict";
(self["webpackChunk_educational_technology_collective_etc_jupyterlab_telemetry_coursera"] = self["webpackChunk_educational_technology_collective_etc_jupyterlab_telemetry_coursera"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'etc-jupyterlab-telemetry-coursera', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AWSAPIGatewayAdapter": () => (/* binding */ AWSAPIGatewayAdapter),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_telemetry_library__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @educational-technology-collective/etc_jupyterlab_telemetry_library */ "webpack/sharing/consume/default/@educational-technology-collective/etc_jupyterlab_telemetry_library");
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_telemetry_library__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_educational_technology_collective_etc_jupyterlab_telemetry_library__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_notebook_state_provider__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @educational-technology-collective/etc_jupyterlab_notebook_state_provider */ "webpack/sharing/consume/default/@educational-technology-collective/etc_jupyterlab_notebook_state_provider");
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_notebook_state_provider__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_educational_technology_collective_etc_jupyterlab_notebook_state_provider__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_feedback__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @educational-technology-collective/etc_jupyterlab_feedback */ "webpack/sharing/consume/default/@educational-technology-collective/etc_jupyterlab_feedback");
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_feedback__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_educational_technology_collective_etc_jupyterlab_feedback__WEBPACK_IMPORTED_MODULE_3__);





const PLUGIN_ID = '@educational-technology-collective/etc_jupyterlab_telemetry_coursera:plugin';
class AWSAPIGatewayAdapter {
    constructor({ etcJupyterLabNotebookStateProvider, config }) {
        this._etcJupyterLabNotebookStateProvider = etcJupyterLabNotebookStateProvider;
        this._config = config;
    }
    async adaptMessage(sender, data) {
        var _a, _b, _c, _d;
        try {
            let notebookState = this._etcJupyterLabNotebookStateProvider.getNotebookState({
                notebookPanel: data.notebookPanel
            });
            var body = {
                'event_name': data.eventName,
                'cells': data.cells,
                'notebook': notebookState === null || notebookState === void 0 ? void 0 : notebookState.notebook,
                'seq': notebookState === null || notebookState === void 0 ? void 0 : notebookState.seq,
                'session_id': notebookState === null || notebookState === void 0 ? void 0 : notebookState.session_id,
                'user_id': ((_a = this._config) === null || _a === void 0 ? void 0 : _a.workspace_id) ? (_b = this._config) === null || _b === void 0 ? void 0 : _b.workspace_id : "UNDEFINED",
                'notebook_path': data.notebookPanel.context.path,
                'kernel_error': data.kernelError,
                'selection': data.selection,
                'environ': data.environ,
                'message': data.message //  The message from the feedback extension.
            };
            if ((_c = this._config['capture_notebook_events']) === null || _c === void 0 ? void 0 : _c.includes(data.eventName)) {
                body['meta'] = (_d = data.notebookPanel.content.model) === null || _d === void 0 ? void 0 : _d.toJSON();
            }
            let request = Object.assign({}, body);
            delete request['meta'];
            console.log('Request', request);
            let response = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('s3', { method: 'POST', body: JSON.stringify(body) });
            console.log('Response', {
                'response': response,
                'requestBody': request
            });
        }
        catch (e) {
            console.error(e);
        }
    }
}
/**
 * Initialization data for the @educational-technology-collective/etc_jupyterlab_telemetry_coursera extension.
 */
const plugin = {
    id: PLUGIN_ID,
    autoStart: true,
    requires: [
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker,
        _educational_technology_collective_etc_jupyterlab_notebook_state_provider__WEBPACK_IMPORTED_MODULE_2__.IETCJupyterLabNotebookStateProvider,
        _educational_technology_collective_etc_jupyterlab_telemetry_library__WEBPACK_IMPORTED_MODULE_1__.IETCJupyterLabTelemetryLibraryFactory,
        _educational_technology_collective_etc_jupyterlab_feedback__WEBPACK_IMPORTED_MODULE_3__.IETCJupyterLabFeedbackServiceFactory
    ],
    activate: (app, notebookTracker, etcJupyterLabNotebookStateProvider, etcJupyterLabTelemetryLibraryFactory, etcJupyterLabFeedbackServiceFactory) => {
        let messageAdapter;
        let appConfig = (async () => {
            try {
                await app.started;
                const config = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('config');
                console.log(`${PLUGIN_ID}, ${config.version}`);
                if (!config.telemetry) {
                    notebookTracker.widgetAdded.disconnect(onWidgetAdded, undefined);
                }
                return config;
            }
            catch (e) {
                console.error(e);
                notebookTracker.widgetAdded.disconnect(onWidgetAdded, undefined);
                return false;
            }
        })();
        async function onWidgetAdded(sender, notebookPanel) {
            //  Handlers must be attached immediately in order to detect early events, hence we do not want to await the appearance of the Notebook.
            let config = await appConfig;
            if (config.telemetry) {
                setInterval(() => {
                    var _a;
                    if ((_a = notebookPanel.content.model) === null || _a === void 0 ? void 0 : _a.dirty) {
                        notebookPanel.context.save();
                    }
                }, config.save_interval * 1000);
                if (!messageAdapter) {
                    messageAdapter = new AWSAPIGatewayAdapter({ etcJupyterLabNotebookStateProvider, config });
                }
                etcJupyterLabNotebookStateProvider.addNotebookPanel({ notebookPanel });
                let etcJupyterLabTelemetryLibrary = etcJupyterLabTelemetryLibraryFactory.create({ notebookPanel });
                etcJupyterLabTelemetryLibrary.notebookClipboardEvent.notebookClipboardCopied.connect(messageAdapter.adaptMessage, messageAdapter);
                etcJupyterLabTelemetryLibrary.notebookClipboardEvent.notebookClipboardCut.connect(messageAdapter.adaptMessage, messageAdapter);
                etcJupyterLabTelemetryLibrary.notebookClipboardEvent.notebookClipboardPasted.connect(messageAdapter.adaptMessage, messageAdapter);
                etcJupyterLabTelemetryLibrary.notebookVisibilityEvent.notebookVisible.connect(messageAdapter.adaptMessage, messageAdapter);
                etcJupyterLabTelemetryLibrary.notebookVisibilityEvent.notebookHidden.connect(messageAdapter.adaptMessage, messageAdapter);
                etcJupyterLabTelemetryLibrary.notebookOpenEvent.notebookOpened.connect(messageAdapter.adaptMessage, messageAdapter);
                etcJupyterLabTelemetryLibrary.notebookCloseEvent.notebookClosed.connect(messageAdapter.adaptMessage, messageAdapter);
                etcJupyterLabTelemetryLibrary.notebookSaveEvent.notebookSaved.connect(messageAdapter.adaptMessage, messageAdapter);
                etcJupyterLabTelemetryLibrary.notebookScrollEvent.notebookScrolled.connect(messageAdapter.adaptMessage, messageAdapter);
                etcJupyterLabTelemetryLibrary.activeCellChangeEvent.activeCellChanged.connect(messageAdapter.adaptMessage, messageAdapter);
                etcJupyterLabTelemetryLibrary.cellAddEvent.cellAdded.connect(messageAdapter.adaptMessage, messageAdapter);
                etcJupyterLabTelemetryLibrary.cellRemoveEvent.cellRemoved.connect(messageAdapter.adaptMessage, messageAdapter);
                etcJupyterLabTelemetryLibrary.cellExecutionEvent.cellExecuted.connect(messageAdapter.adaptMessage, messageAdapter);
                etcJupyterLabTelemetryLibrary.cellErrorEvent.cellErrored.connect(messageAdapter.adaptMessage, messageAdapter);
                await notebookPanel.revealed;
                for (let cell of notebookPanel.content.widgets) {
                    if (cell.model.metadata.has('nbgrader')) {
                        let etcJupyterLabFeedbackService = etcJupyterLabFeedbackServiceFactory.create({ notebookPanel });
                        etcJupyterLabFeedbackService.buttonClicked.connect(messageAdapter.adaptMessage, messageAdapter);
                        etcJupyterLabFeedbackService.resultsDisplayed.connect(messageAdapter.adaptMessage, messageAdapter);
                        etcJupyterLabFeedbackService.resultsDismissed.connect(messageAdapter.adaptMessage, messageAdapter);
                        break;
                    }
                }
            }
        }
        notebookTracker.widgetAdded.connect(onWidgetAdded, undefined);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.956df5f7f862621b568d.js.map