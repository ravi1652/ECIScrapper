import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"

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

            extracted_data.append([party_name, won_seats, leading, total])

    headers = ["Party Name", "Won Seats", "Leading", "Total"]
    print(tabulate(extracted_data, headers=headers, tablefmt="pretty"))

except Exception as e:
    print(f"Error occurred: {str(e)}")
