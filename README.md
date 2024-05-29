# CacheWarmerMK

CacheWarmerMK is a Python script designed to crawl a website, extract all links, and warm up the cache by fetching those links. This helps ensure that frequently accessed pages are preloaded into the cache, improving website performance.

## Features

- Crawls a website to find all internal links.
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

1. Set the `base_url` and `start_url` to the target website you want to warm up:
    ```python
    base_url = 'https://www.martijnkozijntest.nl'
    start_url = 'https://www.martijnkozijntest.nl'
    ```

2. Run the script:
    ```bash
    python cache_warmer.py
    ```

3. The script will continuously crawl the website, save the found URLs to a file `crawled_urls.txt`, and warm up the cache for these URLs.

## Configuration

- **Maximum Concurrent Workers**: Adjust the number of concurrent connections by changing the `max_workers` parameter in the `warm_cache` function call.
    ```python
    successful_scans = warm_cache(urls, max_workers=10)
    ```

- **Crawl and Warm-up Interval**: Change the sleep duration between cycles by modifying the `time.sleep(30)` line.
    ```python
    time.sleep(30)  # Adjust the sleep duration as needed
    ```

## Script Explanation

- **crawl_website(url, base_url, visited)**: Recursively crawls the given URL, extracts all internal links, and excludes URLs containing `/img`.

- **fetch(url)**: Fetches a URL with a timeout, printing success or failure messages.

- **warm_cache(urls, max_workers)**: Concurrently fetches URLs using a ThreadPoolExecutor to warm up the cache.

- **Main Loop**: Continuously crawls the website, saves URLs to a file, and performs the cache warm-up cycle until interrupted by the user.

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

Feel free to contribute to the project by opening issues or submitting pull requests. For any questions, contact [your email or GitHub profile].
