import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import os
import threading

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
}

lock = threading.Lock()
results = []

def load_payloads(path):
    if not os.path.isfile(path):
        print(f"[!] File not found: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def extract_links(url):
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        links = set()
        for link in soup.find_all("a", href=True):
            href = link['href']
            full_url = urljoin(url, href)
            if urlparse(full_url).netloc == urlparse(url).netloc:
                links.add(full_url)
        return list(links)
    except Exception as e:
        print(f"[!] Error fetching links: {e}")
        return []

def test_payload(url, param, payload):
    try:
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        params = parse_qs(parsed.query)
        test_params = {k: (payload if k == param else v[0]) for k, v in params.items()}
        test_url = base + "?" + "&".join([f"{k}={v}" for k, v in test_params.items()])
        res = requests.get(test_url, headers=headers, timeout=10)

        if payload in res.text:
            with lock:
                result = f"[!!] Vulnerable: {test_url} | Param: {param} | Payload: {payload}"
                print(result)
                results.append(result)
            return True
    except Exception as e:
        with lock:
            print(f"[!] Error testing {url} param {param}: {e}")
    return False

def is_vulnerable(url, payloads):
    parsed = urlparse(url)
    if not parsed.query:
        return
    params = list(parse_qs(parsed.query).keys())

    threads = []
    for param in params:
        for payload in payloads:
            t = threading.Thread(target=test_payload, args=(url, param, payload))
            t.start()
            threads.append(t)
    for t in threads:
        t.join()

def load_links_manually():
    print("\n[!] No links found automatically.")
    choice = input("Do you want to (1) enter a link manually or (2) load from file? [1/2]: ").strip()
    links = []

    if choice == "1":
        manual = input("Enter link: ").strip()
        links.append(manual)
    elif choice == "2":
        path = input("Enter path to links file: ").strip()
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                links = [line.strip() for line in f if line.strip()]
        else:
            print("[!] File not found.")
    else:
        print("[!] Invalid choice.")
    return links

def main():
    target = input("Enter target URL (e.g. https://example.com): ").strip()
    wordlist_path = input("Enter path to payload wordlist: ").strip()
    payloads = load_payloads(wordlist_path)
    if not payloads:
        return

    print("[*] Collecting links...")
    links = extract_links(target)
    print(f"[+] Found {len(links)} links.")

    if not links:
        links = load_links_manually()
        if not links:
            print("[!] No links to test. Exiting.")
            return

    for link in links:
        print(f"\n[•] Testing: {link}")
        is_vulnerable(link, payloads)

    if results:
        with open("xss_results.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(results))
        print(f"\n[✔] Results saved to xss_results.txt")
    else:
        print("\n[-] No XSS vulnerabilities found.")

if __name__ == "__main__":
    main()
