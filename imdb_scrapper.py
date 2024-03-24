from bs4 import BeautifulSoup
import requests
import re
import json
import hmac
import hashlib
import base64
import urllib.parse



url = "https://www.imdb.com/"
headers = {
    # "authority": "www.imdb.com",
    # "method": "GET",
    # "path": "/",
    # "scheme": "https",
    # "Accept":
    # "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "Accept-Encoding": "gzip, deflate, br, zstd",
    # "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    'Connection': 'keep-alive',
    # "Cookie": "session-id=143-4189353-4103615; session-id-time=2082787201l; ubid-main=134-2063362-0732054; ad-oo=0; ci=e30; _cc_id=5b5a98fbb6e9e2bbd2700fce1ac9c0c2; panoramaId_expiry=1711631608480; panoramaId=a616e53186f29f7be684cc85921f185ca02cfd5df821f281a423c701ca7f09b8; panoramaIdType=panoDevice; _au_1d=AU1D-0100-001711026810-FR9946BK-UN94; _gid=GA1.2.1062795066.1711026814; session-token=C40KGo+J6NOaMJAQ6W3dPM4v3EhSprCIaHc9wpXUELbfYVa9SunxL2EQauTEDZYWFAWj88D83XTvENkNY2X6KJfp0uZL+KXPgVB5NkJ+aPZ4oanKRI5EdYK2++z2R8ljYdKXPVD2Ng+YpFYBPgksnTcXo9Tv00zpD8UpuGVaMFkie15w+yHlsf+QMDsIwT6R9qe0DBKjJUP9Y5hSCdq78k7EPoD7LuwbzhGz1yTPFzrLj+BKGFmkrelNDIHry6G76pyccGS9xnnhYNtMIQsGejUGedRSfMm8iY7Rej11zpKEk5Z7E+b7Lws9GiBJqVqcK6u+yr/cBvRksQtoU+iGkR10Pii6cllI; __gads=ID=00027a5ecd4bd561:T=1711028413:RT=1711028413:S=ALNI_MbrdcO9_SMqrPuyz3xzXGESDrxrEA; __gpi=UID=00000d4f388c6d5e:T=1711028413:RT=1711028413:S=ALNI_MZ3WifwwVEsLXhor6hXU4yZHTx5ng; __eoi=ID=0ddf42796ad94cce:T=1711028413:RT=1711028413:S=AA-Afjab9t7GsuWhyC5Y2go-y9wt; _ga_FVWZ0RM4DH=GS1.1.1711027183.1.1.1711029496.60.0.0; _ga=GA1.2.197886156.1711026814; csm-hit=tb:16PD07F3J0A9S41QVKXH+s-TV457P8A3Q04FW32X3XZ|1711030283817&t:1711030283817&adb:adblk_no"
    # ,"Transfer-Encoding": "chunked"
}
searchUrl = "https://v3.sg.media-imdb.com/suggestion/x/{search_text}.json?includeVideos=1"
genre_url = "https://www.imdb.com/search/title/?genres={}"

base = "https://www.imdb.com"

def base64_encoded(data):
    # json_str = json.dumps(data)
    # print("next data",json_str)
    # Encode the JSON string to base64
    # base64_encoded_data = base64.b64encode(json_str.encode()).decode()
    # encoded_data = base64.b64encode(json.dumps(data).encode()).decode()
    # json_str = json.dumps(data)

    # # Encode the JSON string to base64
    # encoded_data = base64.b64encode(json_str.encode()).decode()
    json_str = json.dumps(data)

    # Encode the JSON string to base64
    encoded_data = base64.b64encode(json_str.encode()).decode()

    # Format the encoded data
    formatted_data = encoded_data.replace('+', '-').replace('/', '_').rstrip('=')

    print(formatted_data)
    print(encoded_data)

    return encoded_data


def encode(json_data):
    

    # JSON data to be hashed
   
    # Convert the data to a JSON string
    # json_data = json.dumps(data, sort_keys=True)

    # Key for HMAC
    key = b'65dd1bac6fea9c75c87e2c0435402c1296b5cc5dd908eb897269aaa31fff44b1'

    # Calculate HMAC-SHA256 hash
    hmac_hash = hmac.new(key, json_data.encode(), hashlib.sha256).hexdigest()

    print("HMAC-SHA256 Hash:", hmac_hash)

def hit_requests(url,payload):
    encoded_payload = urllib.parse.urlencode({"query": payload})

    # Create the final URL
    url = f"{url}?{encoded_payload}"
    print("===================================\n")
    print(url)

    session = requests.Session()
    response = session.get(url)
    if not response or not response.content:
        return
    return response.content
    
