from bs4 import BeautifulSoup
import requests
import re

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


def fetch_imdb(url):
    url = "https://www.imdb.com/search/title/?genres=comedy"
    session = requests.Session()
    response = session.get(url, headers=headers)
    if not response or not response.content:
        return
    print("2. Poor Things" in response.text)
    soup_home = BeautifulSoup(response.text,'html.parser')
    # print(soup_home.get()) 
    elements = soup_home.find(class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-748571c8-0 jmWPOZ detailed-list-view ipc-metadata-list--base")
    final_list = []
    for element in elements:
        movie_dict = {}
        title = element.find(class_="ipc-title__text").get_text(strip=True)
        release_year = element.find(class_="sc-b0691f29-8 ilsLEX dli-title-metadata-item").get_text(strip=True)
        imdb_rating_text = element.find(class_='ipc-rating-star--imdb').text.strip()
        imdb_rating = re.split(r"\s",imdb_rating_text)
        imdb_rating = imdb_rating[0]
        # director = element.find(class_="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b0691f29-9 klOwFB dli-title").get_text(strip=True)
        # casts = element.find(class_="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b0691f29-9 klOwFB dli-title").get_text(strip=True)
        plot_summary = element.find(class_="ipc-html-content-inner-div").get_text(strip=True)
        data = element.find(class_="ipc-lockup-overlay ipc-focusable")
        href = data['href']
        # print(href)
        more_details_api = base + href
        final_response = session.get(more_details_api, headers=headers)
        if not final_response or not final_response.content:
            return
        soup_genre_page = BeautifulSoup(final_response.text,'html.parser')
        # print(soup_genre_page)
        director = soup_genre_page.find(class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link").get_text(strip=True)
        print(director)
        ul_element = soup_genre_page.find_all("ul",class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt")

        # Initialize a list to store the texts
        texts = []

        # Extract text from each <a> element within <li> elements
        for ul in ul_element:
            for li_element in ul.find_all('li'):
                if not li_element:
                    continue
                a_element = li_element.find('a')
                if a_element:
                    texts.append(a_element.text.strip())
        movie_dict = {
            "titile": title,
            "release_year": release_year,
            "imdb_rating": imdb_rating,
            "plot_summary": plot_summary,
            "director": director,
            "casts": texts
        }
        break
        


genre = "comedy"
genre_url = genre_url.format(genre)
fetch_imdb(genre_url)

