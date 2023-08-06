import {ServerConnection} from '@jupyterlab/services';
import axios from "axios";
import { KernelSpecAPI } from '@jupyterlab/services';

interface Configuration {
	ATLAS_BASE_URL: string;
  SN_FILE_LIBRARY_URL: string;
}

const getServerBaseUrl = (settings: ServerConnection.ISettings): string => {
  let baseUrl = settings.baseUrl;
  // Add the trailing slash if it is missing.
  if (!baseUrl.endsWith('/')) {
    baseUrl += '/';
  }
  return baseUrl;
}

export const ATLAS_BASE_URL = await (async (): Promise<string> => {
	const currentUrl = window.location.href;

	const parameters = new URL(currentUrl).searchParams;
	const baseUrl: string | undefined = parameters.get('atlas_base_url')!;
	if (baseUrl === null) {
		const init: RequestInit = {
			method: 'GET',
		};
		const settings = ServerConnection.makeSettings();
		const requestUrl = getServerBaseUrl(settings) + 'skillsnetwork-authoring-extension/config';
    const response = await ServerConnection.makeRequest(
			requestUrl,
			init,
			settings,
		);
		const configuration: Configuration
      = (await response.json()) as Configuration;
		return configuration.ATLAS_BASE_URL;
  } else {
    return decodeURIComponent(baseUrl)
  }
})();

export const SN_FILE_LIBRARY_URL = await (async (): Promise<string> => {
	const currentUrl = window.location.href;

	const parameters = new URL(currentUrl).searchParams;
	const snFileLibraryURL: string | undefined = parameters.get('sn_file_library_url')!;
	if (snFileLibraryURL === null) {
		const init: RequestInit = {
			method: 'GET',
		};
		const settings = ServerConnection.makeSettings();
		const requestUrl = getServerBaseUrl(settings) + 'skillsnetwork-authoring-extension/config';
    const response = await ServerConnection.makeRequest(
			requestUrl,
			init,
			settings,
		);
		const configuration: Configuration
      = (await response.json()) as Configuration;
		return configuration.SN_FILE_LIBRARY_URL;
  } else {
    return decodeURIComponent(snFileLibraryURL)
  }
})();

/**
 * Extracts the session token. Will first try to get a token via the URL, if none was found then try to get the token via cookie.
 *
 * @returns token
 */
 export const MODE = async (): Promise<string> => {

  const currentURL = window.location.href;
  const params = new URL(currentURL).searchParams;
  let mode: string | null = params.get('mode');

  return mode == "learn" ? mode : "author";
};


/**
 * Extracts the session token. Will first try to get a token via the URL, if none was found then try to get the token via cookie.
 *
 * @returns token
 */
export const ATLAS_TOKEN = async (): Promise<string> => {
  const currentURL = window.location.href;
  const params = new URL(currentURL).searchParams;
  let token: string | null = sessionStorage.getItem('atlas_token');

  if (token === null) {
    const token_from_query = params.get('atlas_token')
    token = (token_from_query !== null) ? token_from_query : 'NO_TOKEN'
  }

  Globals.TOKEN = token;
  return token;
};

export const SET_DEFAULT_LAB_NAME_AND_KERNEL = async (): Promise<string> => {
const currentURL = window.location.href;
  const params = new URL(currentURL).searchParams;
  let env_type = params.get('env_type')

  if (env_type !== "jupyterlab" && env_type !== "jupyterlite"){
    env_type = "local"
  }

  console.log("Env type: ", env_type)

  if (env_type === 'jupyterlab' || env_type === "local") {
    // In production, jupyterlab doesn't have python3 as a kernel option so use python
    Globals.PY_KERNEL_NAME = await GET_PYKERNEL();
    Globals.DEFAULT_LAB_NAME = 'lab.ipynb';
  } else if (env_type === 'jupyterlite'){
    Globals.PY_KERNEL_NAME = 'python'
    Globals.DEFAULT_LAB_NAME = 'lab.jupyterlite.ipynb';
  }
  return env_type
}

/**
 * Gets the python kernel. If more than one python kernel is found, prioritize python3. If only one python kernel is found, select that kernel
 *
 * @returns pykernel
 */
export const GET_PYKERNEL = async (): Promise<string> => {
  // Get the available kernels
  let kspecs = await (await KernelSpecAPI.getSpecs()).kernelspecs;

  function checkPython(spec: string){
    return spec.includes('python')
  }

  let keys = Object.keys(kspecs)
  // filter for only the spec names with python in it, sorted
  let filtered_keys = keys.filter(checkPython).sort()
  // return the priority python
  let pykernel = filtered_keys[filtered_keys.length-1];

  return pykernel
}

export var CancelToken = axios.CancelToken;
export var source = CancelToken.source();

// Global variables
export class Globals {
  public static TOKEN: string;
  public static PY_KERNEL_NAME: string;
  public static DEFAULT_LAB_NAME: string;
}
