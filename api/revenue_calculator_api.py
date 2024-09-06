from typing import List
from pprint import pprint as pp
import requests
import json


default_headers ={
  'Pragma': 'no-cache',
  'Accept': 'application/json',
  'accept-encoding': 'gzip, deflate, br, zstd',
  'accept-language': "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
  'referer': 'https://sellercentral.amazon.com/hz/fba/profitabilitycalculator/index?lang=en_US',
  'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'sec-gpc': '1',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
  'Cookie': 'session-id=135-0152276-8067861; i18n-prefs=USD; sp-cdn="L5Z9:TR"; ubid-main=131-7265863-6174363; session-id-eu=260-3642913-2766466; ubid-acbuk=262-3304095-9797960; __Host_mlang=en_US; ld=NSGoogle; session-token=Tk5BbC+fmcM3j87jtZ4BahXq/PWsU9Dbu0skYQJWLawJ0BCz9RKwHAWXW1LsBzYq8HEN8/cuLaCYqjFO5wpnWfU+PNOzeYAdC2p8i87sxePblqB61YIV9bph1vrbbOLXZC1Hua6cxBJoiDkTm2cOCsBr3RVnBPKN69opaBnBVQk4FXLDENYkUm0dbS4oGlT8eWh1CKfKviia7zeQJMhasQgkkm6tCK2o90Tb1cjVeEiMC9sQKJ65zM8tNEY6Q4ufTJWjPMR4oVbvqUNOlWmim0Wp5N7XRfLsn/iuBKTuxqRe8pcSs1fvN7Wiog/kU/e5aABpskMRs9NPc5dyrXwBc7z57SSq4+7J; session-id-time=2356283880l; s_sess=%20s_ppvl%3DUS%25253ASD%25253ASC-revcal%252C100%252C100%252C1393%252C673%252C813%252C1440%252C900%252C2%252CLP%3B%20s_sq%3D%3B%20s_cc%3Dtrue%3B%20s_ppv%3DUS%25253ASD%25253ASC-revcal%252C76%252C76%252C813%252C673%252C813%252C1440%252C900%252C2%252CLP%3B%20c_m%3Dwww.google.comNatural%2520Search%3B; s_pers=%20s_fid%3D53F78B21D450619C-35A2BDF1308FACCD%7C1883330301177%3B%20s_dl%3D1%7C1725565701179%3B%20s_ev15%3D%255B%255B%2527NSGoogle%2527%252C%25271725563901180%2527%255D%255D%7C1883330301180%3B'
}


def get_detail(asin: str, country_code: str):
    detail_url = f"https://sellercentral.amazon.com/rcpublic/productmatch?searchKey={asin}&countryCode={country_code}&locale=en-US"
    further_detail_url = f"https://sellercentral.amazon.com/rcpublic/getadditionalpronductinfo?asin={asin}&countryCode={country_code}&fnsku=&searchType=GENERAL&locale=en-US"

    detail = requests.get(detail_url, headers=default_headers)
    further_detail = requests.get(further_detail_url, headers=default_headers)
    print(detail.text)
    return detail, further_detail


def get_program_ids(country_code: str):
    url = f"https://sellercentral.amazon.com/rcpublic/getprograms?countryCode={country_code}&mSku=&locale=en-US"
    response = requests.get(url, headers=default_headers)
    data = json.loads(response.text)

    program_ids = []
    for program in data["programInfoList"]:
        name = program["name"]
        display_priority = program["displayPriority"]
        concatenated_value = f"{name}#{display_priority}"
        program_ids.append(concatenated_value)
    return program_ids


def get_fee_details(asin: str, country_code: str, currency: str, gl: str, price: float, program_ids: List[str]):

    fee_url = f"https://sellercentral.amazon.com/rcpublic/getfees?countryCode={country_code}&locale=en-US"
    payload = {"countryCode": country_code, "itemInfo": {"asin": asin, "glProductGroupName": gl, "packageLength": "0", "packageWidth": "0", "packageHeight": "0", "dimensionUnit": "", "packageWeight": "0",
                                                         "weightUnit": "", "afnPriceStr": str(price), "mfnPriceStr": str(price), "mfnShippingPriceStr": "0", "currency": currency, "isNewDefined": False}, "programIdList": program_ids, "programParamMap": {}}
    response = requests.post(fee_url, json=payload, headers=default_headers)
    return response


if __name__ == "__main__":

    from pprint import pprint as pp
    country_code = "CA"
    currency = "CAD"
    asin = "B08B2GFJ1C"
    detail, further_detail = get_detail(asin, country_code)

    parsed_detail = json.loads(detail.text)
    gl_value = parsed_detail["data"]["otherProducts"]["products"][0]["gl"]

    parsed_further_detail = json.loads(further_detail.text)
    price = parsed_further_detail["data"]["price"]["amount"]

    program_ids = get_program_ids(country_code)
    program_ids.pop()
    fee = get_fee_details(asin, country_code, currency,
                          gl_value, price, program_ids)

    pp(detail.text)
    print("--------")
    pp(further_detail.text)
    print("--------")
    pp(fee.text)

    # response = get_fee_details("B08B2GFJ1C", "CA", "CAD", "gl_kitchen", 68.9, ["Core#0", "MFN#1"])

    # pp(response.text)
