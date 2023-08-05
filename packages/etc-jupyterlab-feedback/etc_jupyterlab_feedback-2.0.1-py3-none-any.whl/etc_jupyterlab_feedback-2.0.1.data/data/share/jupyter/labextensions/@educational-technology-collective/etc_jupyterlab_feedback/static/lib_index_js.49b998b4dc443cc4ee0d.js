"use strict";
(self["webpackChunk_educational_technology_collective_etc_jupyterlab_feedback"] = self["webpackChunk_educational_technology_collective_etc_jupyterlab_feedback"] || []).push([["lib_index_js"],{

/***/ "./lib/button.js":
/*!***********************!*\
  !*** ./lib/button.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ETCJupyterLabConfigurableTextButton": () => (/* binding */ ETCJupyterLabConfigurableTextButton)
/* harmony export */ });
class ETCJupyterLabConfigurableTextButton {
    constructor({ stylePressed, style, innerHTML }) {
        this._stylePressed = stylePressed;
        this._style = style;
        this.eventTarget = new EventTarget();
        let node = this.node = document.createElement('div');
        let button = this.button = document.createElement('button');
        button.classList.add('jp-Button');
        let span = this._span = document.createElement('span');
        span.classList.add('bp3-button-text');
        if (innerHTML) {
            span.innerHTML = innerHTML;
        }
        button.appendChild(span);
        node.appendChild(button);
        if (style) {
            Object.assign(button.style, style);
        }
        this.enable();
    }
    disable() {
        this.button.removeEventListener('mousedown', this);
        this.button.removeEventListener('mouseup', this);
        this.button.removeEventListener('click', this);
    }
    enable() {
        this.button.addEventListener('mousedown', this);
        this.button.addEventListener('mouseup', this);
        this.button.addEventListener('click', this);
    }
    handleEvent(event) {
        try {
            if (event.type == 'click') {
                this.eventTarget.dispatchEvent(new CustomEvent('click'));
            }
            else if (event.type == 'mousedown') {
                Object.assign(this.button.style, this._stylePressed);
                document.addEventListener('mouseup', this, { once: true });
            }
            else if (event.type == 'mouseup') {
                Object.assign(this.button.style, this._style);
            }
        }
        catch (e) {
            console.error(e);
        }
    }
    set innerHtml(html) {
        this._span.innerHTML = html;
    }
}


/***/ }),

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
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'etc-jupyterlab-feedback', // API Namespace
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
/* harmony export */   "IETCJupyterLabFeedbackServiceFactory": () => (/* binding */ IETCJupyterLabFeedbackServiceFactory),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./service */ "./lib/service.js");





const PLUGIN_ID = '@educational-technology-collective/etc_jupyterlab_feedback:plugin';
const IETCJupyterLabFeedbackServiceFactory = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token(PLUGIN_ID);
class ETCJupyterLabFeedbackServiceFactory {
    create({ notebookPanel }) {
        return new _service__WEBPACK_IMPORTED_MODULE_3__.ETCJupyterLabFeedbackService({ notebookPanel });
    }
}
/**
 * Initialization data for the @educational-technology-collective/etc_jupyterlab_configurable_button extension.
 */
const plugin = {
    id: PLUGIN_ID,
    provides: IETCJupyterLabFeedbackServiceFactory,
    autoStart: true,
    optional: [
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookTracker,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry
    ],
    activate: (app, notebookTracker, settingRegistry) => {
        let etcJupyterLabFeedbackServiceFactory = new ETCJupyterLabFeedbackServiceFactory();
        (async () => {
            try {
                await app.started;
                const config = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('config');
                console.log(`${PLUGIN_ID}, ${config.version}`);
                // //// TEST
                // function addButtonToToolbar(notebookPanel: NotebookPanel) {
                //   let etcJupyterLabFeedbackService = etcJupyterLabFeedbackServiceFactory.create({ notebookPanel });
                //   etcJupyterLabFeedbackService.buttonClicked.connect((sender, args) => console.log(args));
                //   etcJupyterLabFeedbackService.resultsDisplayed.connect((sender, args) => console.log(args));
                //   etcJupyterLabFeedbackService.resultsDismissed.connect((sender, args) => console.log(args));
                // }
                // notebookTracker.forEach(addButtonToToolbar);
                // notebookTracker.widgetAdded.connect(async (sender: INotebookTracker, notebookPanel: NotebookPanel) => {
                //   await notebookPanel.revealed;
                //   addButtonToToolbar(notebookPanel);
                // });
                // ////
            }
            catch (e) {
                console.error(e);
            }
        })();
        return etcJupyterLabFeedbackServiceFactory;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/service.js":
/*!************************!*\
  !*** ./lib/service.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ETCJupyterLabFeedbackService": () => (/* binding */ ETCJupyterLabFeedbackService)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _button__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./button */ "./lib/button.js");





