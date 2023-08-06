/* eslint-disable no-async-promise-executor */
import { AxiosError, AxiosInstance } from 'axios';
import { show_spinner, showSuccessPublishDialog, showFailurePublishDialog } from './dialog';
import { Dialog } from '@jupyterlab/apputils';
import { ATLAS_BASE_URL } from './config';
import axios from 'axios';
import { source } from './config';

export const axiosHandler = (lab_token: string): AxiosInstance => {
  const atlasClient = axios.create({
      baseURL: ATLAS_BASE_URL,
      headers: {
        Authorization: `Bearer ${lab_token}`,
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        "Accept": 'application/json'
      }
    });
  return atlasClient;
}

/**
 * GET the lab model / JSON that represents a .ipynb file/notebook from ATLAS
 *
 * @param axiosHandler Axios client that contains a JWT Bearer token
 * @returns Promise<void>
 */
export const getLabModel = (axiosHandler: AxiosInstance) => {
  // GET the lab model
  return axiosHandler
    .get('v1/labs')
    .then(result => {
      Dialog.flush(); //remove spinner
      return result.data;
    })
    .catch(error => {
      console.log(error);
      throw "Failed to fetch notebook"
    });
};

/**
 * POST the lab model / JSON from the .ipynb file/notebook to ATLAS
 *
 * @param axiosHandler Axios client that contains a JWT Bearer token
 * @returns Promise<void>
 */
export const postLabModel = async (
  axiosHandler: AxiosInstance,
  labModel: string
): Promise<void> => {
  show_spinner('Publishing your lab onto Skills Network...');
  return new Promise<void>(async (resolve, reject) => {
    await axiosHandler
      .post('v1/labs', {
        body: labModel
      },{
        cancelToken: source.token,
      })
      .then(res => {
        console.log('SUCCESSFULLY PUSHED', res);
        Dialog.flush(); //remove spinner
        showSuccessPublishDialog();
        resolve;
      })
      .catch((error: AxiosError) => {
        console.log(error);
        Dialog.flush(); // remove spinner
        showFailurePublishDialog();
        reject;
      });
  });
};
