import { each } from '@lumino/algorithm';

import { ISignal, Signal } from "@lumino/signaling";

import { Token } from '@lumino/coreutils';

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { requestAPI } from './handler';

import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';

import { ETCJupyterLabFeedbackService } from './service';

const PLUGIN_ID = '@educational-technology-collective/etc_jupyterlab_feedback:plugin';

export const IETCJupyterLabFeedbackServiceFactory = new Token<IETCJupyterLabFeedbackServiceFactory>(PLUGIN_ID);

export interface IETCJupyterLabFeedbackServiceFactory {

  create({ notebookPanel }: { notebookPanel: NotebookPanel }
  ): ETCJupyterLabFeedbackService;
}

class ETCJupyterLabFeedbackServiceFactory implements IETCJupyterLabFeedbackServiceFactory {

  create({
    notebookPanel
  }: {
    notebookPanel: NotebookPanel
  }): ETCJupyterLabFeedbackService {

    return new ETCJupyterLabFeedbackService({ notebookPanel });
  }
}

/**
 * Initialization data for the @educational-technology-collective/etc_jupyterlab_configurable_button extension.
 */
const plugin: JupyterFrontEndPlugin<IETCJupyterLabFeedbackServiceFactory> = {
  id: PLUGIN_ID,
  provides: IETCJupyterLabFeedbackServiceFactory,
  autoStart: true,
  optional: [
    INotebookTracker,
    ISettingRegistry
  ],
  activate: (
    app: JupyterFrontEnd,
    notebookTracker: INotebookTracker,
    settingRegistry: ISettingRegistry | null
  ) => {

    let etcJupyterLabFeedbackServiceFactory = new ETCJupyterLabFeedbackServiceFactory();

    (async () => {
      try {

        await app.started;

        const config = await requestAPI<any>('config');

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

export default plugin;
