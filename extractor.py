from bs4 import BeautifulSoup
from csv import writer
import requests
import re
import concurrent.futures as cf
# from webscrapper import WebmdScraper

def age_sex(soup):
    soup = soup.find('div', {'class':'details'})
    soup = soup.text.lower()
    age = soup.find('-')
    sex = soup.find('male')
    if(age>=0 and sex>=0):
        age = soup[age-2:age+3]
        if(soup[sex-1]=='e'):
            sex = 'Female'
        else:
            sex = 'Male'
        return age,sex
    return (0,0)

def condition(soup):
    soup = soup.find('strong', {'class':'condition'})
    if soup:
        soup = soup.text[11:]
    return soup

def rating(soup):
    soup = soup.find('div', {'role':'slider'})
    return soup['aria-valuenow']

def categories(soup):
    soup = soup.find('div', {'class':'categories'})
    soup = soup.find_all('div',{'role':'slider'})
    return [r['aria-valuenow'] for r in soup]

def description(soup):
    soup = soup.find('p', {'class', 'description-text'})
    if soup:
        soup = soup.text
    return soup

def drug_drugid(url):
    r = re.findall(r'https://www.webmd.com/drugs/drugreview-(.*?)-(.*?).aspx\?drugid=', url)
    if r:
        return r[0]
    return (None, None)

def extracting_data_from_review(soup):
    age,sex = age_sex(soup)
    if (age!=0 or sex!=0):
        cond = condition(soup)
        rate = rating(soup)
        eff, ease, satis = categories(soup)
        reviews = description(soup)
        return [age, sex, cond, rate, eff, ease, satis, reviews]

def write_csv(s, page, till_page, url, headers, drug, drug_id):
    query = f"?conditionid=&sortval=1&pagenumber={page}"
    try:
        r = s.get(url+query, headers=headers)
    except:
        print('\n')
        print(query)
        print('\n')
        # return 0
    else:
        soup = BeautifulSoup(r.text, 'lxml')
        r = soup.find_all('div', {'class':'review-details'})
        for num in r:
            ls = extracting_data_from_review(num)
            if ls:
                ls.extend([drug, drug_id])
                with open('webmd.csv', 'a', newline='') as f:
                    csv_writer = writer(f)
                    csv_writer.writerow(ls)

def getting_all_reviews(url, reviews, headers):
    url = "https://www.webmd.com"+url
    print(f"fetching url {url}")
    till_page = reviews/20
    till_page = (till_page//1)+1 if (till_page%1>0) else till_page//1
    till_page = int(till_page)
    drug_id, drug = drug_drugid(url)
    with cf.ThreadPoolExecutor() as executor:
        with requests.Session() as s:
            results = [executor.submit(write_csv, s, page, till_page, url, headers, drug, drug_id) for page in range(0,till_page)]
            for res in cf.as_completed(results):
                res.result()

if __name__ == '__main__':
    headers= {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"}
    url = "/drugs/drugreview-20512-abreva-topical?drugid=20512&drugname=abreva-cream"
    reviews = 144
    getting_all_reviews(url, reviews, headers)