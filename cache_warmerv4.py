import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
from urllib.parse import urljoin, urlparse

# Function to crawl a website and extract all links
def crawl_website(url, base_url, visited=None):
    if visited is None:
        visited = set()
    if url in visited:
        return visited
    parsed_url = urlparse(url)
    if '/img' in parsed_url.path or parsed_url.query:
        return visited
    visited.add(url)
    print(f"Crawling: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            full_url = urlparse(full_url)._replace(query="").geturl()  # Remove query parameters
            if full_url not in visited and base_url in full_url:
                visited.update(crawl_website(full_url, base_url, visited))
    except requests.RequestException as e:
        print(f"Failed to crawl {url}: {str(e)}")
    return visited

# Function to fetch a URL with a delay to avoid server overload
def fetch(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"Successfully warmed: {url}")
            return True
        else:
            print(f"Failed to warm: {url}, Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Exception for {url}: {str(e)}")
        return False

# Function to warm the cache for the list of URLs with limited concurrent connections
def warm_cache(urls, max_workers=10):  # Increase max_workers to 10
    successful_scans = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(fetch, urls)
    successful_scans = sum(results)
    return successful_scans

if __name__ == "__main__":
    base_url = 'https://www.martijnkozijntest.nl'
    start_url = 'https://www.martijnkozijntest.nl'
    
    try:
        while True:
            # Crawl the website to get all URLs
            print("Starting crawl...")
            urls = crawl_website(start_url, base_url)
            print(f"Found {len(urls)} URLs to warm up")

            # Warm-up cycle
            print("Starting cache warm-up...")
            start_time = time.time()
            successful_scans = warm_cache(urls, max_workers=10)  # Adjust the number of workers to control load
            end_time = time.time()
            cycle_time = end_time - start_time
            print(f"Cache warming cycle completed in {cycle_time} seconds")
            print(f"Total successful scans: {successful_scans}")

            # Sleep for a desired period if needed, e.g., 60 seconds
            time.sleep(30)  # Reduce sleep time to 30 seconds

    except KeyboardInterrupt:
        print("Cache warming interrupted by user")
