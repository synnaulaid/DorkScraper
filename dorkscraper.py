import argparse
import googleapiclient.discovery
import sys
import json
import os
import time
import threading
import colorama
from termcolor import colored

colorama.init(autoreset=True)

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

def loading_animation():
    loading_symbols = ['|', '/', '-', '\\']
    for _ in range(10):  # Simple 10-step loading animation
        for symbol in loading_symbols:
            print(f"{colored('[INFO]', 'blue')} {colored('Searching', 'green')} {symbol}", end='\r')
            time.sleep(0.1)

def shell_mode():
    print(colored("[DorkScraper]", "blue") + colored(" > ", "white") + "Welcome to the interactive shell.")
    while True:
        command = input(colored("[DorkScraper]", "blue") + colored(" > ", "white")).strip()
        
        if command in ["exit", "quit"]:
            print("Exiting interactive shell.")
            break
        elif command in ["-h", "help"]:
            print("""
    Commands in the shell:
    -d your_dork -p number_of_pages : Perform a dorking search.
    -h show help : Display help information.
    exit : Exit the interactive shell.
            """)
        elif command.startswith("-d "):
            # Parsing input command
            parts = command.split(" -p ")
            dork_query = parts[0][3:].strip()  # Remove '-d ' from the string
            
            num_pages = 1  # Default pages
            if len(parts) > 1:
                try:
                    num_pages = int(parts[1].strip())
                except ValueError:
                    print(colored("[ERROR]", 'red') + colored(" Invalid number of pages. Using default (1).", 'white')) 


            # Pastikan API_KEY dan CSE_ID sudah diatur
            api_key, cse_id = check_api_credentials()
            
            print(colored("[INFO]", 'blue') + colored(f" Searching for dork: {dork_query} on {num_pages} pages...", 'green'))

            # Mulai animasi loading di thread terpisah
            loading_thread = threading.Thread(target=loading_animation)
            loading_thread.start()

            results = google_search(dork_query, api_key, cse_id, num_pages)

            loading_thread.join()  # Tunggu sampai animasi loading selesai

            if results:
                print(colored("[INFO]", 'blue') + colored(f" Found {len(results)} result(s):", 'green'))
                for idx, item in enumerate(results, 1):
                    print(f"{idx}. {item['link']}")
            else:
                print(colored("[INFO]", 'blue') + colored(f"No results found.", 'red'))
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
    print(colored("[INFO]", 'blue') + colored(f" Searching for dork: {dork_query} on pages...", 'green'))
    api_key, cse_id = check_api_credentials()

    # Start animasi di background
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()

    results = google_search(dork_query, api_key, cse_id, num_results)

    loading_thread.join()  # Tunggu animasi selesai sebelum menampilkan hasil

    if results:
        print(colored("[INFO]", 'blue') + colored(f" Found {len(results)} result(s):", 'green'))
        for idx, item in enumerate(results, 1):
            print(f"{idx}. {item['link']}")
    else:
        print(colored("[INFO]", 'blue') + colored(f"No results found.", 'red'))

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
