import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
from urllib.parse import urljoin, urlparse

# Function to crawl a website and extract all links
def crawl_website(url, base_url, session, visited=None, count=0):
    if visited is None:
        visited = set()
    if url in visited:
        return visited, count
    parsed_url = urlparse(url)
    if '/img' in parsed_url.path:  # Exclude URLs containing /img in the path
        return visited, count
    visited.add(url)
    count += 1
    print(f"({count}) Crawling: {url}")
    try:
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            parsed_full_url = urlparse(full_url)._replace(query="").geturl()  # Remove query parameters for consistency
            if parsed_full_url not in visited and base_url in parsed_full_url:
                visited, count = crawl_website(parsed_full_url, base_url, session, visited, count)
    except requests.RequestException as e:
        print(f"Failed to crawl {url}: {str(e)}")
    return visited, count

# Function to fetch a URL with a delay to avoid server overload
def fetch(url, user_agent, session, count):
    headers = {'User-Agent': user_agent}
    try:
        response = session.get(url, headers=headers, timeout=10)
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
def warm_cache(urls, user_agents, session, max_workers=10):
    successful_scans = 0
    count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for url in urls:
            for user_agent in user_agents:
                count += 1
                futures.append(executor.submit(fetch, url, user_agent, session, count))
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    successful_scans = sum(results)
    return successful_scans

if __name__ == "__main__":
    base_url = 'https://www.martijnkozijn.nl'
    start_url = 'https://www.martijnkozijn.nl'
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",  # Desktop
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",  # iPhone
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"  # Android
    ]

    session = requests.Session()  # Create a session to handle cookies

    try:
        while True:
            # Crawl the website to get all URLs
            print("Starting crawl...")
            urls, crawl_count = crawl_website(start_url, base_url, session)
            print(f"Found {len(urls)} URLs to warm up")
            
            # Save the URLs to a file for verification
            with open('crawled_urls.txt', 'w') as f:
                for url in urls:
                    f.write(url + '\n')

            # Warm-up cycle
            print("Starting cache warm-up...")
            start_time = time.time()
            successful_scans = warm_cache(urls, user_agents, session, max_workers=10)
            end_time = time.time()
            cycle_time = end_time - start_time
            print(f"Cache warming cycle completed in {cycle_time} seconds")
            print(f"Total successful scans: {successful_scans}")

            # Sleep for a desired period if needed, e.g., 60 seconds
            time.sleep(60)

    except KeyboardInterrupt:
        print("Cache warming interrupted by user")
