#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app
import json

from .http_client import FCMHttpClient
from .classes import *


def checkForFCMError(response):
    if response.status_code != 200:
        jsonResponse = json.loads(response.text)
        errorBody = jsonResponse.get('error', None)
        if errorBody is not None:
            return ErrorResult(Exception(errorBody['message']))
        else:
            return ErrorResult(Exception("Unable to parse error code: " + str(response.status_code)))
    else:
        return None


class FCMClient:

    def __init__(self):
        self.http_client = FCMHttpClient()

    def sendPush(self, to, data, ttl="86400"):
        requestResult = self.http_client.post_json_request("fcm/send", {
            "to": to, "ttl": ttl, "data": data
        })
        if requestResult.is_error():
            return requestResult
        error_check = checkForFCMError(requestResult.get_response())
        if error_check is not None:
            return error_check
        return PushSendRequest(True)