def fetch_imdb(url, genre):
    next_navigation = ""
    # url = "https://www.imdb.com/search/title/?genres=horror"
    navigation_url = "https://caching.graphql.imdb.com/"
    session = requests.Session()
    response = session.get(url, headers=headers)
    if not response or not response.content:
        return
    print("2. Poor Things" in response.text)
    soup_home = BeautifulSoup(response.text,'html.parser')
    # print(soup_home.get()) 
    elements = soup_home.find(class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-748571c8-0 jmWPOZ detailed-list-view ipc-metadata-list--base")
    final_list = []
    # next_data_navigation = soup_home.find('script', id='__NEXT_DATA__')
    # if next_data_navigation:
    #     next_navigation = next_data_navigation.get_text()
    start = 50
    search_string = 'ref_=sr_i_{}'.format(start)

    # Find the <a> tag based on the dynamically generated search string
    target_a_tag = soup_home.find('a', href=lambda href: href and search_string in href)

    # Get the 'href' attribute value
    if target_a_tag:
        href_value = target_a_tag.get('href')
        print("761",href_value)
        searched_text = re.search(r"[a-z]{2}[\d]{7}",href_value,re.I)
        if searched_text:
            sea_val = searched_text.group()
            print(sea_val)
    print("genre - ",genre)
    next_data = {
        # "esToken":["575","575",str(href_value)],
        "esToken":["168","168","tt3783958"],
    
        "filter":{"constraints":{"genreConstraint":{
            "allGenreIds":[genre],"excludeGenreIds":[]}},
            "language":"en-US","sort":{"sortBy":"POPULARITY","sortOrder":"ASC"},"resultIndex": start-1}}
   
    base64_encoded_data = base64_encoded(next_data)
    print("==\n",base64_encoded_data,"==\n")
    # operationName: "AdvancedTitleSearch"
    payload = {
    "operationName": "AdvancedTitleSearch",
    "variables": {
        "after": base64_encoded_data,
        "first": 50,
        "genreConstraint": {
            "allGenreIds": [genre],
            "excludeGenreIds": []
        },
        "locale": "en-US",
        "sortBy": "POPULARITY",
        "sortOrder": "ASC"
    },
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "65dd1bac6fea9c75c87e2c0435402c1296b5cc5dd908eb897269aaa31fff44b1",
                "version": 1
            }
        }
        }
    # tried to fetch the navigation, every thin
    # new_response = hit_requests(navigation_url,payload)
    for element in elements:
        movie_dict = {}
        title = ""
        release_year = ""
        imdb_rating= ""
        imdb_rating_text = element.find(class_='ipc-rating-star--imdb')
        release_year_text = element.find(class_="sc-b0691f29-8 ilsLEX dli-title-metadata-item")
        if release_year_text:
            release_year = release_year_text.get_text(strip=True)
        if imdb_rating_text:
            imdb_rating = imdb_rating_text.text.strip()
            imdb_rating = re.split(r"\s",imdb_rating)
            imdb_rating = imdb_rating[0]
        plot_summary = element.find(class_="ipc-html-content-inner-div").get_text(strip=True)
        data = element.find(class_="ipc-lockup-overlay ipc-focusable")
        href = data['href']
        more_details_api = base + href
        final_response = session.get(more_details_api, headers=headers)
        if not final_response or not final_response.content:
            return
        soup_genre_page = BeautifulSoup(final_response.text,'html.parser')
        # print(soup_genre_page)
        title_ele = soup_genre_page.find(class_="hero__primary-text")
        if title_ele:
            title = title_ele.get_text(strip=True)
        # print(title)
        director = soup_genre_page.find(class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link").get_text(strip=True)
        # print(director)
        ul_element = soup_genre_page.find_all("ul",class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt")
        # Initialize a list to store the texts
        casts = []
        # Extract text from each <a> element within <li> elements
        for ul in ul_element:
            for li_element in ul.find_all('li'):
                if not li_element:
                    continue
                a_element = li_element.find('a')
                if a_element:
                    casts.append(a_element.text.strip())
        movie_dict = {
            "title": title,
            "release_year": release_year,
            "imdb_rating": imdb_rating,
            "plot_summary": plot_summary,
            "director": director,
            "casts": casts
        }
        final_list.append(movie_dict)
    print(final_list)
    with open("sample.json", "w") as outfile: 
        json.dump(final_list, outfile)
        


        


genre = "Comedy"
genre_url = genre_url.format(genre)
fetch_imdb(genre_url, genre)


