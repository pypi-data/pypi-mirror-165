import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { INotebookTracker, KernelError, NotebookPanel } from '@jupyterlab/notebook';

import { IETCJupyterLabTelemetryLibraryFactory } from '@educational-technology-collective/etc_jupyterlab_telemetry_library';

import { IETCJupyterLabNotebookStateProvider } from '@educational-technology-collective/etc_jupyterlab_notebook_state_provider';

import { requestAPI } from './handler';

import { IETCJupyterLabFeedbackServiceFactory } from '@educational-technology-collective/etc_jupyterlab_feedback';

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


const PLUGIN_ID = '@educational-technology-collective/etc_jupyterlab_telemetry_coursera:plugin';

export class AWSAPIGatewayAdapter {

  private _config: any;
  private _etcJupyterLabNotebookStateProvider: IETCJupyterLabNotebookStateProvider;

  constructor(
    { etcJupyterLabNotebookStateProvider, config }:
      { etcJupyterLabNotebookStateProvider: IETCJupyterLabNotebookStateProvider, config: any }
  ) {

    this._etcJupyterLabNotebookStateProvider = etcJupyterLabNotebookStateProvider;

    this._config = config
  }

  async adaptMessage(sender: any, data: INotebookEventMessage) {

    try {

      let notebookState = this._etcJupyterLabNotebookStateProvider.getNotebookState({
        notebookPanel: data.notebookPanel
      });

      var body: any = {
        'event_name': data.eventName,  //  The name of the event.
        'cells': data.cells,  //  The relevant cells.
        'notebook': notebookState?.notebook,  //  The diffed Notebook.
        'seq': notebookState?.seq,  //  The event sequence.
        'session_id': notebookState?.session_id,  //  The session ID.
        'user_id': this._config?.workspace_id ? this._config?.workspace_id : "UNDEFINED",  //  The user ID.
        'notebook_path': data.notebookPanel.context.path,  //  The path of the Notebook.
        'kernel_error': data.kernelError, //  The complete kernel error for cell_errored event.
        'selection': data.selection, //  The selection for copy/cut/paste events.
        'environ': data.environ,  //  All environment variables for open_notebook events.
        'message': data.message //  The message from the feedback extension.
      };

      if (this._config['capture_notebook_events']?.includes(data.eventName)) {

        body['meta'] = data.notebookPanel.content.model?.toJSON();
      }

      let request = { ...body };

      delete request['meta'];

      console.log('Request', request);

      let response = await requestAPI<any>('s3', { method: 'POST', body: JSON.stringify(body) });

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
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [
    INotebookTracker,
    IETCJupyterLabNotebookStateProvider,
    IETCJupyterLabTelemetryLibraryFactory,
    IETCJupyterLabFeedbackServiceFactory
  ],
  activate: (
    app: JupyterFrontEnd,
    notebookTracker: INotebookTracker,
    etcJupyterLabNotebookStateProvider: IETCJupyterLabNotebookStateProvider,
    etcJupyterLabTelemetryLibraryFactory: IETCJupyterLabTelemetryLibraryFactory,
    etcJupyterLabFeedbackServiceFactory: IETCJupyterLabFeedbackServiceFactory,
  ) => {

    let messageAdapter: AWSAPIGatewayAdapter;

    let appConfig = (async () => {

      try {

        await app.started;

        const config = await requestAPI<any>('config');

        console.log(`${PLUGIN_ID}, ${config.version}`);

        if (!config.telemetry) {

          notebookTracker.widgetAdded.disconnect(onWidgetAdded, this);
        }

        return config;
      }
      catch (e) {
        console.error(e);
        notebookTracker.widgetAdded.disconnect(onWidgetAdded, this);
        return false;
      }
    })();

    async function onWidgetAdded(sender: INotebookTracker, notebookPanel: NotebookPanel) {
      //  Handlers must be attached immediately in order to detect early events, hence we do not want to await the appearance of the Notebook.

      let config = await appConfig;

      if (config.telemetry) {

        setInterval(() => {
          if (notebookPanel.content.model?.dirty) {
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

    notebookTracker.widgetAdded.connect(onWidgetAdded, this);
  }
};

export default plugin;