class ETCJupyterLabFeedbackService {
    constructor({ notebookPanel }) {
        this._buttonClicked = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._resultsDisplayed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._resultsDismissed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this.handleEvent = this.handleEvent.bind(this);
        this._notebookPanel = notebookPanel;
        let buttonConfig = {
            style: {
                color: 'white',
                backgroundColor: '#00a2ed',
                border: '0px',
                minWidth: '80px'
            },
            stylePressed: {
                backgroundColor: '#0082be'
            },
            innerHTML: 'Feedback'
        };
        this._etcJupyterLabConfigurableTextButton = new _button__WEBPACK_IMPORTED_MODULE_3__.ETCJupyterLabConfigurableTextButton(buttonConfig);
        notebookPanel.toolbar.insertAfter('restart-and-run', 'etc-jupyterlab-configurable-button', new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget({ node: this._etcJupyterLabConfigurableTextButton.node }));
        this._etcJupyterLabConfigurableTextButton.eventTarget.addEventListener('click', this);
    }
    async handleEvent(event) {
        var _a;
        try {
            this._etcJupyterLabConfigurableTextButton.disable();
            let cell = this._notebookPanel.content.activeCell;
            let cells = [
                {
                    id: cell === null || cell === void 0 ? void 0 : cell.model.id,
                    index: this._notebookPanel.content.widgets.findIndex((value) => value == cell)
                }
            ];
            this._buttonClicked.emit({
                eventName: 'validate_button_clicked',
                notebookPanel: this._notebookPanel,
                cells: cells,
                message: ''
            });
            this._etcJupyterLabConfigurableTextButton.innerHtml = 'Feedback...';
            (_a = this._notebookPanel.content.model) === null || _a === void 0 ? void 0 : _a.metadata.set('etc_active_cell', this._notebookPanel.content.activeCellIndex);
            let feedback = (async () => {
                var _a;
                try {
                    if (((_a = this._notebookPanel.content.model) === null || _a === void 0 ? void 0 : _a.metadata.get('etc_feedback')) == true) {
                        return await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('feedback', {
                            body: JSON.stringify({
                                'notebook_path': this._notebookPanel.context.path
                            }),
                            method: 'POST'
                        });
                    }
                    else {
                        return null;
                    }
                }
                catch (e) {
                    console.error(e);
                    return null;
                }
            })();
            let nbgrader = (async () => {
                try {
                    return await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('nbgrader_validate', {
                        body: JSON.stringify({
                            'notebook_path': this._notebookPanel.context.path,
                        }),
                        method: 'POST'
                    });
                }
                catch (e) {
                    console.error(e);
                    return null;
                }
            })();
            let responses = await Promise.all([feedback, nbgrader]);
            let feedbackResponse = responses[0];
            let validationHTML = responses[1];
            let feedbackHTML = feedbackResponse === null || feedbackResponse === void 0 ? void 0 : feedbackResponse.feedback;
            let body = document.createElement('div');
            body.innerHTML = '';
            if (!feedbackHTML) {
                feedbackHTML = `<p>No specific feedback found.</p>`;
            }
            if (!validationHTML) {
                validationHTML = `<p>Validation error.</p>`;
            }
            body.innerHTML = `
            <h2 class="etc-feedback-part">Feedback Results:</h2>
                <p>${feedbackHTML}</p>
                <br>
            <h2 class="etc-feedback-part">Validation Results:</h2>
                <p><pre>${validationHTML}<pre></p>
            `;
            this._resultsDisplayed.emit({
                eventName: 'validation_results_displayed',
                notebookPanel: this._notebookPanel,
                cells: cells,
                message: {
                    'feedback': feedbackResponse,
                    'validation': validationHTML
                }
            });
            await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                title: 'Feedback',
                body: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget({ node: body }),
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton()]
            });
            this._resultsDismissed.emit({
                eventName: 'validation_results_dismissed',
                notebookPanel: this._notebookPanel,
                cells: cells,
                message: {
                    'feedback': feedbackResponse,
                    'validation': validationHTML
                }
            });
        }
        catch (e) {
            console.error(e);
        }
        finally {
            this._etcJupyterLabConfigurableTextButton.innerHtml = "Feedback";
            this._etcJupyterLabConfigurableTextButton.enable();
        }
    }
    get buttonClicked() {
        return this._buttonClicked;
    }
    get resultsDisplayed() {
        return this._resultsDisplayed;
    }
    get resultsDismissed() {
        return this._resultsDismissed;
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.49b998b4dc443cc4ee0d.js.map