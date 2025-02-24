# PatentAnalyzer
Final Project for MPCS Python Programming

**Project Description**
I would like to develop an application which allows users to analyze information from the US Patent Office. The application will allow users to interact with it via the command line to support the following methods/actions. I will use the Patent search API developed in partnership with the US Patents Office found here: https://search.patentsview.org/docs/docs/Search%20API/SearchAPIReference/?_gl=1*ote6kb*_ga*NTY4NjY0OTQyLjE3Mzc1NjY1MTM.*_ga_K4PTTLH074*MTczNzU2NjUxMy4xLjEuMTczNzU2NjUyNy40Ni4wLjA.

Here are some preliminary methods that I would like to develop. I am not going to limit myself to these methods and will continuosuly refine the features based upon feasibility and end user value.

**Potential Features**

    * Provide analysis on the number of patents filed within a designated date period
    * Allow the user to search patents by keywords or strings or across a combination of fields (i.e. combinations of attributes such as inventor, filing date, keyword, geography, etc.)
    * Allow the user to search the patent by different market sectors (i.e. healthcare, tech, etc.)
    * Allow the user to check on the status of a patent by providing the patent API
    * I would like to see if I can collate all the information returned from the query and send it to an LLM to summarize and identify key points from.


### Patent Analyzer Project Plan

    - [ ] By end of week 4, confirm the availability of the API and perform a simple "Get" HTTPS request and ingest JSON message. If the aforementioned API is not supported then identify alternative sources of Patent Data.
    - [ ] By end of week 5, design a simple webpage for users to interact with the data and host it on a local port.
    - [ ] By end of week 6, finalize the list of interesting analytics/KPIs that would be interesting to inventors and begin developing methods to analyze patent data (i.e. # of patents filed within a given period, # of patents in particular sectors, identify soon-to-expire patents that may be available for licensing, etc.).
    - [ ] By end of week 7, develop the UI/UX and functions which will allow users to query the US Patent Database by different patent attributes such as: filing entity, company, keywords, dates, status, sector, etc.
    - [ ] By end of week 8, develop a prompt and method which takes the patent that are returned and summarizes them using an LLM such as LLAMA, ChatGPT, etc. Validate the responses and try to add functionality to where users can select from a set of preconceived prompts (I.e. summarize the patents, identify competing technology for each returned patent, etc.)
    - [ ] By week 9, finalize the application, perform testing and add nice to have features such as graphics and charts which will allow users to identify trends. 2 examples of charts may be: a time series graph of patent filings within a specified date range. Heatmaps of patent filings by geography (i.e. states, cities, etc.)
    


