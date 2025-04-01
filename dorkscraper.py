# INITIAL PROGRAM THIS BETA VERSION
import argparse
import googleapiclient.discovery
import sys
import json
import os

CONFIG_FILE = 'config.json'

def check_api_credentials():
    if not os.path.exists(CONFIG_FILE):
        print(f"[ERROR] Configuration file {CONFIG_FILE} not found.")
        sys.exit(1)

    with open(CONFIG_FILE, 'r') as config_file:
        config = json.load(config_file)
        api_key = config.get('API_KEY')
        cse_id = config.get('CSE_ID')

        if not api_key or not cse_id:
            print("[ERROR] API_KEY and CSE_ID are not set in the configuration file.")
            sys.exit(1)
        return api_key, cse_id

def init_api_credentials(api_key, cse_id):
    config = {
        "API_KEY": api_key,
        "CSE_ID": cse_id
    }

    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config, config_file)
    
    print("[INFO] API_KEY and CSE_ID have been set successfully.")

def google_search(query, api_key, cse_id, num_results=10):
    service = googleapiclient.discovery.build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, num=num_results).execute()
    return res['items'] if 'items' in res else []

def shell_mode():
    print("[DorkScraper] > Welcome to the interactive shell.")
    while True:
        command = input("[DorkScraper] > ")
        if command.startswith("dork "):
            dork_query = command.split("dork ", 1)[1]
            num_results = int(input("Enter the number of pages to search: "))
            results = google_search(dork_query, API_KEY, CSE_ID, num_results)
            if results:
                for idx, item in enumerate(results, 1):
                    print(f"{idx}. {item['link']}")
            else:
                print("No results found.")
        elif command == "-h" or command == "help":
            print_help()
        elif command == "exit":
            print("Exiting interactive shell.")
            break
        else:
            print("Unrecognized command. Type 'help' for assistance.")

def print_help():
    print("""
    Commands in the shell:
    -d your dorking  : Specify the dork for searching.
    -p number of pages to generate : Specify the number of search result pages.
    -h show help : Display help information.
    exit : Exit the interactive shell.
    """)

def cli_mode(dork_query, num_results):
    print(f"Searching for dork: {dork_query} on page 1...")
    api_key, cse_id = check_api_credentials()
    results = google_search(dork_query, api_key, cse_id, num_results)
    if results:
        for idx, item in enumerate(results, 1):
            print(f"{idx}. {item['link']}")
    else:
        print("No results found.")

def main():
    parser = argparse.ArgumentParser(description="DorkScraper is a powerful tool for Google Dorking and scraping valuable data from Google search results using Custom Search Engine (CSE) and Google APIs. It allows you to perform advanced search queries to discover hidden or sensitive information on the web.")
    parser.add_argument('--dork', help='Your dorking query', type=str)
    parser.add_argument('--page', help='Number of pages to generate', type=int, default=1)
    parser.add_argument('--shell', action='store_true', help='Enter interactive shell')
    parser.add_argument('--init', help='Initialize API_KEY and CSE_ID', nargs=2, metavar=('API_KEY', 'CSE_ID'))

    args = parser.parse_args()

    if args.init:
        api_key, cse_id = args.init
        init_api_credentials(api_key, cse_id)
    else:
        if not os.path.exists(CONFIG_FILE):
            print(f"[ERROR] Configuration file {CONFIG_FILE} not found.")
            sys.exit(1)

        with open(CONFIG_FILE, 'r') as config_file:
            config = json.load(config_file)
            API_KEY = config.get('API_KEY')
            CSE_ID = config.get('CSE_ID')

        if args.shell:
            shell_mode()
        elif args.dork:
            cli_mode(args.dork, args.page)
        else:
            print("Please enter --dork or --shell to proceed.")

if __name__ == "__main__":
    main()