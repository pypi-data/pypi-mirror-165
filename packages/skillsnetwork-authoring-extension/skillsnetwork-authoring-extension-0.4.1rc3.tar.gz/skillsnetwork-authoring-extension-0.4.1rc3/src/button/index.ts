/* eslint-disable prettier/prettier */
/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
/* eslint-disable @typescript-eslint/ban-types */
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { Dialog, ToolbarButton } from '@jupyterlab/apputils';
import { IDisposable, DisposableDelegate } from '@lumino/disposable';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { getFileContents, getLabFileName, loadLabContents } from '../tools';
import { axiosHandler, postLabModel, getLabModel } from '../handler';
import { showFailureImportLabDialog } from '../dialog';
import { Globals } from '../config';
import * as nbformat from '@jupyterlab/nbformat';
import { ATLAS_TOKEN, SET_DEFAULT_LAB_NAME_AND_KERNEL, MODE } from '../config';

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  NotebookPanel,
  INotebookModel,
  INotebookTracker
} from '@jupyterlab/notebook';

import { SkillsNetworkFileLibrary } from '../sn-file-library';

/**
 * The plugin registration information.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  activate,
  id: 'skillsnetwork-authoring-extension:plugin',
  autoStart: true,
  requires: [IMainMenu, INotebookTracker, IDocumentManager],
};

/**
 * A notebook widget extension that adds a button to the toolbar.
 */
export class ButtonExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  /**
   * Create a new extension for the notebook panel widget.
   *
   * @param panel Notebook panel
   * @param context Notebook context
   * @returns Disposable on the added button
   */
  createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>
  ): IDisposable {
    const start = async () => {
      // Get the current file contents
      const file = await getFileContents(panel, context);
      // POST to Atlas the file contents/lab model
      postLabModel(axiosHandler(Globals.TOKEN), file);
    };

    const publishButton = new ToolbarButton({
      className: 'publish-lab-button',
      label: 'Publish on SN',
      onClick: start,
      tooltip: 'Publish Lab'
    });

    const snFileLibraryButton = new ToolbarButton({
      className: 'sn-file-library-button',
      label: 'SN File Library',
      onClick: () =>  (new SkillsNetworkFileLibrary()).launch(),
      tooltip: 'Skills Network File Library'
    });

    panel.toolbar.insertItem(9, 'sn-file-library', snFileLibraryButton);
    panel.toolbar.insertItem(10, 'publish', publishButton);
    return new DisposableDelegate(() => {
      publishButton.dispose();
      snFileLibraryButton.dispose();
    });
  }
}

/**
 * Activate the extension.
 *
 * @param app Main application object
 */
async function activate(app: JupyterFrontEnd, mainMenu: IMainMenu, notebookTracker: INotebookTracker, docManager: IDocumentManager) {

  console.log("Activated skillsnetwork-authoring-extension button plugin!");

  if (await MODE() == "learn") return

  // init the token
  const token = await ATLAS_TOKEN();

  //init globals
  const env_type = await SET_DEFAULT_LAB_NAME_AND_KERNEL()

  console.log('Using default kernel: ', Globals.PY_KERNEL_NAME);

  // Add the Publish widget to the lab environment
  app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());

  // Try to load up a notebook when author is using the browser tool (not in local)
  app.restored.then(async () => {
    if (token !== 'NO_TOKEN' && env_type !== "local"){
      try{
        let {instructions_file_path, body: instructions_content} = await getLabModel(axiosHandler(token))
        const labFilename = getLabFileName(instructions_file_path);
        // Attempt to open the lab
        const nbPanel = docManager.createNew(labFilename, 'notebook', { name:  Globals.PY_KERNEL_NAME} ) as NotebookPanel;
        if (nbPanel === undefined) {
          throw Error('Error loading lab')
        }
        loadLabContents(nbPanel, JSON.parse(instructions_content) as unknown as nbformat.INotebookContent);
      }
      catch (e){
        Dialog.flush() // remove spinner
        showFailureImportLabDialog();
        Globals.TOKEN = "NO_TOKEN";
        console.log(e)
      }
    }
  })
}

/**
 * Export the plugin as default.
 */
export default plugin;
