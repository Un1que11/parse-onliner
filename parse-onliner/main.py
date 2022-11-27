import requests
import json


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0'
}


def get_page(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open('index.html', 'w') as f:
        f.write(response.text)


def get_json(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open('result.json', 'w') as f:
        json.dump(response.json(), f, indent=4, ensure_ascii=False)


def collect_data():
    s = requests.Session()
    response = s.get(url='https://catalog.onliner.by/sdapi/catalog.api/search/notebook?in_stock=1&page=2', headers=headers)

    data = response.json()
    pages_count = data.get('page').get('last')

    result_data = []
    for page in range(1, pages_count + 1):
        url = f'https://catalog.onliner.by/sdapi/catalog.api/search/notebook?in_stock=1&page={page}'
        r = s.get(url=url, headers=headers)

        data = r.json()
        products = data.get('products')

        for product in products:
            discount_percent = product.get('sale').get('discount')

            if discount_percent != 0:
                result_data.append(
                    {
                        'title': product.get('full_name'),
                        'link': product.get('html_url'),
                        'price_base': f'{product.get("sale").get("min_prices_median").get("amount")} BYN',
                        'price_sale': f'{product.get("prices").get("price_min").get("amount")} BYN',
                        'discount_percent': discount_percent
                    }
                )
        print(f'{page}/{pages_count}')
    with open('result_data.json', 'w') as f:
        json.dump(result_data, f, indent=4, ensure_ascii=False)


def main():
    # get_page(url='https://catalog.onliner.by/notebook')
    # get_json(url='https://catalog.onliner.by/sdapi/catalog.api/search/notebook?in_stock=1&page=2')
    collect_data()


if __name__ == '__main__':
    main()
