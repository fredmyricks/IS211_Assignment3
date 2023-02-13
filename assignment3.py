import argparse
import csv
import re
import requests


def download_log_file(url):
    response = requests.get(url)
    return response.text

def process_file(file_content):
    reader = csv.reader(file_content.splitlines())
    return [row for row in reader]

def search_for_image_hits(file_rows):
    image_hits = 0
    for row in file_rows:
        if re.search(r'.*\.(jpg|gif|png)', row[0]):
            image_hits += 1
    total_hits = len(file_rows)
    return (image_hits, (image_hits / total_hits) * 100)

def find_most_popular_browser(file_rows):
    browser_counts = {'Firefox': 0, 'Chrome': 0, 'Internet Explorer': 0, 'Safari': 0}
    for row in file_rows:
        user_agent = row[2]
        if re.search(r'Firefox', user_agent):
            browser_counts['Firefox'] += 1
        elif re.search(r'Chrome', user_agent):
            browser_counts['Chrome'] += 1
        elif re.search(r'Internet Explorer', user_agent):
            browser_counts['Internet Explorer'] += 1
        elif re.search(r'Safari', user_agent):
            browser_counts['Safari'] += 1
    return max(browser_counts, key=browser_counts.get)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='The URL of the log file')
    args = parser.parse_args()

    file_content = download_log_file(args.url)
    file_rows = process_file(file_content)
    image_hits, image_hits_percentage = search_for_image_hits(file_rows)
    most_popular_browser = find_most_popular_browser(file_rows)
    # hour_counts = get_hits_per_hour(file_rows)

    print(f'Image requests account for {image_hits_percentage:.1f}% of all requests')
    print(f'The most popular browser is {most_popular_browser}')


