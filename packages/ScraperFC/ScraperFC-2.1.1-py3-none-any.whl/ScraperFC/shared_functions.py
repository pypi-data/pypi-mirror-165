from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from IPython.display import clear_output
import random
import pandas as pd
import numpy as np


################################################################################
def check_season(year, league, source):
    valid = {
        'All': {},
        'FBRef': {
            'EPL': 1993,
            'La Liga': 1989,
            'Bundesliga': 1989,
            'Serie A': 1989,
            'Ligue 1': 1996,
            'MLS': 1996
        },
        'Understat': {
            'EPL': 2015,
            'La Liga': 2015,
            'Bundesliga': 2015,
            'Serie A': 2015,
            'Ligue 1': 2015
        },
        'FiveThirtyEight': {
            'EPL': 2017,
            'La Liga': 2017,
            'Bundesliga': 2017,
            'Serie A': 2017,
            'Ligue 1': 2017
        },
        'SofaScore': {
            'USL League One': 2019
        },
        'Capology': {
            'Bundesliga': 2014,
            '2.Bundesliga': 2020,
            'EPL': 2014,
            'EFL Championship': 2014,
            'Serie A': 2010,
            'Serie B': 2020,
            'La Liga': 2014,
            'La Liga 2': 2020,
            'Ligue 1': 2014,
            'Ligue 2': 2020,
            'Eredivisie': 2014,
            'Primeira Liga': 2014,
            'Scottish PL': 2020,
            'Super Lig': 2014,
            'Belgian 1st Division': 2014
        },
        'Transfermarkt': {
            'EPL': 1993,
            'EFL Championship': 2005,
            'EFL1': 2005,
            'EFL2': 2005,
            'Bundesliga': 1964,
            '2.Bundesliga': 1982,
            'Serie A': 1930,
            'Serie B': 1930,
            'La Liga': 1929,
            'La Liga 2': 1929,
            'Ligue 1': 1970,
            'Ligue 2': 1993,
            'Eredivisie': 1955,
            'Scottish PL': 2004,
            'Super Lig': 1960,
            'Jupiler Pro League': 1987,
            'Liga Nos': 1994,
            'Russian Premier League': 2011,
            'Brasileirao': 2001,
            'Argentina Liga Profesional': 2015,
            'MLS': 1996,
        },
    }
    
    assert source in list(valid.keys())
    error = None
    
    # make sure year is an int
    if type(year) != int:
        error = "Year needs to be an integer."
        return error, False
    
    # Make sure league is a valid string for the source
    if type(league)!=str or league not in list(valid[source].keys()):
        error = 'League must be a string. Options are {}'.format(list(valid[source].keys()))
        return error, False
    
    # Make sure the source has data from the requested league and year
    if year < valid[source][league]:
        error = 'Year invalid for source {} and league {}. Must be {} or later.'.format(source, league, valid[source][league])
        return error, False
    
    return error, True

################################################################################
def get_proxy():
    """ Adapted from https://stackoverflow.com/questions/59409418/how-to-rotate-selenium-webrowser-ip-address """
    options = Options()
    options.headless = True
    options.add_argument("window-size=700,600")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    clear_output()
    
    try:
        driver.get("https://sslproxies.org/")
        table = driver.find_elements_by_tag_name("table")[0]
        df = pd.read_html(table.get_attribute("outerHTML"))[0]
        df = df.iloc[np.where(~np.isnan(df["Port"]))[0],:] # ignore nans

        ips = df["IP Address"].values
        ports = df["Port"].astype("int").values

        driver.quit()
        proxies = list()
        for i in range(len(ips)):
            proxies.append("{}:{}".format(ips[i], ports[i]))
        i = random.randint(0, len(proxies)-1)
        return proxies[i]
    except Exception as e:
        driver.close()
        driver.quit()
        raise e
