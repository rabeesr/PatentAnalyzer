from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Date, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from external_api_routes.patent_routes import *
from external_api_routes.gemeni_routes import *
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
from database import *

# Initialize FastAPI
app = FastAPI()
app.db = DataBase()

@app.get("/search_patents")
def store_patents(search_all: str = "", filing_start_date: str = "", filing_end_date: str = "", grant_date: str = "",
                  patent_number: str = "", inventor_name: str = "", invention_title: str = "", applicant_name: str = "", city: str = "", state: str = ""):
    
    search_results = dict()
    #construct the query term necessary to pass into the JSON based on whether fields are filled out or now
    q= ''

    if search_all:
        if not q == '':
            q = q + ' AND "' + search_all + '"'
        else:
            q = '"' + search_all + '"'

    if patent_number:
        if not q == '':
            q = q + ' AND ' + 'applicationMetaData.patentNumber:"' + patent_number + '"'
        else:
            q = 'applicationMetaData.patentNumber:"' + patent_number + '"'
    
    if applicant_name:
        if not q == '':
            q = q + ' AND ' + 'applicationMetaData.firstApplicantName:"' + applicant_name + '"'
        else:
            q = 'applicationMetaData.firstApplicantName:"' + applicant_name + '"'
    
    if inventor_name:
        if not q == '':
            q = q + ' AND ' + 'applicationMetaData.firstInventorName:"' + inventor_name + '"'
        else:
            q = 'applicationMetaData.firstInventorName:"' + inventor_name + '"'
    if invention_title:
        if not q == '':
            q = q + ' AND ' + 'applicationMetaData.inventionTitle:"' + invention_title + '"'
        else:
            q = 'applicationMetaData.inventionTitle:"' + invention_title + '"'
    if city:
        if not q == '':
            q = q + ' AND ' + 'correspondenceAddressBag.cityName:"' + city + '"'
        else:
            q = 'correspondenceAddressBag.cityName:"' + city + '"'
    if state:
        if not q == '':
            q = q + ' AND ' + 'correspondenceAddressBag.geographicRegionName:"' + state + '"'
        else:
            q = 'correspondenceAddressBag.geographicRegionName:"' + state + '"'

    json_payload = create_json_payload(q=q, filing_start_date=filing_start_date, filing_end_date= filing_end_date)
    resp = make_search_request(PATENT_SEARCH_URL, json_payload=json_payload)
    api_call_number = 0
    search_results["count"] = resp.json()["count"]
    search_results[f"attempt{api_call_number}"] = resp.json()["patentFileWrapperDataBag"]
    if resp.json()["count"] > 100:
        # setting to a conservative limit of 3 to reduce likelihood of hitting daily limit for testing purposes. Can make this bigger in a production environmment
        api_call_limit = 1
        offset = 0
        while search_results["count"] - (offset + 100) >= 0 and api_call_number < api_call_limit:
            offset = offset + 100
            json_payload2 = create_json_payload(q=q, filing_start_date=filing_start_date, filing_end_date= filing_end_date, offset = offset)
            resp = make_search_request(PATENT_SEARCH_URL, json_payload=json_payload2)
            api_call_number += 1
            search_results[f"attempt{api_call_number}"] = resp.json()
    for x in search_results:
        if x == "count":
            pass
        else:
            for y in search_results[x]:
                try:
                    application_number = y['applicationNumberText']
                except:
                    continue
                else:
                    application_number = y['applicationNumberText']
                    concat_dict =  y['applicationMetaData'] | y['correspondenceAddressBag'][0] | {"applicationNumberText":y['applicationNumberText']}
                    app.db.put(application_number, concat_dict)
    return app.db.all()

# Return all stored patent data
@app.get("/all_patents")
def return_all_patents():
    return app.db.all()
    

# summarize patent data
@app.get("/summarize_patent")
def summarize_patent(application_number):
    response = get_patent_docs(PATENT_DOC_URL, application_number=application_number)
    #helper function to get the download URL of the selected patent
    
    def find_pdf_spec_url(data):
        for document in data.get('documentBag', []):
            if document.get('documentCode') == 'SPEC':
                for download in document.get('downloadOptionBag', []):
                    if download.get('mimeTypeIdentifier') == 'PDF':
                        return download.get('downloadUrl')
        return None
    #test with 18537570
    # Find and print the PDF URL
    pdf_url = find_pdf_spec_url(response.json())
    if pdf_url:
        response2 = requests.get(pdf_url, headers=headers)
        if response2.status_code == 200:
            with open("./contents/PatentSpec.pdf", 'wb') as file:
                file.write(response2.content)
            return 'File downloaded successfully'
        else:
            return 'Failed to download file'

# # Generate line chart data
# @app.get("/line_chart")
# def generate_line_chart():
#     x = list(range(10))
#     y = [val**2 for val in x]  # Example quadratic function
#     return {"x": x, "y": y}

# # Save a report (mock function)
# @app.post("/save_report")
# def save_report():
#     return {"message": "Report saved successfully"}

@app.delete("/clear_db")
def clear_db_table():
    return app.db.clear_all()
