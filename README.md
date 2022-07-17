<samp>

# Web-Md Drug review scraper

This is python web scraper which will scrap the review of a drug from webmd website.

---

## Installation

Clone the repository
```bash
git clone https://github.com/anoying-kid/WebMd-Drug-Review-Scraper.git
```
```bash
pip install -r requirements.txt
```

Optional

1) complete the process in one line using setup.sh
```
./setup.sh
```
(dont forget to give the execute permission)

For Mac
```
chmod 775 setup.sh
```

For Linux
```
chmod +x setup.sh
```

For Windows do normally.

---

## Use

This has two files
- webscrapper.py
- extractor.py

### webscrapper.py

This file is the main file for getting the review by each and every alphabet from the [webmd](https://www.webmd.com/drugs/2/index) site.

It will take long time so furthur this code can be minimize for futhur needs.

### extractor.py

This file will only extract the data from a particular site.

e.g.

```python 3
if __name__ == '__main__':
    headers= {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"}
    url = "/drugs/drugreview-20512-abreva-topical?drugid=20512&drugname=abreva-cream"
    reviews = 144
    getting_all_reviews(url, reviews, headers)
```
headers will be same, url wil be url of the review site like [this](https://www.webmd.com/drugs/drugreview-8953-a-g-pro-oral?drugid=8953&drugname=a-g-pro) and dont forgot to give the number of reviews to it.

---

Give food to my cat 🐈‍⬛:
```
0x3B1472F86C6fe9dB5A753e238f9e46580fcFfAD4
```

**NOTE** : My cat is hungry.
</samp>