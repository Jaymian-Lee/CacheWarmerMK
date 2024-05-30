import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import xml.etree.ElementTree as ET

# Function to fetch and parse the sitemap
def fetch_sitemap(sitemap_url):
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        sitemap_content = response.content
        urls = parse_sitemap(sitemap_content)
        return urls
    except requests.RequestException as e:
        print(f"Failed to fetch sitemap: {str(e)}")
        return []

# Function to parse the sitemap XML and extract URLs
def parse_sitemap(content):
    urls = []
    try:
        tree = ET.fromstring(content)
        for elem in tree:
            for subelem in elem:
                if 'loc' in subelem.tag:
                    urls.append(subelem.text)
    except ET.ParseError as e:
        print(f"Failed to parse sitemap: {str(e)}")
    return urls

# Function to fetch a URL with a delay to avoid server overload
def fetch(url, user_agent, count):
    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"({count}) Successfully warmed: {url} with user agent: {user_agent}")
            return True
        else:
            print(f"({count}) Failed to warm: {url}, Status code: {response.status_code}, user agent: {user_agent}")
            return False
    except requests.RequestException as e:
        print(f"({count}) Exception for {url} with user agent {user_agent}: {str(e)}")
        return False

# Function to warm the cache for the list of URLs with limited concurrent connections
def warm_cache(urls, user_agents, max_workers=10):
    successful_scans = 0
    count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for url in urls:
            for user_agent in user_agents:
                count += 1
                futures.append(executor.submit(fetch, url, user_agent, count))
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    successful_scans = sum(results)
    return successful_scans

if __name__ == "__main__":
    sitemap_url = 'https://www.martijnkozijn.nl/1_nl_0_sitemap.xml'
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",  # Desktop
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",  # iPhone
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"  # Android
    ]

    try:
        while True:
            # Fetch and parse the sitemap to get all URLs
            print("Fetching sitemap...")
            urls = fetch_sitemap(sitemap_url)
            print(f"Found {len(urls)} URLs to warm up")
            
            # Save the URLs to a file for verification
            with open('sitemap_urls.txt', 'w') as f:
                for url in urls:
                    f.write(url + '\n')

            # Warm-up cycle
            print("Starting cache warm-up...")
            start_time = time.time()
            successful_scans = warm_cache(urls, user_agents, max_workers=10)
            end_time = time.time()
            cycle_time = end_time - start_time
            print(f"Cache warming cycle completed in {cycle_time} seconds")
            print(f"Total successful scans: {successful_scans}")

            # Sleep for a desired period if needed, e.g., 60 seconds
            time.sleep(30)

    except KeyboardInterrupt:
        print("Cache warming interrupted by user")
