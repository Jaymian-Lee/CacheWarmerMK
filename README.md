Here's the updated README to reflect the new structure with two separate scripts for crawling URLs and processing sitemaps:

---

# CacheWarmerMK

CacheWarmerMK is a Python script designed to improve website performance by preloading frequently accessed pages into the cache. It includes two versions:
- One that crawls a website to extract all links.
- One that reads a sitemap to extract links.

## Features

- Crawls a website to find all internal links (URL-based crawler).
- Reads a sitemap to extract all listed URLs (Sitemap-based crawler).
- Excludes URLs containing `/img` to avoid fetching image resources.
- Concurrently fetches URLs to warm up the cache.
- Periodically repeats the cache warming process.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/CacheWarmerMK.git
    cd CacheWarmerMK
    ```

2. Install the required Python packages:
    ```bash
    pip install requests beautifulsoup4
    ```

## Usage

### URL-based Crawler

1. Navigate to the `urls` directory:
    ```bash
    cd urls
    ```

2. Set the `base_url` and `start_url` to the target website you want to warm up:
    ```python
    base_url = 'https://www.martijnkozijntest.nl'
    start_url = 'https://www.martijnkozijntest.nl'
    ```

3. Run the script:
    ```bash
    python cache_warmer.py
    ```

4. The script will continuously crawl the website, save the found URLs to a file `crawled_urls.txt`, and warm up the cache for these URLs.

### Sitemap-based Crawler

1. Navigate to the `sitemap` directory:
    ```bash
    cd sitemap
    ```

2. Set the `sitemap_url` to the target sitemap you want to warm up:
    ```python
    sitemap_url = 'https://www.martijnkozijn.nl/1_nl_0_sitemap.xml'
    ```

3. Run the script:
    ```bash
    python cache_warmer.py
    ```

4. The script will fetch the sitemap, save the found URLs to a file `sitemap_urls.txt`, and warm up the cache for these URLs.

## Configuration

- **Maximum Concurrent Workers**: Adjust the number of concurrent connections by changing the `max_workers` parameter in the `warm_cache` function call.
    ```python
    successful_scans = warm_cache(urls, user_agents, max_workers=10)
    ```

- **Crawl and Warm-up Interval**: Change the sleep duration between cycles by modifying the `time.sleep(30)` line.
    ```python
    time.sleep(30)  # Adjust the sleep duration as needed
    ```

## Script Explanation

### URL-based Crawler

- **crawl_website(url, base_url, visited, count)**: Recursively crawls the given URL, extracts all internal links, and excludes URLs containing `/img`.

- **fetch(url, user_agent, count)**: Fetches a URL with a timeout, printing success or failure messages.

- **warm_cache(urls, user_agents, max_workers)**: Concurrently fetches URLs using a ThreadPoolExecutor to warm up the cache.

- **Main Loop**: Continuously crawls the website, saves URLs to a file, and performs the cache warm-up cycle until interrupted by the user.

### Sitemap-based Crawler

- **fetch_sitemap(sitemap_url)**: Fetches and parses the sitemap XML.

- **parse_sitemap(content)**: Extracts URLs from the sitemap XML.

- **fetch(url, user_agent, count)**: Fetches a URL with a timeout, printing success or failure messages.

- **warm_cache(urls, user_agents, max_workers)**: Concurrently fetches URLs using a ThreadPoolExecutor to warm up the cache.

- **Main Loop**: Continuously fetches URLs from the sitemap, saves URLs to a file, and performs the cache warm-up cycle until interrupted by the user.

## Example Output

```
Starting crawl...
Crawling: https://www.martijnkozijntest.nl
Found 15 URLs to warm up
Starting cache warm-up...
Successfully warmed: https://www.martijnkozijntest.nl
Cache warming cycle completed in 12.3 seconds
Total successful scans: 15
```

## Acknowledgements

- [Requests Library](https://docs.python-requests.org/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)

---

Feel free to contribute to the project by opening issues or submitting pull requests. For any questions, don't hesitate to contact me!

---

This README now reflects the changes and includes instructions for both the URL-based crawler and the Sitemap-based crawler.
