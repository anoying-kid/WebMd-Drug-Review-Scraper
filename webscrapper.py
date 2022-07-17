from bs4 import BeautifulSoup
from extractor import getting_all_reviews
from csv import writer
import requests
import string
import re
import concurrent.futures as cf
import asyncio

class Webmd():
    url = "https://www.webmd.com/drugs/2/alpha/"
    loc = [f'{s}/{s}{t}' for s in string.ascii_lowercase for t in string.ascii_lowercase ]
    # loc = ['a/aa','a/ab','b/ba','b/bb']
    headers= {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"}

    def getting_drug_links(self, var):
        with requests.session() as s:
            new_link = self.url+var
            r = s.get(new_link, headers=self.headers)
            soup = BeautifulSoup(r.text, 'lxml')
            r = soup.find_all('a', {'class': 'alpha-drug-name'})
            return [i['href'] for i in r]

    def number_of_review(self,r):
        r = re.findall(r'\(.*?\)', r.text)
        r = r[0]
        r = r[1:-1]
        return int(r)

    def review_links(self, s, site):
        r = s.get(site, headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        r = soup.find('ul', {'class':'auto-tabs'})
        if r:
            r = r('li')[-1]
            reviews = self.number_of_review(r)
            if (reviews!=0):
                r = r.a['href']
                getting_all_reviews(r, reviews, self.headers)

    async def getting_review_links(self, var):
        links = self.getting_drug_links(var)
        url = "https://www.webmd.com"
        with requests.session() as s:
            with cf.ThreadPoolExecutor() as executor:
                results = [executor.submit(self.review_links, s, url+link) for link in links]
            for res in cf.as_completed(results):
                res.result()

    async def for_all_alphabets(self):
        for var in self.loc:
            await self.getting_review_links(var)

    def main(self):
        with open('webmd.csv', 'a', newline='') as f:
            head = ['Age','Sex','Condition','Rating','Effectiveness','Ease of use', 'Satisfaction', 'Reviews', 'Drug', 'DrugId']
            csv_writer = writer(f)
            csv_writer.writerow(head)
        asyncio.run(self.for_all_alphabets())

if __name__ == '__main__':
    web = Webmd()
    web.main()