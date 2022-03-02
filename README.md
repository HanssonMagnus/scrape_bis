@author: hansson.carl.magnus@gmail.com

## Update 2022-03-02
After requests the code is made available for the data collection in my paper
[Evolution of topics in central bank speech communication](https://arxiv.org/abs/2109.10058).

The original dataset, used in the paper, containing central bank speeches from 1997-01-07 to
2020-01-10 can be found at [Kaggle](https://www.kaggle.com/magnushansson/central-bank-speeches).

## The scripts
`scrape_bis`:
Scrapes the BIS website for all central bank (118 institutions) speeches over the period 1997-today and
sorts the speeches into directories named as the institution in the meta data "extra title" from
the BIS webpage. It takes around `3h` to collect all the speeches and the total size of the directory
of pdfs is around `2.4G`.
The scraper run sequentially and thus does not hit the BIS server hard. I've not noticed any
request restrictions from the server.

`pdf_to_txt`:
Converts the pdf files into txt files such that they can be processed and used in NLP. It takes
around `29min` to converst all the pdf files to txt files and the size of the directory of txts is
around `326M`.

The code can run on standard laptops with more than `2.5G` of disk space.

## Required software
Required:
- Python 3
- Packages listed in `Pipfile`

Optional:
- [Pipenv](https://pipenv.pypa.io/en/latest/)

For a short introduction to `Pipenv` see
[this blog post](https://magnushansson.xyz/blog_posts/software/2020-03-26-Pipenv).

## Run the scraper
Step 1:
Clone repo and cd into the directory,
```
git clone https://github.com/HanssonMagnus/scrape_bis.git
cd scrape_bis
```

Step 2:
Create a pipenv environment and install packages,
```
pipenv shell
pipenv install
```

Step 3:
Run the scraper,
```
cd source/0_scrape_bis
python main.py
```

Step 4:
Convert pdfs to txts,
```
cd ../1_pdf_to_txt
python pdf_to_txt.py
```

Note: Step 2 can be changed to any other virtual environment or simply installing the required
packages in `Pipfile` with `pip install`.

## Logs
The scripts create a directory, `logs`, where log files for the scripts are saved.
`logging_bis_scraper.log` collects all speeches that it fails to download (around `100`), together
with the URLs to the speeches such that it is possible to manually investigate or download them.
`logging_pdf_to_txt.log` collects the pdf files that the script was unable to convert into txt
files. When the scripts are done you can compare the pdf and txt directories that you are
interested in and if they differ significantly in number you can investigate it.

## How it works
The speeches are sorted on the web-based search engine by dates, e.g., the
speeches from 08 Jan 2020 are named:
```
    https://www.bis.org/review/r200108a.pdf
    https://www.bis.org/review/r200108b.pdf
    .
    .
    .
    https://www.bis.org/review/r200108e.pdf
```

Thus the URL is the same and the date is the same, but the last letter is changing. The scraper
scrapes all speeches by creating a `datelist` with all dates from 1997 (the first speech) to today
and downloading all speeches for each day (incrementing a, b, c and so on) until there is no more
files for that day (page not found).
