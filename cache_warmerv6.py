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
    if '/img' in parsed_url.path:  # Exclude URLs containing /img in the path
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
            parsed_full_url = urlparse(full_url)._replace(query="").geturl()  # Remove query parameters for consistency
            if parsed_full_url not in visited and base_url in parsed_full_url:
                visited.update(crawl_website(parsed_full_url, base_url, visited))
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
def warm_cache(urls, max_workers=10):
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
            
            # Save the URLs to a file for verification
            with open('crawled_urls.txt', 'w') as f:
                for url in urls:
                    f.write(url + '\n')

            # Warm-up cycle
            print("Starting cache warm-up...")
            start_time = time.time()
            successful_scans = warm_cache(urls, max_workers=10)
            end_time = time.time()
            cycle_time = end_time - start_time
            print(f"Cache warming cycle completed in {cycle_time} seconds")
            print(f"Total successful scans: {successful_scans}")

            # Sleep for a desired period if needed, e.g., 60 seconds
            time.sleep(30)

    except KeyboardInterrupt:
        print("Cache warming interrupted by user")
