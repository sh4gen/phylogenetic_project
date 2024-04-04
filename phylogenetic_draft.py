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

total_time = 0
start_time = time.time()
max_time = 600

num_iterations = 0
total_iterations_time = 0
total_request_time = 0
total_parse_time = 0
total_add_time = 0
item_counter = 0

while len(parse_set) != 0 and (time.time() - start_time) < max_time:
    iteration_start_time = time.time() # TIMER
    
    url = parse_set.pop()

    if url in visited_set:
        continue

    try:
        request_start_time = time.time() # TIMER

        response = session.get(url)
        response.raise_for_status()

        request_end_time = time.time() # TIMER
        request_time = request_end_time - request_start_time
        total_request_time += request_time

        parsing_start_time = time.time() # TIMER

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

                    parsing_end_time = time.time() # TIMER
                    parse_time = parsing_end_time - parsing_start_time
                    total_parse_time += parse_time

                    word_count = text.count(' ') + 1
                    full_url = urljoin(url, href)

                    if full_url not in visited_set:
                        add_start_time = time.time() # TIMER
                        new_urls.append(full_url)

                    if text not in names_set and word_count == 2 and text[0].isupper():
                        print(text)
                        names_set.add(text)

                    add_end_time = time.time() # TIMER
                    add_time = add_end_time - add_start_time
                    total_add_time += add_time
 
            parse_set.update(new_urls)        
            item_counter += len(new_urls)
            visited_set.add(url)

    except requests.exceptions.RequestException as e:
        print("Error fetching URL:", url)
        print(e)

    iteration_end_time = time.time() # TIMER
    iteration_time = iteration_end_time - iteration_start_time
    total_iterations_time += iteration_time

    num_iterations += 1

end_time = time.time()
total_time = end_time - start_time

if len(parse_set) == 0:
    print("Scraping completed.")
else:
    print("Maximum time reached. Scraping stopped.")

print("Total Time:", total_time)
print("Total Iterations:", num_iterations)
print("Average Time per Iteration:", total_iterations_time / num_iterations if num_iterations > 0 else 0)
print("Average Time per Request:", total_request_time / num_iterations if num_iterations > 0 else 0)
print("Average Time per Parse:", total_parse_time / item_counter if item_counter > 0 else 0)
print("Average Time per Add:", total_add_time / item_counter if item_counter > 0 else 0)

with open('links.txt', 'a') as f:
    for visited_url in visited_set:
        f.write(visited_url + '\n')

with open('main_data.txt', 'a') as f:
    for name in names_set:
        f.write(name + '\n')
