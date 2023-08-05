import { Widget } from '@lumino/widgets';
import { ISignal, Signal } from "@lumino/signaling";
import { INotebookTracker, Notebook, NotebookPanel, KernelError } from '@jupyterlab/notebook';
import { INotebookContent } from '@jupyterlab/nbformat';
import { requestAPI } from './handler';
import {
    Cell,
    ICellModel
} from '@jupyterlab/cells';

import {
    showDialog,
    Dialog
} from '@jupyterlab/apputils';

import { ETCJupyterLabConfigurableTextButton, IETCJupyterLabConfigurableTextButtonOptions } from './button';

export interface ICellMeta {
    index: number;
    id: any;
}

export interface INotebookEventMessage {
    eventName: string;
    cells: Array<ICellMeta>;
    notebookPanel: NotebookPanel;
    kernelError?: KernelError | null | undefined;
    selection?: string;
    meta?: any;
    environ?: object,
    message?: any
}

export interface IETCJupyterLabFeedbackService {
    buttonClicked: ISignal<ETCJupyterLabFeedbackService, INotebookEventMessage>;
    resultsDisplayed: ISignal<ETCJupyterLabFeedbackService, INotebookEventMessage>;
    resultsDismissed: ISignal<ETCJupyterLabFeedbackService, INotebookEventMessage>;
}

export class ETCJupyterLabFeedbackService {

    private _buttonClicked: Signal<ETCJupyterLabFeedbackService, INotebookEventMessage> = new Signal(this);
    private _resultsDisplayed: Signal<ETCJupyterLabFeedbackService, INotebookEventMessage> = new Signal(this);
    private _resultsDismissed: Signal<ETCJupyterLabFeedbackService, INotebookEventMessage> = new Signal(this);

    private _notebookPanel: NotebookPanel;
    private _etcJupyterLabConfigurableTextButton: ETCJupyterLabConfigurableTextButton;

    constructor({
        notebookPanel
    }: {
        notebookPanel: NotebookPanel
    }) {
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
        }

        this._etcJupyterLabConfigurableTextButton = new ETCJupyterLabConfigurableTextButton(buttonConfig);

        notebookPanel.toolbar.insertAfter(
            'restart-and-run',
            'etc-jupyterlab-configurable-button',
            new Widget({ node: this._etcJupyterLabConfigurableTextButton.node })
        );

        this._etcJupyterLabConfigurableTextButton.eventTarget.addEventListener('click', this);
    }

    async handleEvent(event: Event) {

        try {

            this._etcJupyterLabConfigurableTextButton.disable();

            let cell = this._notebookPanel.content.activeCell;

            let cells = [
                {
                    id: cell?.model.id,
                    index: this._notebookPanel.content.widgets.findIndex((value: Cell<ICellModel>) => value == cell)
                }
            ];

            this._buttonClicked.emit({
                eventName: 'validate_button_clicked',
                notebookPanel: this._notebookPanel,
                cells: cells,
                message: ''
            });

            this._etcJupyterLabConfigurableTextButton.innerHtml = 'Feedback...';

            this._notebookPanel.content.model?.metadata.set(
                'etc_active_cell',
                this._notebookPanel.content.activeCellIndex
            );

            let feedback = (async () => {
                try {
                    if (this._notebookPanel.content.model?.metadata.get('etc_feedback') == true) {
                        return await requestAPI<any>('feedback', {
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
                    return await requestAPI<any>('nbgrader_validate', {
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

            let feedbackHTML = feedbackResponse?.feedback;

            let body = document.createElement('div');
            body.innerHTML = '';

            if (!feedbackHTML) {
                feedbackHTML = `<p>No specific feedback found.</p>`
            }


            if (!validationHTML) {
                validationHTML = `<p>Validation error.</p>`
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

            await showDialog({
                title: 'Feedback',
                body: new Widget({ node: body }),
                buttons: [Dialog.okButton()]
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

    get buttonClicked(): ISignal<ETCJupyterLabFeedbackService, INotebookEventMessage> {
        return this._buttonClicked;
    }

    get resultsDisplayed(): ISignal<ETCJupyterLabFeedbackService, INotebookEventMessage> {
        return this._resultsDisplayed;
    }

    get resultsDismissed(): ISignal<ETCJupyterLabFeedbackService, INotebookEventMessage> {
        return this._resultsDismissed;
    }
}
