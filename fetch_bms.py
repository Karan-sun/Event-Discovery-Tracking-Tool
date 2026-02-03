import requests

url = "https://in.bookmyshow.com/explore/events-mumbai"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Referer': 'https://in.bookmyshow.com/'
}

try:
    s = requests.Session()
    response = s.get(url, headers=headers)
    response.raise_for_status()
    print(f"Status Code: {response.status_code}")
    with open("bms_sample.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Successfully downloaded bms_sample.html")
except Exception as e:
    print(f"Error fetching URL: {e}")
