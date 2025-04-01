# DorkScraper

DorkScraper is a powerful tool for Google Dorking and scraping valuable data from Google search results using Custom Search Engine (CSE) and Google APIs. It allows you to perform advanced search queries to discover hidden or sensitive information on the web.

## Features

- **Google Dorking**: Utilizes Google Dork queries to perform precise searches for finding specific information.
- **Data Scraping**: Extracts and collects data from Google search results pages.
- **Custom Search Engine (CSE)**: Integrates with Google's CSE to refine search results and enhance the scraping process.
- **Flexible and Scalable**: Easily configurable for different search queries and customizable scraping settings.

## Requirements

Before running DorkScraper, ensure you have the following installed:

- Python 3.x
- Google Custom Search JSON API key
- Python Libraries:
  - requests
  - google-api-python-client

## Installations

```
❯ git clone https://github.com/synnaulaid/DorkScraper.git
❯ cd DorkScraper
❯ pip install -r req.txt
❯ python3 dorkscraper.py
[ERROR] Configuration file config.json not found.
# set your API & CSE see coammnad:
❯ python3 dorkscraper.py --help
usage: dorkscraper.py [-h] [--dork DORK] [--page PAGE] [--shell]
                      [--init API_KEY CSE_ID]

DorkScraper is a powerful tool for Google Dorking and scraping valuable data
from Google search results using Custom Search Engine (CSE) and Google APIs.
It allows you to perform advanced search queries to discover hidden or
sensitive information on the web.

options:
  -h, --help            show this help message and exit
  --dork DORK           Your dorking query
  --page PAGE           Number of pages to generate
  --shell               Enter interactive shell
  --init API_KEY CSE_ID
                        Initialize API_KEY and CSE_ID

```