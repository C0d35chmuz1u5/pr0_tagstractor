import sys
import requests
import os
import json
from tqdm import tqdm
import ctypes
from datetime import datetime
import time

# Add auth to pr0 via dependency

def print_explanation_and_exit():
    print("Explanation: This script extracts and ranks tags from pr0gramm.com API.")
    print("Usage: python pr0_tagstractor.py <start_post_id> <end_post_id>")
    sys.exit()

if len(sys.argv) != 3:
    print_explanation_and_exit()

start_number = int(sys.argv[1])
end_number = int(sys.argv[2])

if start_number >= end_number:
    print("Error: The start_post_id must be lower than the end_post_id.")
    print_explanation_and_exit()

ctypes.windll.kernel32.SetConsoleTitleW("pr0 TAGstractor")

base_url = "https://pr0gramm.com/api/items/info?itemId="
url_array = []

os.system('cls')

for i in tqdm(range(start_number, end_number + 1), desc="Generating URLs"):
    url_array.append(base_url + str(i))

os.system('cls')    

tag_counters = {}

error_urls = []

result_folder = "pr0_tag_result"
if not os.path.exists(result_folder):
    os.makedirs(result_folder)

for url in tqdm(url_array, desc="Processing URLs"):
    try:
        response = requests.get(url)
        data = response.json()

        if not data or data == "" or response.status_code != 200:
            raise ValueError(str(response.status_code))

        for tag_info in data.get("tags", []):
            tag = tag_info.get("tag")
            if tag:
                tag_counters[tag] = tag_counters.get(tag, 0) + 1

    except ValueError as ve:
        error_urls.append((url, str(ve)))
    except requests.exceptions.RequestException as e:
        status_code_message = f"Error {e.response.status_code}" if hasattr(e, 'response') and e.response is not None and e.response.status_code is not None else "N/A"
        error_message = f"{url} ::: {status_code_message}"
        error_urls.append(error_message)

if error_urls:
    current_timestamp = datetime.now()
    formatted_string = current_timestamp.strftime("%Y-%m-%d %H-%M-%S.%f")
    with open(os.path.join(result_folder, f'error-{formatted_string.replace(":", "_")}.txt'), 'w', encoding='utf-8') as error_file:
        error_file.write("Fetching Errors on:\n")
        for error_tuple in error_urls:
            error_url, status_code = error_tuple
            error_file.write(f"{error_url} - Status Code: {status_code}\n")


tag_counters_list = list(tag_counters.items())

os.system('cls')

sorted_tags = []
with tqdm(total=len(tag_counters_list), desc="Sorting Tags") as pbar_sorting:
    for tag, count in sorted(tag_counters_list, key=lambda x: x[1], reverse=True):
        sorted_tags.append((tag, count))
        pbar_sorting.update(1)

os.system('cls')

current_timestamp = datetime.now()
formatted_string = current_timestamp.strftime("%Y-%m-%d %H-%M-%S.%f")

with open(os.path.join(result_folder, f'most_used_tags_descending-{formatted_string.replace(":", "_")}.txt'), 'w', encoding='utf-8') as file:
    for tag, count in sorted_tags:
        file.write(f"{tag}\n")

with open(os.path.join(result_folder, f'ranking_tags-{formatted_string.replace(":", "_")}.txt'), 'w', encoding='utf-8') as file:
    file.write(f"USED:::TAG\n")
    for tag, count in sorted_tags:
        file.write(f"{count}::::::{tag}\n")

os.system('cls')      
print("Total tags extracted (descending based on times used): {}".format(len(tag_counters_list)))