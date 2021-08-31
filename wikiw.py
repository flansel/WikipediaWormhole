#wikiwormhole Copyright Felix Ansell 2021

import requests
import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia('en')
start = 'College_of_Veterinary_Science_and_Animal_Husbandry'
page_py = wiki_wiki.page(start)
target = "Doctor_Who"
closeLinks = []
linkParents = []
allLinks = []
path = []


def trace(link):
    path.append(link)
    if link not in startingLinks:
        parent = linkParents[allLinks.index(link)]
        path.append(parent)
        trace(parent)


def get_closeLinks(target):
    global closeLinks
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action":"query",
        "format":"json",
        "list":"backlinks",
        "bltitle":target,
        "bllimit":"500",
    }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    for i in range(0, len(DATA['query']['backlinks'])):
        closeLinks.append(str(DATA['query']['backlinks'][i]['title']))


def get_links(page):
    linkList = []
    l = page.links
    for title in sorted(l.keys()):
        linkList.append(title)
    return linkList


def go_through_links(links):
    newLink = []
    print(links)
    for link in links:
        if link in closeLinks or link == target:
            #print("found link@", link)
            trace(link)
            return

    for link in links:
        l = wiki_wiki.page(link)
        temp = get_links(l)
        for l in temp:
            newLink.append(l)
            allLinks.append(l)
            linkParents.append(link)
    go_through_links(newLink)


startingLinks = get_links(page_py)


def main():
    get_closeLinks(target)
    ls = get_links(page_py)

    go_through_links(ls)


main()
path.insert(0, target)
path.append(start)
x = list(reversed(path))
f = []
for i in x:
    if i not in f:
        f.append(i)
print(f)
