import os
import sqlite3
import shutil
from urllib.parse import urlparse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

DST = "./History_copy"


HISTORY_PATH = DST

def get_chrome_history_path():
    return os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        r"Google\Chrome\User Data\Default\History"
    )


def chrome_time_to_datetime(chrome_time):
    # Chrome stores time in microseconds since 1601-01-01
    epoch_start = datetime(1601, 1, 1)
    return epoch_start + timedelta(microseconds=chrome_time)

def extract_raw_visits():
    conn = sqlite3.connect(HISTORY_PATH)
    
    cursor = conn.cursor()

    query = """
    SELECT urls.url, urls.title, visits.visit_time
    FROM visits
    JOIN urls ON visits.url = urls.id
    ORDER BY visits.visit_time DESC
    LIMIT 10000;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    visits = []
    for url, title, visit_time in rows:
        dt = chrome_time_to_datetime(visit_time)
        visits.append((dt, url, title))

    return visits

def domain_from_url(url):
    try:
        return urlparse(url).netloc
    except:
        return None

def summarize(visits):
    domain_counts = {}

    for dt, url, title in visits:
        domain = domain_from_url(url)
        if not domain:
            continue
        domain_counts[domain] = domain_counts.get(domain, 0) + 1

    # print top 20
    print("\nTop Domains:")
    for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"{domain:40} {count}")

    return domain_counts


def plot_top_domains(domain_counts, top_n=20):
    top = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    domains = [d for d, _ in top]
    counts = [c for _, c in top]

    plt.figure(figsize=(12, 6))
    plt.barh(domains, counts)
    plt.gca().invert_yaxis()
    plt.title("Top Domains (Visit Count)")
    plt.xlabel("Visits")
    plt.tight_layout()
    plt.show()


def plot_long_tail(domain_counts):
    sorted_counts = sorted(domain_counts.values(), reverse=True)

    plt.figure(figsize=(10, 5))
    plt.plot(sorted_counts)
    plt.yscale("log")
    plt.title("Long Tail of Domain Visits (Log Scale)")
    plt.xlabel("Domain Rank")
    plt.ylabel("Visit Count (log)")
    plt.tight_layout()
    plt.show()


def main():
    print("Extracting Chrome history...")
    visits = extract_raw_visits()
    domain_counts = summarize(visits)

    plot_top_domains(domain_counts)
    plot_long_tail(domain_counts)


SRC = get_chrome_history_path()
# Always copy fresh
shutil.copy2(SRC, DST)

if __name__ == "__main__":
    main()
