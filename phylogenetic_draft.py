from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import time

parse_set = {
    'https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Undef&id=2759&lvl=3&keep=1&srchmode=1&unlock'
}

visited_set = set()
names_set = set()

session = requests.Session()


start_time = time.time()
max_time = 600

num_iterations = 0

timer = {
    "parse": [0.0, 0.0],
    "request": [0.0, 0.0],
    "total": [0.0, 0.0],
}

times = {
    "parse": 0.0,
    "request": 0.0,
    "total": 0.0,
}

while len(parse_set) != 0 and (time.time() - start_time) < max_time:
    
    timer["total"][0] = time.time()
    
    url = parse_set.pop()

    if url in visited_set:
        continue

    try:
        timer["request"][0] = time.time()

        response = session.get(url)
        response.raise_for_status()

        timer["request"][1] = time.time()

        timer["parse"][0] = time.time()

        soup = BeautifulSoup(response.content, "html.parser")
        ul_tag = soup.find('ul', attrs={'compact': ''})

        if ul_tag is not None:

            circle_items = ul_tag.find_all('li', attrs={'type': 'circle'})
            disc_items = ul_tag.find_all('li', attrs={'type': 'disc'})
            square_items = ul_tag.find_all('li', attrs={'type': 'square'})
            all_items = circle_items + disc_items + square_items

            new_urls = []
            for item in all_items:
                a_tag = item.find('a')
                if a_tag:
                    text = a_tag.text.strip()
                    href = a_tag.get('href')

                    word_count = text.count(' ') + 1
                    full_url = urljoin(url, href)

                    if full_url not in visited_set:
                        new_urls.append(full_url)

                    if text not in names_set and word_count == 2 and text[0].isupper():
                        names_set.add(text)
 
            parse_set.update(new_urls)        
            visited_set.add(url)

        timer["parse"][1] = time.time()

    except requests.exceptions.RequestException as e:
        print("Error fetching URL:", url)
        print(e)

    timer["total"][1] = time.time()
    num_iterations += 1

    for key in timer:
        times[key] += timer[key][1] - timer[key][0]

    if num_iterations % 10 == 0:
        print("Total Time:", times["total"])
        print("Total Iterations:", num_iterations)
        print("Average Time per Iteration:", times["total"] / num_iterations)
        print("Average Request Time:", times["request"] / num_iterations)
        print("Average Parse Time:", times["parse"] / num_iterations)
        print("Number of URLs in parse_set:", len(parse_set))
        print("Number of URLs in visited_set:", len(visited_set))
        print("Number of names:", len(names_set))
        print()

if len(parse_set) == 0:
    print("Scraping completed.")
else:
    print("Maximum time reached. Scraping stopped.")

with open('links.txt', 'a') as f:
    for visited_url in visited_set:
        f.write(visited_url + '\n')

with open('main_data.txt', 'a') as f:
    for name in names_set:
        f.write(name + '\n')
