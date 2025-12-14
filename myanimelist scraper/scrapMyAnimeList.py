from bs4 import BeautifulSoup
import requests
import time
import getUserAgent

genresPages = []
def scrapMyAnimeList():
    response = requests.get('https://myanimelist.net/anime.php')
    soup = BeautifulSoup(response.text, 'html.parser')
    genre_link = soup.find_all('div', class_="genre-link")
    for i in genre_link[0]:
        links = i.find_all('div', class_="genre-list al")
        for link in links:
            genresPages.append(link.find('a').get('href'))

headers = {
    'user-agent': getUserAgent.getAgent()
}

proxies = {
    "http": f"http://{getUserAgent.getProxy()}"
}

animes = []
covers = []

scrapMyAnimeList()
for genre in genresPages:
    for page in range(50):
        try:
            request = 0
            if page == 0:
                request = requests.get(f'https://myanimelist.net{genre}', headers=headers, proxies=proxies)
            else:
                request = requests.get(f'https://myanimelist.net{genre}?page={page}', headers=headers, proxies=proxies)

            if request.status_code == 404:
                break
            else:
                soup = BeautifulSoup(request.text, 'html.parser')
                animeCards = soup.find_all('div', class_="seasonal-anime-list")
                for anime in animeCards: #scrape the name and the link of the image for every anime on the page
                    titles = anime.find_all('div', class_="title-text")
                    for i in titles:
                        title = i.find('h2', class_="h2_anime_title").get_text()
                        titleToUrl = title.replace(' ', '-')
                        animes.append(title)
                    images = anime.find_all('div', class_="image")
                    for i in images:
                        image = i.find('img', class_="lazyload").get('data-src')
                        covers.append(image)
            
            with open('animes.txt', 'w+', encoding='utf-8') as file:
                for name, cover in zip(animes, covers):
                    file.write(f"{name} : {cover}\n")

            time.sleep(4)

        except Exception as e:
            print(e)