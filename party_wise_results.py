import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

def extract_party_results(url):
    try:
        response = requests.get(url)
        html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')

        container_div = soup.find('div', class_='cardTble')

        if container_div is None:
            raise ValueError(f"Container div with class 'cardTble' not found on {url}")

        rows = container_div.find_all('tr', class_='tr')

        extracted_data = []

        for row in rows:
            columns = row.find_all('td')

            if len(columns) >= 4:
                party_name = columns[0].text.strip()
                won_seats = columns[1].text.strip()
                leading = columns[2].text.strip()
                total = columns[3].text.strip()

                link = columns[1].find('a')['href'].split('-')[-1].split('.')[0] if columns[1].find('a') else None

                extracted_data.append([party_name, won_seats, leading, total, link])

        headers = ["Party Name", "Won Seats", "Leading", "Total", "Link (ID)"]

        indexed_data = [[i + 1] + row for i, row in enumerate(extracted_data)]
        indexed_headers = ["Index"] + headers

        print(tabulate(indexed_data, headers=indexed_headers, tablefmt="pretty"))

        return extracted_data

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None
