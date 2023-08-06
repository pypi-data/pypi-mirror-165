import logging
from typing import Dict, Optional
import os
from fastapi import HTTPException
import requests
from autoretouchlib.auth import get_id_token
from retry import retry


class TooManyRequestsOnAiPlatformError(HTTPException):
    pass


class OutOfMemoryError(HTTPException):
    pass


class ServiceUnavailableError(HTTPException):
    pass


class PredictionService:

    def __init__(self, priority: Optional[int] = None, allow_low_quality: bool = False, tries: int = 1):
        self._predict_wrapper = retry((TooManyRequestsOnAiPlatformError, OutOfMemoryError, ServiceUnavailableError),
                                      tries=tries, delay=1, jitter=(0., .5))
        self._priority = priority
        self._allow_low_quality = allow_low_quality

    def predict(self, request: dict, model_url: str) -> Dict:
        return self._predict_wrapper(self._predict)(request, model_url)

    def _predict(self, request: dict, model_url: str) -> Dict:
        """Send json data to a deployed model for prediction.

        Parameters
        ----------
        request: ([Mapping[str: Any]])
            Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
            convertible to Tensors, or (potentially nested) lists of datatypes
            convertible to tensors.
        model_url: to be used for prediction
        Raises
        ------
          RuntimeError
            If googleapiclient returns any error.
        Returns
        -------
        Mapping[str: any]
            dictionary of prediction results defined by the model.

        """
        headers = {}
        if self._priority is not None:
            headers["Workflow-Execution-Priority"] = str(self._priority)
        if os.environ.get("PROXY_LOCAL", False):
            timeout = None
        else:
            id_token = get_id_token(model_url)
            headers["Authorization"] = f"Bearer {id_token}"
            timeout = 30
        for instance in request["instances"]:
            instance["reduce_scales"] = f"{self._allow_low_quality}"
        try:
            proxy_response = requests.post(url=model_url, json=request, headers=headers, timeout=timeout)
            if proxy_response.status_code == 400:
                for instance in request["instances"]:
                    instance.pop("reduce_scales")
                proxy_response = requests.post(url=model_url, json=request, headers=headers, timeout=timeout)
            proxy_response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            if errh.response.status_code == 429:
                raise TooManyRequestsOnAiPlatformError(status_code=errh.response.status_code,
                                                       detail=errh.response.reason)
            if errh.response.status_code == 422:
                raise OutOfMemoryError(status_code=422, detail=errh.response.reason)
            if errh.response.status_code == 503:
                raise ServiceUnavailableError(status_code=503, detail=errh.response.reason)
            logging.error("Http Error: %s", errh)
            raise HTTPException(status_code=errh.response.status_code, detail=errh.response.reason)
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting: %s", errc)
            raise HTTPException(status_code=502, detail="Connection Error")
        except requests.exceptions.Timeout as errt:
            logging.error("Timeout Error: %s", errt)
            raise HTTPException(status_code=504, detail="Timeout")
        except requests.exceptions.RequestException as err:
            logging.error("Unexpected Error: %s", err)
            raise HTTPException(status_code=400, detail=err.response.reason)
        return proxy_response.json()
