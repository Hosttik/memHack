import axios from "axios";
import { app } from "src/config/config";
import { AXIOS_TIMEOUT } from "src/constants";

const createNetworkAdapter = config => axios.create(config);

const apiInstance = createNetworkAdapter({
  baseURL: `${app.host}${app.apiPrefix}/${app.apiVersion}`,
  timeout: AXIOS_TIMEOUT
});

const errorHandler = (err, method, url) => {
  console.error(err, method, url);
};

const requestFactory = (instance, method, commonConfig, withParams) => async (
  url,
  params = null,
  reqConfig = {}
) => {
  const config = {
    ...commonConfig,
    ...reqConfig
  };
  const processedParams = method === "get" ? { params } : params;

  const instanceOptions = withParams
    ? [url, processedParams, config]
    : [url, config];

  try {
    const result = await instance[method](...instanceOptions);
    return result.data;
  } catch (err) {
    errorHandler(err, method, url);
  }
};

const createRequest = (instance, commonConfig) => {
  return {
    get: requestFactory(instance, "get", commonConfig, true),
    head: requestFactory(instance, "head", commonConfig, false),
    delete: requestFactory(instance, "delete", commonConfig, false),
    post: requestFactory(instance, "post", commonConfig, true),
    put: requestFactory(instance, "put", commonConfig, true),
    patch: requestFactory(instance, "patch", commonConfig, true)
  };
};

export const apiHost = createRequest(apiInstance, {});
