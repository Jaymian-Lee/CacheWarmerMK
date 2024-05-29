import requests
import concurrent.futures
import time
import xml.etree.ElementTree as ET

# Function to parse the XML file and extract URLs
def parse_sitemap(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    urls = []
    for url in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
        urls.append(loc)
    return urls

# Function to fetch a URL
def fetch(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"Successfully warmed: {url}")
        else:
            print(f"Failed to warm: {url}, Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Exception for {url}: {str(e)}")

# Function to warm the cache for the list of URLs
def warm_cache(urls, max_workers=5):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(fetch, urls)

if __name__ == "__main__":
    # Parse the XML file to get URLs
    sitemap_path = 'martijnkozijntest.xml'
    urls = parse_sitemap(sitemap_path)
    
    try:
        while True:
            start_time = time.time()
            warm_cache(urls)
            end_time = time.time()
            print(f"Cache warming cycle completed in {end_time - start_time} seconds")
            # Sleep for a desired period if needed, e.g., 60 seconds
            time.sleep(60)
    except KeyboardInterrupt:
        print("Cache warming interrupted by user")
