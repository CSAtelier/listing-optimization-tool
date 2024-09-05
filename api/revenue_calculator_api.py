import requests


default_headers = {
    'Host' : 'sellercentral.amazon.com',
    'Pragma' : "no-cache",
    'accept' : 'application/json',
    'accept-encoding' : 'gzip, deflate, br, zstd',
    'referer': 'https://sellercentral.amazon.com/hz/fba/profitabilitycalculator/index?lang=en',
    'sec-ch-ua': '"Chromium";v="128", "Not:A-Brand";v="24", "Brave";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

def get_detail(asin: str, country_code: str):

    url = f"https://sellercentral.amazon.com/rcpublic/productmatch?searchKey={asin}&countryCode={country_code}&locale=en-US"
    response = requests.get(url, headers= default_headers)
    return response




if __name__ == "__main__":

    from pprint import pprint as pp
    
    country_code = "CA"
    asin = "B08B2GFJ1C"

    detail = get_detail(asin, country_code)

    pp(detail.text)