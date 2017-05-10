from bs4 import BeautifulSoup
import urllib2
import re
import requests
import time
from pymongo import MongoClient
import pandas as pd

client = MongoClient('localhost:27017')



def make_soup(url, coll_url):
    '''
    input: url
    output: beautiful soup object that has commented section removed from html source
    '''
    comm = re.compile("<!--|-->")
    time.sleep(1.1)
    page = urllib2.urlopen(url)
    html = page.read()
    coll_url.insert({'url':url, 'html':html})
    soupdata = BeautifulSoup(comm.sub("", html), 'lxml')
    return soupdata


def get_play_by_play_soup(url, coll_url):
    '''
    input: pass in url link for scraping
    output: scraping query that contains table data to be scraped
    '''
    #Send to make_soup to use regular expression to remove comments from html
    soup = make_soup(url, coll_url)

    pbp = soup.find('table', {'id':'pbp'})

    return pbp

def get_column_headers(pbp):
    '''
    input: play-by-play web scraping object
    output: list of column headers
    '''
    column_headers = []
    for column in pbp.find('tr').findAll('th'):
        column_headers.append(str(column.getText()))
    return column_headers

def get_years(end_year = 2016):
    '''
    output: list of strings of the years of football data to be scraped. data
    only available after 1993
    '''
    years = []
    for year in range(1994, end_year + 1):
        years.append(str(year))
    return years

def get_weeks(num_weeks=17):
    '''
    output: return a list of strings in the form "week_1" for each week in an nfl
    season, only 17 weeks in an nfl regular season
    '''
    weeks = []
    for week in range(1, num_weeks + 1):
        weeks.append('week_' +str(week))
    return weeks

def scrape_one_game(pbp, db):
    '''
    input: play_by_play html table from pro football reference
    output: a list of lists containing play_by_play data from one game
    '''
    column_headers = get_column_headers(pbp)
    home_team = column_headers[7]
    away_team = column_headers[6]
    column_headers[7] = 'home_team'
    column_headers[6] = 'away_team'
    game = []
    for test in pbp.findAll('tr')[2:]:
        try:
            qtr = str(test.find('th', attrs={'data-stat': 'quarter'}).getText())
        except:
            continue
        if not test.findAll('td'):
            continue

        time = str(test.findAll('td')[0].getText())
        down = str(test.findAll('td')[1].getText())
        togo = str(test.findAll('td')[2].getText())
        location = str(test.findAll('td')[3].getText())
        detail = str(test.findAll('td')[4].getText())
        pbp_a = str(test.findAll('td')[5].getText())
        pbp_h = str(test.findAll('td')[6].getText())
        exp_b = str(test.findAll('td')[7].getText())
        exp_a = str(test.findAll('td')[8].getText())
        home_wp = str(test.findAll('td')[9].getText())
        play = [qtr, time, down, togo, location, detail, away_team, home_team, exp_b, exp_a, home_wp]
        data = {k:v for k,v in zip(column_headers, play)}

        db.insert(data)
        game.append(play)
    return game

def get_links_to_scrape(years, weeks):
    '''
    input: list of years/seasons to scrape, list of weeks to scrape
    output: list of links to the boxscores that contain play-by-play data for each game
    of every week for every season indicated
    '''
    links = []
    for year in years:
        for week in weeks:
            time.sleep(1.1)
            link = 'http://www.pro-football-reference.com/years/' + year + '/' + week +'.htm'
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.findAll(class_='game_summary expanded nohover'):
                links.append(str(link.findAll('a')[1]['href']))
    return links

def run_scraper(links, coll_data, coll_url):
    data = []
    for link in links:
        url = "http://www.pro-football-reference.com" + link
        pbp = get_play_by_play_soup(url, coll_url)

        data.extend(scrape_one_game(pbp, coll_data))
    return data


if __name__ == '__main__':
    db_capstone = client['capstone']
    datarows = db_capstone.datarows
    urls = db_capstone.urls
    years = get_years(2016)
    weeks = get_weeks()
    links = get_links_to_scrape(['2016'], weeks)
    data = run_scraper(links, datarows, urls)
    data = pd.DataFrame(list(datarows.find()))
    data.to_csv('2016_season.csv')
    client.close()
