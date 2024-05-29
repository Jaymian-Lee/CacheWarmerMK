import requests
import concurrent.futures
import time
import xml.etree.ElementTree as ET

# Function to download and parse the XML file from the URL and extract URLs
def parse_sitemap(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    root = ET.fromstring(response.content)
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
            return True
        else:
            print(f"Failed to warm: {url}, Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Exception for {url}: {str(e)}")
        return False

# Function to warm the cache for the list of URLs
def warm_cache(urls, max_workers=5):
    successful_scans = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(fetch, urls)
    successful_scans = sum(results)
    return successful_scans

# Function to check the cache status
def check_cache_status(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            cache_status = response.json()
            return cache_status.get('cache_count', 0)  # Assuming the response contains 'cache_count'
        else:
            print(f"Failed to check cache status: {url}, Status code: {response.status_code}")
            return 0
    except requests.RequestException as e:
        print(f"Exception for {url}: {str(e)}")
        return 0

if __name__ == "__main__":
    # URL of the sitemap
    sitemap_url = 'https://www.martijnkozijntest.nl/1_nl_0_sitemap.xml'
    urls = parse_sitemap(sitemap_url)
    cache_status_url = 'https://example.com/cache-status'  # Replace with your actual cache status endpoint
    
    try:
        # Initial cache status check
        initial_cache_count = check_cache_status(cache_status_url)
        print(f"Initial cache count: {initial_cache_count}")
        
        # First warm-up cycle (cold cache)
        start_time = time.time()
        successful_scans = warm_cache(urls)
        end_time = time.time()
        first_cycle_time = end_time - start_time
        print(f"First cache warming cycle completed in {first_cycle_time} seconds")
        print(f"Total successful scans: {successful_scans}")

        # Cache status after first warm-up cycle
        cache_count_after_first_cycle = check_cache_status(cache_status_url)
        print(f"Cache count after first cycle: {cache_count_after_first_cycle}")

        # Second warm-up cycle (warm cache)
        start_time = time.time()
        successful_scans = warm_cache(urls)
        end_time = time.time()
        second_cycle_time = end_time - start_time
        print(f"Second cache warming cycle completed in {second_cycle_time} seconds")
        print(f"Total successful scans: {successful_scans}")

        # Cache status after second warm-up cycle
        cache_count_after_second_cycle = check_cache_status(cache_status_url)
        print(f"Cache count after second cycle: {cache_count_after_second_cycle}")

        # Compare times
        print(f"Time difference between first and second cycle: {first_cycle_time - second_cycle_time} seconds")

    except KeyboardInterrupt:
        print("Cache warming interrupted by user")
