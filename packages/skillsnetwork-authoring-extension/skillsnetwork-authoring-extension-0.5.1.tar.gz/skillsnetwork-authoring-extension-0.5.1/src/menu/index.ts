import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { Menu, Widget } from '@lumino/widgets';
import { Dialog, showDialog } from '@jupyterlab/apputils';
import { INotebookTracker, NotebookPanel,   } from '@jupyterlab/notebook';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { show_spinner, showFailureImportLabDialog } from '../dialog';
import { getLabFileName, loadLabContents } from '../tools';
import { axiosHandler, getLabModel } from '../handler';
import * as nbformat from '@jupyterlab/nbformat';
import { Globals, MODE } from '../config';

export const menu: JupyterFrontEndPlugin<void> = {
  id: 'skillsnetwork-authoring-extension:menu',
  autoStart: true,
  requires: [IMainMenu, INotebookTracker, IDocumentManager],
  activate: async (app: JupyterFrontEnd, mainMenu: IMainMenu, notebookTracker: INotebookTracker, docManager: IDocumentManager) => {

    console.log('Activated skillsnetwork-authoring-extension menu plugin!');

    if (await MODE() == "learn") return

    const editLabFromToken = 'edit-lab-from-token';
    app.commands.addCommand(editLabFromToken, {
    label: 'Edit a Lab',
    execute: () => {
      showTokenDialog(notebookTracker, docManager);
    }
    })

    const { commands } = app;

    // Create a new menu
    const menu: Menu = new Menu({ commands });
    menu.title.label = 'Skills Network';
    mainMenu.addMenu(menu, { rank: 80 });

    // Add command to menu
    menu.addItem({
    command: editLabFromToken,
    args: {}
    });

    const showTokenDialog = (notebookTracker: INotebookTracker, docManager: IDocumentManager) => {

      // Generate Dialog body
      let bodyDialog = document.createElement('div');
      let nameLabel = document.createElement('label');
      nameLabel.textContent = "Enter your authorization token: "
      let tokenInput = document.createElement('input');
      tokenInput.className = "jp-mod-styled";
      bodyDialog.appendChild(nameLabel);
      bodyDialog.appendChild(tokenInput);

      showDialog({
        title: "Edit a Lab",
        body: new Widget({node: bodyDialog}),
        buttons: [Dialog.cancelButton(), Dialog.okButton()]
      }).then(async result => {
        if (result.button.accept){
          show_spinner('Loading up your lab...');

          const token = tokenInput.value
          let {instructions_file_path, body: instructions_content} = await getLabModel(axiosHandler(token))
          const labFilename = getLabFileName(instructions_file_path);

          // Attempt to open the lab
          const nbPanel = docManager.createNew(labFilename, 'notebook', { name:  Globals.PY_KERNEL_NAME}) as NotebookPanel;

          if (nbPanel === undefined) {
            throw Error('Error loading lab')
          }
          loadLabContents(nbPanel, JSON.parse(instructions_content) as unknown as nbformat.INotebookContent);
          Globals.TOKEN = tokenInput.value;
          sessionStorage.setItem('atlas_token', Globals.TOKEN);
        }
      })
      .catch((e) => {
        Dialog.flush(); //remove spinner
        showFailureImportLabDialog();
        console.log(e)
      });
    };
  }
};
