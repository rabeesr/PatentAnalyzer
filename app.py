# https://github.com/imwilsonxu/fbone
import requests
import json
import time
import random

SLEEP_AFTER_429 = 0.1
SLEEP_BETWEEN_HTTP = 0
HTTP_RETRY = 5
MAX_FILES = 10
total_429 = 0
total_rate = 0

api_key = "ohY7iVcf.B6TG9410k9Q663YwfwUdpJfiMTiIUZPV"
url = 'https://search.patentsview.org/api/v1/patent/?q={"_gte":{"patent_date":"2007-01-09"}}'
apllication_id = "12345678"


headers = {
    'x-api-key': api_key
}


def make_search_request(file_url, retry=0):
    global total_429
    response = requests.get(file_url, headers=headers)
    if response.status_code == 429 and retry < HTTP_RETRY:
        time.sleep(SLEEP_AFTER_429)
        retry += 1
        total_429 += 1
        print(f"Got HTTP 429. Retry number: {retry}")
        return make_search_request(file_url, retry)
    return response

resp = make_search_request(url)
print(resp.json())

print(resp)
