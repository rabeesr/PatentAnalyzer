import requests
import json
import time
import random
from typing import *

SLEEP_AFTER_429 = 0.1
SLEEP_BETWEEN_HTTP = 0
HTTP_RETRY = 5
MAX_FILES = 2
total_429 = 0
total_rate = 0
API_KEY = "zbncijprczprbxnvxksauznwwdxzot"
PATENT_SEARCH_URL = 'https://api.uspto.gov/api/v1/patent/applications/search'
PATENT_DOC_URL = 'https://api.uspto.gov/api/v1/patent/applications/'
DEFAULT_LIMIT = 100

headers = {
    'X-API-KEY': API_KEY,
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

LIST_OF_FIELDS = [
    'applicationNumberText',
    'applicationMetaData.inventionTitle',
    'applicationMetaData.patentNumber',
    'applicationMetaData.smallEntityStatusIndicator',
    'applicationMetaData.nationalStageIndicator',
    'applicationMetaData.firstApplicantName',
    'applicationMetaData.firstInventorName',
    'applicationMetaData.applicationStatusDescriptionText',
    'applicationMetaData.applicationStatusCode',
    'applicationMetaData.applicationStatusDate',
    'applicationMetaData.filingDate',
    'applicationMetaData.applicationTypeCode',
    'applicationMetaData.applicationTypeLabelName',
    'applicationMetaData.applicationTypeCategory',
    'applicationMetaData.filingDate',
    'applicationMetaData.grantDate',
    'correspondenceAddressBag.geographicRegionName',
    'correspondenceAddressBag.cityName',
    'correspondenceAddressBag.countryName'
]

def create_json_payload(q: str = None, filing_start_date: Optional[str] = None, filing_end_date: Optional[str] = None,
                        offset: int = 0,limit: int = DEFAULT_LIMIT, sort: Optional[List] = None):
    """
    Constructs a JSON structure for a patent search query.

    Parameters:
        q (str, optional): The search query string.
        filters (list of dict, optional): List of filter dictionaries.
        range_filters (list of dict, optional): List of range filter dictionaries.
        offset (int, optional): Pagination offset, default is 0.
        limit (int, optional): Pagination limit, default is 100.
        sort (list of dict, optional): List of sorting criteria.

    Returns:
        dict: JSON-compatible dictionary representing the patent search query.
    """

    query = {}

    if q:
        query["q"] = q
    
    query["filters"] = [
    {
      "name": "applicationMetaData.applicationStatusDescriptionText",
      "value": [
        "Patented Case"
      ]
    }
    ]

    query["rangeFilters"] = [
     {
      "field": "applicationMetaData.filingDate",
      "valueFrom": filing_start_date, 
      "valueTo": filing_end_date
     }
    ]


    query["pagination"] = {
        "offset": offset,
        "limit": limit
    }

    query["sort"] = [
    {
      "field": "applicationMetaData.filingDate",
      "order": "desc"
    }
  ]

    query["fields"] = LIST_OF_FIELDS

    return query


def make_search_request(base_url, json_payload, retry=0):
    global total_429
    response = requests.post(base_url, headers=headers, json=json_payload)
    if response.status_code == 429 and retry < HTTP_RETRY:
        time.sleep(SLEEP_AFTER_429)
        retry += 1
        total_429 += 1
        print(f"Got HTTP 429. Retry number: {retry}")
        return make_search_request(base_url, retry, json_payload=json_payload)
    else:
        print('Sorry maximum retries exceeded, server not available. Please try again later')
    return response


def get_patent_docs(base_url, application_number, retry=0):
    global total_429
    doc_url = f'{base_url}{application_number}/documents'
    response = requests.get(doc_url, headers=headers)
    if response.status_code == 429 and retry < HTTP_RETRY:
        time.sleep(SLEEP_AFTER_429)
        retry += 1
        total_429 += 1
        print(f"Got HTTP 429. Retry number: {retry}")
        response = get_patent_docs(doc_url, application_number, retry)
    else:
        print('Sorry maximum retries exceeded, server not available. Please try again later')
    return response

# response = make_search_request(PATENT_SEARCH_URL, 
#                                json_payload= {
#   "q": "applicationMetaData.firstApplicantName:\"Apple\"",
#   "filters": [
#     {
#       "name": "applicationMetaData.applicationStatusDescriptionText",
#       "value": [
#         "Patented Case"
#       ]
#     }
#   ],
#   "rangeFilters": [
#     {
#       "field": "applicationMetaData.filingDate",
#       "valueFrom": "2024-03-05",
#       "valueTo": "2025-03-05"
#     }
#   ],
#   "pagination": {
#     "offset": 0,
#     "limit": 100
#   },
#   "sort": [
#     {
#       "field": "applicationMetaData.filingDate",
#       "order": "desc"
#     }
#   ],
#   "fields": [
#     "applicationNumberText",
#     "applicationMetaData.inventionTitle",
#     "applicationMetaData.patentNumber",
#     "applicationMetaData.smallEntityStatusIndicator",
#     "applicationMetaData.nationalStageIndicator",
#     "applicationMetaData.firstApplicantName",
#     "applicationMetaData.firstInventorName",
#     "applicationMetaData.applicationStatusDescriptionText",
#     "applicationMetaData.applicationStatusCode",
#     "applicationMetaData.applicationStatusDate",
#     "applicationMetaData.filingDate",
#     "applicationMetaData.applicationTypeCode",
#     "applicationMetaData.applicationTypeLabelName",
#     "applicationMetaData.applicationTypeCategory",
#     "applicationMetaData.filingDate",
#     "applicationMetaData.grantDate",
#     "correspondenceAddressBag.geographicRegionName",
#     "correspondenceAddressBag.cityName",
#     "correspondenceAddressBag.countryName"
#   ]
# })

# print(response.json())
# response2 = get_patent_docs(PATENT_DOC_URL, "29930834")
# # # # response3 = requests.get("https://api.uspto.gov/api/v1/download/applications/18540269/LQ5PPXONGREENX2.pdf", headers=headers)
# print(response2.json())

# if response3.status_code == 200:
#     with open("./contents/File.pdf", 'wb') as file:
#         file.write(response3.content)
#     print('File downloaded successfully')
# else:
#     print('Failed to download file')
# print(response3.url)