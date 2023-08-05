from requests_html import HTMLSession

session = HTMLSession()
url = "https://pic.netbian.com"
r = session.get(url)
selector = '#main > div.slist'
about = r.html.find(selector, first=True)

print(r.html.absolute_links)


'''
img_Elements = about.find('img')

img_url_lst = [url + i.attrs['src'] for i in img_Elements]

for img_url in img_url_lst:
    name = "out/" + img_url.split('/')[-1]
    f = open(name, 'wb')
    f.write(session.get(img_url).content)
    print(f'downloaded file:{name} ')
    f.close()

'''
