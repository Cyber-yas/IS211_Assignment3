import argparse 
import urllib.request
import csv 
import io 
import re 

def downloadData(url): 
    """
    Reads data from a URL and returns the data as a string.

    :param url: URL to download
    :return: the content of the URL as a string
    """
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')


def processData(file_content):
    """
    Processes the CSV file content to gather stats on images and browsers.

    :param file_content: CSV file content as a string
    """
    csv_data = csv.reader(io.StringIO(file_content))
    
    image_counter = 0
    total_hits = 0

    # Browser counters:
    chrome_counter = 0
    safari_counter = 0
    msie_counter = 0
    firefox_counter = 0

    # Regular expression for image file extensions:
    image_pattern = re.compile(r'\.(jpg|gif|png)$', re.IGNORECASE)

    for row in csv_data:
        total_hits += 1
        
        path_to_file = row[0]  # Path to file
        browser = row[2]  # Browser (User-Agent)
        
        
        if image_pattern.search(path_to_file):
            image_counter += 1

        
        if "Chrome" in browser and "Safari" not in browser:
            chrome_counter += 1
        elif "Firefox" in browser:
            firefox_counter += 1
        elif "Safari" in browser and "Chrome" not in browser:
            safari_counter += 1
        elif "MSIE" in browser:
            msie_counter += 1

    # Calculating the percentage of image requests
    percent_images = (image_counter / total_hits) * 100
    print(f"Image requests account for {percent_images:.2f}% of all requests.")
    
    # Browser statistics
    browser_stats = {
        "Chrome": chrome_counter,
        "Firefox": firefox_counter,
        "Safari": safari_counter,
        "MSIE": msie_counter
    }
    
    # The browser with the maximum hits
    most_popular_browser = max(browser_stats, key=browser_stats.get)
    print(f"The most popular browser is {most_popular_browser} with {browser_stats[most_popular_browser]} hits.")


def main(url):
    """
    Main function to download data and process it.

    :param url: URL to download the data from
    """
    print(f"Running main with URL = {url}...")
    url_data = downloadData(url)
    processData(url_data) 


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the data file", type=str, required=True)
    args = parser.parse_args()  # Parse arguments
    main(args.url)  # Pass URL to the main function


