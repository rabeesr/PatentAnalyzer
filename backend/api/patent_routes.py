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
applicationNumberText = '18540269'

sample_json = {
    "q": "Nanobody",
    "filters": [
        {
        "name": "applicationMetaData.applicationTypeLabelName",
        "value": [
            "Utility"
        ]
        }
    ],
    "rangeFilters": [
        {
        "field": "applicationMetaData.filingDate",
        "valueFrom": "2022-01-01",
        "valueTo": "2023-12-31"
        }
    ],
    "pagination": {
        "offset": 0,
        "limit": 1
    },
    "sort": [
        {
        "field": "applicationMetaData.filingDate",
        "order": "Desc"
        }
    ],
    "fields": [
    "applicationNumberText",
    "applicationMetaData.filingDate",
    "applicationMetaData.firstInventorName",
    "applicationMetaData.firstApplicantName",
    "applicationMetaData.applicationStatusDate",
    "applicationMetaData.applicationStatusCode",
    "applicationMetaData.applicationStatusDescriptionText",
    "applicationMetaData.filingDate",
    "applicationMetaData.applicationTypeCode",
    "applicationMetaData.applicationTypeLabelName",
    "applicationMetaData.applicationTypeCategory",
    "applicationMetaData.inventionTitle",
    "applicationMetaData.patentNumber",
    "applicationMetaData.applicationTypeCategory",
    "correspondenceAddressBag.geographicRegionName",
    "correspondenceAddressBag.cityName",
    "pgpubDocumentMetaData.fileLocationURI",
    "documentBag"
    ]
    }

API_KEY = "zbncijprczprbxnvxksauznwwdxzot"
URL = 'https://api.uspto.gov/api/v1/patent/applications/search/'
firstApplicantName = 'applicationMetaData.firstApplicantName:Apple*'
limit = 1

headers = {
    'X-API-KEY': API_KEY,
    'accept': 'application/json'
}

LIST_OF_FIELDS = [
    'applicationMetaData.firstApplicantName',
    'applicationMetaData.firstInventorName',
    'applicationMetaData.applicationStatusDescriptionText',
    'applicationMetaData.applicationStatusDate',
    'applicationMetaData.filingDate',
    'applicationMetaData.applicationTypeCode',
    'applicationMetaData.applicationTypeLabelName',
    'applicationMetaData.applicationTypeCategory',
    'applicationMetaData.filingDate',
    'applicationMetaData.inventionTitle',
    'applicationMetaData.patentNumber'
]

LIST_OF_FIELDS2 = [
    'applicationMetaData.firstApplicantName',
    'applicationMetaData.firstInventorName'
]


def make_search_request(base_url, retry=0):
    global total_429
    s = '%2'.join(x for x in LIST_OF_FIELDS2)
    file_url = base_url + '&q=' + f'{firstApplicantName}' + f'&limit=1' + f'&fields={s}'
    print(file_url)
    response = requests.post(base_url, headers=headers, json=sample_json)
    if response.status_code == 429 and retry < HTTP_RETRY:
        time.sleep(SLEEP_AFTER_429)
        retry += 1
        total_429 += 1
        print(f"Got HTTP 429. Retry number: {retry}")
        return make_search_request(file_url, retry)
    return response

resp = make_search_request(URL)
response2 = requests.get(f"https://api.uspto.gov/api/v1/patent/applications/18540269/documents", headers=headers)
response3 = requests.get("https://api.uspto.gov/api/v1/download/applications/18540269/LQ5PPXONGREENX2.pdf", headers=headers)
#print(resp.json())
#print(response2.json())
file_Path = 'research_Paper_1.pdf'

if response3.status_code == 200:
    with open("./content.pdf", 'wb') as file:
        file.write(response3.content)
    print('File downloaded successfully')
else:
    print('Failed to download file')
print(response3.url)