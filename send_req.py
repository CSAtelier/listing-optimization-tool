import requests

headers = {
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

x = requests.get('https://sellercentral.amazon.com/rcpublic/productmatch?searchKey=B08B2GFJ1C&countryCode=CA&locale=en-US', headers=headers)

print(x.text)