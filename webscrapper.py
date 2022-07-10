from bs4 import BeautifulSoup
from extractor import getting_all_reviews
from csv import DictWriter
import requests
import string
import re

class WebmdScraper():
    url = "https://www.webmd.com/drugs/2/alpha/"
    # loc = [f'{s}/{s}{t}' for s in string.ascii_lowercase for t in string.ascii_lowercase ]
    loc = ['a/aa','a/ab','b/ba','b/bb']
    headers= {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"}

    def request_data(self):
        for var in self.loc:
            new_link = self.url+var
            with requests.session() as s:
                r = s.get(new_link, headers=self.headers)
                yield r.text
                # with open('r.html', 'w') as w:
                #     w.write(r.text)
    
    def get_links(self):
        for r in self.request_data():
            soup = BeautifulSoup(r, 'lxml')
            r = soup.find_all('a', {'class': 'alpha-drug-name'})
            for i in r:
                yield i['href']
    
    def entering_links(self):
        url = "https://www.webmd.com"
        for link_direct in self.get_links():
            new_link = url + link_direct
            with requests.session() as s:
                r = s.get(new_link, headers=self.headers)
                yield (r.text,new_link)

    def number_of_review(self,soup):
        r = re.findall(r'\(.*?\)', soup.text)
        r = r[0]
        r = r[1:-1]
        return int(r)

    def getting_review_links(self):
        for r,new_link in self.entering_links():
            soup = BeautifulSoup(r, 'lxml')
            r = soup.find('ul', {'class':'auto-tabs'})
            if r:
                r = r('li')[-1]
                reviews = self.number_of_review(r)
                if (reviews!=0):
                    r = r.a['href']
                    yield (r,reviews)
            else:
                print(new_link)

    def extracting_review_from_page(self):
        for link,reviews in self.getting_review_links():
            if link:
                with open('webmd.csv', 'a') as f:
                    head = ['Age','Sex','Condition','Rating','Effectiveness','Ease of use', 'Satisfaction', 'Reviews', 'Drug', 'DrugId']
                    csv_writer = DictWriter(f, fieldnames=head)
                    if f.tell() == 0:
                        csv_writer.writeheader()
                # yield (link[:-5], int(reviews), self.headers)
                getting_all_reviews(link[:-5], int(reviews), self.headers)

    # def saving_links_to_csv(self):
    #     for link,reviews in self.getting_review_links():
    #         if link:
    #             with open('links.csv','a') as f:
    #                 head = ['links','reviews']
    #                 csv_writer = DictWriter(f,fieldnames=head)
    #                 if f.tell() == 0:
    #                     csv_writer.writeheader()
    #                 csv_writer.writerow({
    #                     'links':link[:-5],
    #                     'reviews':reviews
    #                 })

if __name__ == '__main__':
    webmd = WebmdScraper()
    # webmd.saving_links_to_csv()
    webmd.extracting_review_from_page()