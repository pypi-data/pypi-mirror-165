import requests
REST_API_KEY = ''


def getKakaoAddressSearchResult(address, api_key=REST_API_KEY):
    base_url = 'https://dapi.kakao.com/v2/local/search/address.json'
    headers = {"Authorization": f"KakaoAK {api_key}"}
    q = f'query={address}'
    res = requests.get(f'{base_url}?{q}', headers=headers).text
    return res
