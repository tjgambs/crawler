from BeautifulSoup import BeautifulSoup as Soup
import urllib
import threading
import sched

starting_url = 'http://www.cdm.depaul.edu/about/Pages/People/Faculty.aspx'

used_urls = set()
unused_urls = set()

emails = set()


def download_html(url):
   try:
       html = urllib.urlopen(url).read()
       return Soup(html)
   except:
       return ''
   
def find_urls(url):
    html = download_html(url)
    
    for row in html.findAll('a'):
        try:
            link = row['href']
            if link.startswith('mailto:'):
                continue
            
            if link.startswith('http') and link not in used_urls:
                unused_urls.add(link)
            
            if link.startswith('//') and link not in used_urls:
                unused_urls.add('http:/' +  link[1:])
            
            if link.startswith('/') and not link.startswith('//') and link not in used_urls:
                unused_urls.add('/'.join(url.split('/')[:3]) + link)                            
        except:
            pass
    find_emails(html)

    
def find_emails(html):
    for row in html.findAll('a'):
        if 'mailto:' in str(row) and row['href'].replace('mailto','') not in emails :
            if str(row).find('@') != -1:
                emails.add((row['href'].replace('mailto:','').split('?')[0]))
        
def crawl(p=True):
    find_urls(starting_url)
    while True:
        try:
            link = unused_urls.pop()
            find_urls(link)
            used_urls.add(link)
            if p is True:
                print link
        except:
            pass
        save()

def save():
    try:
        with open('mass_emails.txt','w') as file1:
            for i in emails:
                file1.write(i+'\n')
                
        with open('used_urls.txt','w') as file2:
            for i in used_urls:
                file2.write(i+'\n')
    
        with open('unused_urls','w') as file3:
            for i in unused_urls:
                file3.write(i+'\n')
    except:
        pass
            
if __name__ == '__main__': crawl()
