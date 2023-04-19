import requests
from requests import Session
from bs4 import BeautifulSoup


BASE = 'https://tioanime.com/'
DIRECTORIO = 'https://tioanime.com/directorio'


def get_anime_info(list):
    info = []
    for ep in list.contents:
        if ep == '\n':continue
        animename = ep.contents[1].contents[1].contents[3].next
        animeurl = ep.contents[1].contents[1].attrs['href']
        animefigure = ''
        try:
            animefigure = ep.contents[1].contents[1].contents[1].contents[1].contents[0].attrs['src']
        except:
            animefigure = ep.contents[1].contents[1].contents[1].contents[0].contents[0].attrs['src']
        info.append({'Anime':animename,'Url':animeurl,'Image':animefigure})
    return info


def get_latest_episodies():
    global BASE
    resp = requests.get(BASE)
    html = str(resp.text).replace('/uploads','https://tioanime.com/uploads')
    html = html.replace('/ver','https://tioanime.com/ver')
    soup = BeautifulSoup(html, "html.parser")
    episodios = soup.find_all('ul')[1]
    return get_anime_info(episodios)


def get_dir_url(index,named=True):
    global DIRECTORIO
    if named:
        return DIRECTORIO + '?q=' + str(index)
    return DIRECTORIO + '?p=' + str(index)

def get_url_from(name):
    pass

def get_result(directory,name=''):
    searchList = []
    resp = requests.get(directory)
    html = str(resp.text).replace('/uploads','https://tioanime.com/uploads')
    html = html.replace('/anime','https://tioanime.com/anime')
    soup = BeautifulSoup(html, "html.parser")
    animes = get_anime_info(soup.find_all('ul')[1])
    for anime in animes:
        if name == '':
            searchList.append(anime)
            continue
        if name in anime['Anime']:
            searchList.append(anime)
    return searchList

def get_dir_size():
    global DIRECTORIO
    resp = requests.get(DIRECTORIO)
    soup = BeautifulSoup(resp.text, "html.parser")
    return int(soup.find_all('ul')[2].contents[8].next.next)


def search(searched,named=True):
    return get_result(get_dir_url(searched,named))

def get_mega(list):
    mega = ''
    for l in list:
        try:
            if 'mega' in l.contents[1].attrs['href']:
                mega = l.contents[1].attrs['href']
                break
        except:
            pass
    return mega

def get_mega_url(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    link = get_mega(soup.find_all('td'))
    mega = link.replace('https://mega.nz','https://mega.nz/file')
    code = mega.split('/')[-1]
    fixed_code_array = code.split('!')
    fixed_code = fixed_code_array[1]+fixed_code_array[0]+fixed_code_array[2]
    mega = mega.replace(code,fixed_code)
    return mega


def get_info(url):
    episodies = []
    resp = requests.get(url)
    html = resp.text.replace('/ver','https://tioanime.com/ver')
    soup = BeautifulSoup(html, "html.parser")
    script = str(soup.find_all('script')[-1].next).replace(' ','').replace('\n','').replace('\r','')
    tokens = script.split(';')
    epis = tokens[1].split(',')
    index = 1
    for ep in epis:
        episodies.append(str(url).replace('anime/','ver/')+'-'+str(index))
        index+=1
    sinopsis = soup.find('p',{'class':'sinopsis'}).next
    return {'sinopsis':sinopsis,'episodies':episodies}

#searchSeries('naruto')
#getAnimeEpisodies('https://tioanime.com/anime/getsuyoubi-no-tawawa-2')