import datetime
from IPython.display import clear_output
import numpy as np
import pandas as pd
from ScraperFC.shared_functions import check_season
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from lxml import etree
from tqdm import tqdm
import time


class FBRef:
    
    ################################################################################
    def __init__(self): #, driver="chrome"):
        #assert driver in ["chrome", "firefox"]
        
        #if driver == "chrome":
        from selenium.webdriver.chrome.service import Service as ChromeService
        options = Options()
        options.headless = True
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"+\
            " (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        )
        options.add_argument("window-size=1400,600")
        options.add_argument("--incognito")
        prefs = {"profile.managed_default_content_settings.images": 2} # don't load images
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                           options=options)
#         elif driver == "firefox":
#             from selenium.webdriver.chrome.service import Service as FirefoxService
#             self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
      
    ################################################################################    
    def close(self):
        self.driver.close()
        self.driver.quit()

    ################################################################################
    def get(self, url):
        self.driver.get(url)
        time.sleep(60)

    ################################################################################
    def get_season_link(self, year, league):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        
        # urls are to league's seasons history page
        # finders are used later to make sure we're getting the right season URL
        urls_finders = {
            "EPL": {
                "url": "https://fbref.com/en/comps/9/history/Premier-League-Seasons",
                "finder": "Premier-League-Stats"
            },
            "La Liga": {
                "url": "https://fbref.com/en/comps/12/history/La-Liga-Seasons",
                "finder": "La-Liga-Stats"
            },
            "Bundesliga": {
                "url": "https://fbref.com/en/comps/20/history/Bundesliga-Seasons",
                "finder": "Bundesliga-Stats"
            },
            "Serie A": {
                "url": "https://fbref.com/en/comps/11/history/Serie-A-Seasons",
                "finder": "Serie-A-Stats"
            },
            "Ligue 1": {
                "url": "https://fbref.com/en/comps/13/history/Ligue-1-Seasons",
                "finder": "Ligue-1-Stats" if year>=2003 else "Division-1-Stats"
            },
            "MLS": {
                "url": "https://fbref.com/en/comps/22/history/Major-League-Soccer-Seasons",
                "finder": "Major-League-Soccer-Stats"
            },
        }
        url = urls_finders[league]["url"]
        finder = urls_finders[league]["finder"]
        
        # self.driver.get(url) # go to league's seasons page
        self.get(url)
        
        # Generate season string to find right element
        if league != "MLS":
            season = str(year-1)+'-'+str(year)
        else:
            season = str(year)
           
        # Get url to season
        for el in self.driver.find_elements(By.LINK_TEXT, season):
            if finder in el.get_attribute('href'):
                return el.get_attribute('href')
            else:
                print('ERROR: Season not found.')
                return -1
    
    ################################################################################
    def get_match_links(self, year, league):
        print("Gathering match links.")
        url = self.get_season_link(year, league)
        
        # go to the scores and fixtures page
        url = url.split('/')
        first_half = '/'.join(url[:-1])
        second_half = url[-1].split('-')
        second_half = '-'.join(second_half[:-1])+'-Score-and-Fixtures'
        url = first_half+'/schedule/'+second_half
        # self.driver.get(url)
        self.get(url)
        
        # Get links to all of the matches in that season
        finders = {
            "EPL": "-Premier-League",
            "La Liga": "-La-Liga",
            "Bundesliga": "-Bundesliga",
            'Serie A': '-Serie-A',
            'Ligue 1': '-Ligue-1' if year>=2003 else '-Division-1',
            "MLS": "-Major-League-Soccer"
        }
        finder = finders[league]
        
        links = set()
        # only get match links from the fixtures table
        for table in self.driver.find_elements(By.TAG_NAME, "table"):
            if table.get_attribute('id')!='' and table.get_attribute('class')!='':
                # find the match links
                for element in tqdm(table.find_elements(By.TAG_NAME, "a")):
                    href = element.get_attribute('href')
                    if (href) and ("/matches/" in href) and (href.endswith(finder)):
                        links.add(href)
        
        return list(links)
    
    ################################################################################
    def add_team_ids(self, df, insert_index, season_url, tag_name):
        # self.driver.get(season_url)
        self.get(season_url)
        team_ids = list()
        for el in self.driver.find_elements(By.XPATH, '//{}[@data-stat="squad"]'.format(tag_name)):
            if el.text != '' and el.text != 'Squad':
                team_id = el.find_element(By.TAG_NAME, 'a') \
                            .get_attribute('href') \
                            .split('/squads/')[-1] \
                            .split('/')[0]
                team_ids.append(team_id)
        df.insert(insert_index, 'team_id', team_ids)
        return df

    ################################################################################
    def add_player_ids_and_links(self, df, url):
        # self.driver.get(url)
        self.get(url)
        player_ids = list()
        player_links = list()
        for el in self.driver.find_elements(By.XPATH, '//td[@data-stat="player"]'):
            if el.text != '' and el.text != 'Player':
                player_id = el.find_element(By.TAG_NAME, 'a') \
                    .get_attribute('href') \
                    .split('/players/')[-1] \
                    .split('/')[0]
                player_ids.append(player_id)
                player_links.append(el.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        df.insert(2, 'player_id', player_ids) # insert player IDs as new col in df
        df.insert(2, 'player_link', player_links) # insert player links as new col in df
        return df
    
    ################################################################################
    def normalize_table(self, xpath):
        button = self.driver.find_element(By.XPATH, xpath)
        self.driver.execute_script("arguments[0].click()",button)
    
    ################################################################################
    def get_html_w_id(self, ID):
        return self.driver.find_element(By.ID, ID).get_attribute('outerHTML')

    ################################################################################
    def scrape_league_table(self, year, league, normalize=False):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        print('Scraping {} {} league table'.format(year, league))
        season = str(year-1)+'-'+str(year)
        url = self.get_season_link(year,league)
        df = pd.read_html(url)
        lg_tbl = df[0].copy()
        #### Drop columns and normalize
        if year >= 2018:
            lg_tbl.drop(columns=["xGD/90"], inplace=True)
        if normalize and year >= 2018:
            lg_tbl.iloc[:,3:13] = lg_tbl.iloc[:,3:13].divide(lg_tbl["MP"], axis="rows")
        elif normalize and year < 2018:
            lg_tbl.iloc[:,3:10] = lg_tbl.iloc[:,3:10].divide(lg_tbl["MP"], axis="rows")
        #### Scrape western conference if MLS
        if league == "MLS":
            west_tbl = df[2].copy()
            if year >= 2018:
                west_tbl.drop(columns=["xGD/90"], inplace=True)
            if normalize and year >= 2018:
                west_tbl.iloc[:,3:13] = west_tbl.iloc[:,3:13].divide(west_tbl["MP"], axis="rows")
            elif normalize and year < 2018:
                west_tbl.iloc[:,3:10] = west_tbl.iloc[:,3:10].divide(west_tbl["MP"], axis="rows")
            return (lg_tbl, west_tbl)
        lg_tbl = self.add_team_ids(lg_tbl, 2, url, "td") # Get team IDs
        return lg_tbl
    
    ################################################################################
    def scrape_standard(self, year, league, normalize=False, player=False):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        print('Scraping {} {} standard stats'.format(year, league))
        season = str(year-1)+'-'+str(year)
        url = self.get_season_link(year,league)
        new = url.split('/')
        new = '/'.join(new[:-1]) + '/stats/' + new[-1]
        if player:
            # self.driver.get(new)
            self.get(new)
            if normalize:
                self.normalize_table('//*[@id=\"stats_standard_per_match_toggle\"]')
            # get html and scrape table
            html = self.get_html_w_id("stats_standard")
            df = pd.read_html(html)[0]
            # drop duplicate header rows and link to match logs
            df = df[df[("Unnamed: 0_level_0","Rk")]!="Rk"].reset_index(drop=True)
            df.drop(columns="Per 90 Minutes", level=0, inplace=True)
            df.drop(columns="Matches", level=1, inplace=True)
            # convert some column types from str to float
            for col in list(df.columns.get_level_values(0)):
                if 'Unnamed' not in col:
                    df[col] = df[col].astype("float")
            # add some calculated columns
            df[("Performance","G+A")] = df[("Performance","Gls")] + df[("Performance","Ast")]
            df[("Performance","G+A-PK")] = df[("Performance","G+A")] - df[("Performance","PK")]
            if year >= 2018:
                df[("Expected","xG+xA")] = df[("Expected","xG")] + df[("Expected","xA")]
            df = self.add_player_ids_and_links(df, new) # get player IDs
            return df
        else:
            df = pd.read_html(new)
            squad = df[0].copy()
            vs = df[1].copy()
            drop_cols = squad.xs("Per 90 Minutes", axis=1, level=0, drop_level=False).columns
            squad.drop(columns=drop_cols, inplace=True)
            vs.drop(columns=drop_cols, inplace=True)
            if normalize:
                squad.iloc[:,8:] = squad.iloc[:,8:].divide(squad[("Playing Time","90s")], axis="rows")
                vs.iloc[:,8:] = vs.iloc[:,8:].divide(vs[("Playing Time","90s")], axis="rows")
            col = ("Performance","G+A")
            squad[col] = squad[("Performance","Gls")] + squad[("Performance","Ast")]
            vs[col] = vs[("Performance","Gls")] + vs[("Performance","Ast")]
            col = ("Performance","G+A-PK")
            squad[col] = squad[("Performance","G+A")] - squad[("Performance","PK")]
            vs[col] = vs[("Performance","G+A")] - vs[("Performance","PK")]
            if year >= 2018:
                col = ("Expected","xG+xA")
                squad[col] = squad[("Expected","xG")] + squad[("Expected","xA")]
                vs[col] = vs[("Expected","xG")] + vs[("Expected","xA")]
            # Get team IDs
            squad = self.add_team_ids(squad, 1, new, 'th') 
            vs = self.add_team_ids(vs, 1, new, 'th')
            return squad, vs
    
    ################################################################################
    def scrape_gk(self, year, league, normalize=False, player=False):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        elif league in['La Liga','Bundesliga','Ligue 1'] and year<2000:
            print('Goalkeeping stats not available from',league,'before 1999/2000 season.')
            return -1
        elif league=='Serie A' and year<1999:
            print('Goalkeeping stats not available from Serie A before 1998/99 season.')
            return -1
        print('Scraping {} {} goalkeeping stats'.format(year, league))
        season = str(year-1)+'-'+str(year)
        url = self.get_season_link(year,league)
        new = url.split('/')
        new = '/'.join(new[:-1]) + '/keepers/' + new[-1]
        new = new.replace("https","http")
        if player:
            # self.driver.get(new)
            self.get(new)
            if normalize:
                self.normalize_table("//*[@id=\"stats_keeper_per_match_toggle\"]")
            # get html and scrape table
            html = self.get_html_w_id("stats_keeper")
            df = pd.read_html(html)[0]
            # drop duplicate header rows and link to match logs
            df = df[df[("Unnamed: 0_level_0","Rk")]!="Rk"].reset_index(drop=True)
            df.drop(columns=("Performance","GA90"), inplace=True)
            df.drop(columns="Matches", level=1, inplace=True)
            # convert type from str to float
            for col in list(df.columns.get_level_values(0)):
                if 'Unnamed' not in col:
                    df[col] = df[col].astype("float")
            df = self.add_player_ids_and_links(df, new) # get player IDs
            return df
        else:
            df = pd.read_html(new)
            squad = df[0].copy()
            vs = df[1].copy()
            squad.drop(columns=("Performance","GA90"), inplace=True)
            vs.drop(columns=("Performance","GA90"), inplace=True)
            if normalize:
                keep_cols = [("Performance","Save%"), ("Performance","CS%"), ("Penalty Kicks","Save%")]
                keep = squad[keep_cols]
                squad.iloc[:,6:] = squad.iloc[:,6:].divide(squad[("Playing Time","90s")], axis="rows")
                squad[keep_cols] = keep
                keep = vs[keep_cols]
                vs.iloc[:,6:] = vs.iloc[:,6:].divide(vs[("Playing Time","90s")], axis="rows")
                vs[keep_cols] = keep
            # Get team IDs
            squad = self.add_team_ids(squad, 1, new, 'th') 
            vs = self.add_team_ids(vs, 1, new, 'th')
            return squad, vs
    
    ################################################################################
    def scrape_adv_gk(self, year, league, normalize=False, player=False):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        elif year < 2018:
            print("Advanced goalkeeping stats not available from before the 2017/18 season.")
            return -1
        print('Scraping {} {} advanced goalkeeping stats'.format(year, league))
        season = str(year-1)+'-'+str(year)
        url = self.get_season_link(year,league)
        new = url.split('/')
        new = '/'.join(new[:-1]) + '/keepersadv/' + new[-1]
        new = new.replace("https","http")
        if player:
            # self.driver.get(new)
            self.get(new)
            if normalize:
                self.normalize_table("//*[@id=\"stats_keeper_adv_per_match_toggle\"]")
            # get html and scrape table
            html = self.get_html_w_id("stats_keeper_adv")
            df = pd.read_html(html)[0]
            # drop duplicate header rows and link to match logs
            df = df[df[("Unnamed: 0_level_0","Rk")]!="Rk"].reset_index(drop=True)
            df.drop(columns=["Matches", "#OPA/90", "/90"], level=1, inplace=True)
            # convert type from str to float
            for col in list(df.columns.get_level_values(0)):
                if 'Unnamed' not in col:
                    df[col] = df[col].astype("float")
            df = self.add_player_ids_and_links(df, new) # get player IDs
            return df
        else:
            df = pd.read_html(new)
            squad = df[0].copy()
            vs = df[1].copy()
            squad.drop(columns=[("Expected","/90"), ("Sweeper","#OPA/90")], inplace=True)
            vs.drop(columns=[("Expected","/90"), ("Sweeper","#OPA/90")], inplace=True)
            if normalize:
                keep_cols = [
                    ("Launched","Cmp%"), ("Passes","Launch%"), ("Passes","AvgLen"),
                    ("Goal Kicks","Launch%"), ("Goal Kicks", "AvgLen"), 
                    ("Crosses","Stp%"), ("Sweeper","AvgDist")
                ]
                keep = squad[keep_cols]
                squad.iloc[:,3:] = squad.iloc[:,3:].divide(squad[("Unnamed: 2_level_0","90s")], axis="rows")
                squad[keep_cols] = keep
                keep = vs[keep_cols]
                vs.iloc[:,3:] = vs.iloc[:,3:].divide(vs[("Unnamed: 2_level_0","90s")], axis="rows")
                vs[keep_cols] = keep
            # Get team IDs
            squad = self.add_team_ids(squad, 1, new, 'th') 
            vs = self.add_team_ids(vs, 1, new, 'th')
            return squad, vs
    
    ################################################################################
    def scrape_shooting(self, year, league, normalize=False, player=False):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        print('Scraping {} {} shooting stats'.format(year, league))
        season = str(year-1)+'-'+str(year)
        url = self.get_season_link(year,league)
        new = url.split('/')
        new = '/'.join(new[:-1]) + '/shooting/' + new[-1]
        new = new.replace("https","http")
        if player:
            # self.driver.get(new)
            self.get(new)
            if normalize:
                self.normalize_table("//*[@id=\"stats_shooting_per_match_toggle\"]")
            # get html and scrape table
            html = self.get_html_w_id("stats_shooting")
            df = pd.read_html(html)[0]
            # drop duplicate header rows and link to match logs
            df = df[df[("Unnamed: 0_level_0","Rk")]!="Rk"].reset_index(drop=True)
            df.drop(columns=[("Standard","Sh/90"),("Standard","SoT/90")], inplace=True)
            df.drop(columns="Matches", level=1, inplace=True)
            # convert type from str to float
            for col in list(df.columns.get_level_values(0)):
                if 'Unnamed' not in col:
                    df[col] = df[col].astype("float")
            df = self.add_player_ids_and_links(df, new) # get player IDs
            return df
        else:
            df = pd.read_html(new)
            squad = df[0].copy()
            vs = df[1].copy()
            squad.drop(
                columns=[("Standard","Sh/90"), ("Standard","SoT/90")], 
                inplace=True
            )
            vs.drop(
                columns=[("Standard","Sh/90"), ("Standard","SoT/90")],
                inplace=True
            )
            if normalize:
                keep_cols = [("Standard","SoT%"), ("Standard","Dist")]
                keep = squad[keep_cols]
                squad.iloc[:,3:] = squad.iloc[:,3:].divide(squad[("Unnamed: 2_level_0","90s")], axis="rows")
                squad[keep_cols] = keep
                keep = vs[keep_cols]
                vs.iloc[:,3:] = vs.iloc[:,3:].divide(vs[("Unnamed: 2_level_0","90s")], axis="rows")
                vs[keep_cols] = keep
            # Get team IDs
            squad = self.add_team_ids(squad, 1, new, 'th') 
            vs = self.add_team_ids(vs, 1, new, 'th')
            return squad, vs
    
    ################################################################################
    def scrape_passing(self, year, league, normalize=False, player=False):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        elif year < 2018:
            print("Passing stats not available from before the 2017/18 season.")
            return -1
        print('Scraping {} {} passing stats'.format(year, league))
        season = str(year-1)+'-'+str(year)
        url = self.get_season_link(year,league)
        new = url.split('/')
        new = '/'.join(new[:-1]) + '/passing/' + new[-1]
        new = new.replace("https","http")
        if player:
            # self.driver.get(new)
            self.get(new)
            if normalize:
                self.normalize_table("//*[@id=\"stats_passing_per_match_toggle\"]")
            # get html and scrape table
            html = self.get_html_w_id('stats_passing')
            df = pd.read_html(html)[0]
            # drop duplicate header rows and link to match logs
            df = df[df[("Unnamed: 0_level_0","Rk")]!="Rk"].reset_index(drop=True)
            df.drop(
                columns=[("Unnamed: 30_level_0","Matches")],
                inplace=True
            )
            # convert type from str to float
            for col in list(df.columns.get_level_values(0)):
                if 'Unnamed' not in col:
                    df[col] = df[col].astype("float")
            df = self.add_player_ids_and_links(df, new) # get player IDs
            return df
        else:
            df = pd.read_html(new)
            squad = df[0].copy()
            vs = df[1].copy()
            if normalize:
                keep_cols = [("Total","Cmp%"), ("Short","Cmp%"), ("Medium","Cmp%"), ("Long","Cmp%")]
                keep = squad[keep_cols]
                squad.iloc[:,3:] = squad.iloc[:,3:].divide(squad[("Unnamed: 2_level_0","90s")], axis="rows")
                squad[keep_cols] = keep
                keep = vs[keep_cols]
                vs.iloc[:,3:] = vs.iloc[:,3:].divide(vs[("Unnamed: 2_level_0","90s")], axis="rows")
                vs[keep_cols] = keep
            # Get team IDs
            squad = self.add_team_ids(squad, 1, new, 'th') 
            vs = self.add_team_ids(vs, 1, new, 'th')
            return squad, vs
    
    ################################################################################
    def scrape_passing_types(self, year, league, normalize=False, player=False):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        elif year < 2018:
            print("Passing type stats not available from before the 2017/18 season.")
            return -1
        print('Scraping {} {} passing type stats'.format(year, league))
        season = str(year-1)+'-'+str(year)
        url = self.get_season_link(year,league)
        new = url.split('/')
        new = '/'.join(new[:-1]) + '/passing_types/' + new[-1]
        new = new.replace("https","http")
        if player:
            # self.driver.get(new)
            self.get(new)
            if normalize:
                self.normalize_table("//*[@id=\"stats_passing_types_per_match_toggle\"]")
            # get html and scrape table
            html = self.get_html_w_id('stats_passing_types')
            df = pd.read_html(html)[0]
            # drop duplicate header rows and link to match logs
            df = df[df[("Unnamed: 0_level_0","Rk")]!="Rk"].reset_index(drop=True)
            df.drop(
                columns=[("Unnamed: 33_level_0","Matches")],
                inplace=True
            )
            # convert type from str to float
            for col in list(df.columns.get_level_values(0)):
                if 'Unnamed' not in col:
                    df[col] = df[col].astype("float")
            df = self.add_player_ids_and_links(df, new) # get player IDs
            return df
        else:
            df = pd.read_html(new)
            squad = df[0].copy()
            vs = df[1].copy()
            if normalize:
                squad.iloc[:,3:] = squad.iloc[:,3:].divide(squad[("Unnamed: 2_level_0","90s")], axis="rows")
                vs.iloc[:,3:] = vs.iloc[:,3:].divide(vs[("Unnamed: 2_level_0","90s")], axis="rows")
            # Get team IDs
            squad = self.add_team_ids(squad, 1, new, 'th') 
            vs = self.add_team_ids(vs, 1, new, 'th')
            return squad, vs
       
    ################################################################################
    def scrape_goal_shot_creation(self, year, league, normalize=False, player=False):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        elif year < 2018:
            print("Goal and shot creation stats not available from before the 2017/18 season.")
            return -1
        print('Scraping {} {} goal and shot creation stats'.format(year, league))
        season = str(year-1)+'-'+str(year)
        url = self.get_season_link(year,league)
        new = url.split('/')
        new = '/'.join(new[:-1]) + '/gca/' + new[-1]
        new = new.replace("https","http")
        if player:
            # self.driver.get(new)
            self.get(new)
            if normalize:
                self.normalize_table("//*[@id=\"stats_gca_per_match_toggle\"]")
            # get html and scrape table
            html = self.get_html_w_id('stats_gca')
            df = pd.read_html(html)[0]
            # drop duplicate header rows and link to match logs
            df = df[df[("Unnamed: 0_level_0","Rk")]!="Rk"].reset_index(drop=True)
            # df.drop(columns=[("SCA","SCA90"), ("GCA","GCA90")], inplace=True)
            df.drop(columns=["SCA90", "GCA90", "Matches"], level=1, inplace=True)
            # convert type from str to float
            for col in list(df.columns.get_level_values(0)):
                if 'Unnamed' not in col:
                    df[col] = df[col].astype("float")
            df = self.add_player_ids_and_links(df, new) # get player IDs
            return df
        else:
            df = pd.read_html(new)
            squad = df[0].copy()
            vs = df[1].copy()
            squad.drop(columns=[("SCA","SCA90"), ("GCA","GCA90")], inplace=True)
            vs.drop(columns=[("SCA","SCA90"), ("GCA","GCA90")], inplace=True)
            if normalize:
                squad.iloc[:,3:] = squad.iloc[:,3:].divide(squad[("Unnamed: 2_level_0","90s")], axis="rows")
                vs.iloc[:,3:] = vs.iloc[:,3:].divide(vs[("Unnamed: 2_level_0","90s")], axis="rows")
            # Get team IDs
            squad = self.add_team_ids(squad, 1, new, 'th') 
            vs = self.add_team_ids(vs, 1, new, 'th')
            return squad, vs
    
    ################################################################################
    def scrape_defensive(self, year, league, normalize=False, player=False):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        elif year < 2018:
            print("Defensive stats not available from before the 2017/18 season.")
            return -1
        print('Scraping {} {} defending stats'.format(year, league))
        season = str(year-1)+'-'+str(year)
        url = self.get_season_link(year,league)
        new = url.split('/')
        new = '/'.join(new[:-1]) + '/defense/' + new[-1]
        new = new.replace("https","http")
        if player:
            # self.driver.get(new)
            self.get(new)
            if normalize:
                self.normalize_table("//*[@id=\"stats_defense_per_match_toggle\"]")
            # get html and scrape table
            html = self.get_html_w_id('stats_defense')
            df = pd.read_html(html)[0]
            # drop duplicate header rows and link to match logs
            df = df[df[("Unnamed: 0_level_0","Rk")]!="Rk"].reset_index(drop=True)
            df.drop(
                columns=[("Unnamed: 31_level_0","Matches")],
                inplace=True
            )
            # convert type from str to float
            for col in list(df.columns.get_level_values(0)):
                if 'Unnamed' not in col:
                    df[col] = df[col].astype("float")
            df = self.add_player_ids_and_links(df, new) # get player IDs
            return df
        else:
            df = pd.read_html(new)
            squad = df[0].copy()
            vs = df[1].copy()
            if normalize:
                keep_cols = [("Vs Dribbles","Tkl%"), ("Pressures","%")]
                keep = squad[keep_cols]
                squad.iloc[:,3:] = squad.iloc[:,3:].divide(squad[("Unnamed: 2_level_0","90s")], axis="rows")
                squad[keep_cols] = keep
                keep = vs[keep_cols]
                vs.iloc[:,3:] = vs.iloc[:,3:].divide(vs[("Unnamed: 2_level_0","90s")], axis="rows")
                vs[keep_cols] = keep
            # Get team IDs
            squad = self.add_team_ids(squad, 1, new, 'th') 
            vs = self.add_team_ids(vs, 1, new, 'th')
            return squad, vs
    
    ################################################################################
    def scrape_possession(self, year, league, normalize=False, player=False):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        elif year < 2018:
            print("Possession stats not available from before the 2017/18 season.")
            return -1
        print('Scraping {} {} possession stats'.format(year, league))
        season = str(year-1)+'-'+str(year)
        url = self.get_season_link(year,league)
        new = url.split('/')
        new = '/'.join(new[:-1]) + '/possession/' + new[-1]
        new = new.replace("https","http")
        if player:
            # self.driver.get(new)
            self.get(new)
            if normalize:
                self.normalize_table("//*[@id=\"stats_possession_per_match_toggle\"]")
            # get html and scrape table
            html = self.get_html_w_id('stats_possession')
            df = pd.read_html(html)[0]
            # drop duplicate header rows and link to match logs
            df = df[df[("Unnamed: 0_level_0","Rk")]!="Rk"].reset_index(drop=True)
            df.drop(
                columns=[("Unnamed: 32_level_0","Matches")],
                inplace=True
            )
            # convert type from str to float
            for col in list(df.columns.get_level_values(0)):
                if 'Unnamed' not in col:
                    df[col] = df[col].astype("float")
            df = self.add_player_ids_and_links(df, new) # get player IDs
            return df
        else:
            df = pd.read_html(new)
            squad = df[0].copy()
            vs = df[1].copy()
            if normalize:
                keep_cols = [("Dribbles","Succ%"),("Receiving","Rec%")]
                keep = squad[keep_cols]
                squad.iloc[:,4:] = squad.iloc[:,4:].divide(squad[("Unnamed: 3_level_0","90s")], axis="rows")
                squad[keep_cols] = keep
                keep = vs[keep_cols]
                vs.iloc[:,4:] = vs.iloc[:,4:].divide(vs[("Unnamed: 3_level_0","90s")], axis="rows")
                vs[keep_cols] = keep
            # Get team IDs
            squad = self.add_team_ids(squad, 1, new, 'th') 
            vs = self.add_team_ids(vs, 1, new, 'th')
            return squad, vs
    
    ################################################################################
    def scrape_playing_time(self, year, league, normalize=False, player=False):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        print('Scraping {} {} playing time stats'.format(year, league))
        season = str(year-1)+'-'+str(year)
        url = self.get_season_link(year,league)
        new = url.split('/')
        new = '/'.join(new[:-1]) + '/playingtime/' + new[-1]
        new = new.replace("https","http")
        if player:
            # self.driver.get(new)
            self.get(new)
            if normalize:
                self.normalize_table("//*[@id=\"stats_playing_time_per_match_toggle\"]")
            # get html and scrape table
            html = self.get_html_w_id('stats_playing_time')
            df = pd.read_html(html)[0]
            # drop duplicate header rows and link to match logs
            df = df[df[("Unnamed: 0_level_0","Rk")]!="Rk"].reset_index(drop=True)
            df.drop(columns=("Team Success","+/-90"), inplace=True)
            df.drop(columns="Matches", level=1, inplace=True)
            if year >= 2018:
                df.drop(columns="xG+/-90", level=1, inplace=True)
            # convert type from str to float
            for col in list(df.columns.get_level_values(0)):
                if 'Unnamed' not in col:
                    df[col] = df[col].astype("float")
            df = self.add_player_ids_and_links(df, new) # get player IDs
            return df
        else:
            df = pd.read_html(new)
            squad = df[0].copy()
            vs = df[1].copy()
            squad.drop(columns=("Team Success","+/-90"), inplace=True)
            vs.drop(columns=("Team Success","+/-90"), inplace=True)
            if year >= 2018:
                squad.drop(columns=("Team Success (xG)","xG+/-90"), inplace=True)
                vs.drop(columns=("Team Success (xG)","xG+/-90"), inplace=True)
            if normalize:
                keep_cols = [
                    ("Playing Time","Mn/MP"), ("Playing Time","Min%"),
                    ("Playing Time","90s"), ("Starts","Mn/Start")
                ]
                keep = squad[keep_cols]
                squad.iloc[:,4:] = squad.iloc[:,4:].divide(squad[("Playing Time","MP")], axis="rows")
                squad[keep_cols] = keep
                keep = vs[keep_cols]
                vs.iloc[:,4:] = vs.iloc[:,4:].divide(vs[("Playing Time","MP")], axis="rows")
                vs[keep_cols] = keep
            # Get team IDs
            squad = self.add_team_ids(squad, 1, new, 'th') 
            vs = self.add_team_ids(vs, 1, new, 'th')
            return squad, vs
    
    ################################################################################
    def scrape_misc(self, year, league, normalize=False, player=False):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        print('Scraping {} {} miscellaneous stats'.format(year, league))
        season = str(year-1)+'-'+str(year)
        url = self.get_season_link(year,league)
        new = url.split('/')
        new = '/'.join(new[:-1]) + '/misc/' + new[-1]
        new = new.replace("https","http")
        if player:
            # self.driver.get(new)
            self.get(new)
            if normalize:
                self.normalize_table("//*[@id=\"stats_misc_per_match_toggle\"]")
            # get html and scrape table
            html = self.get_html_w_id('stats_misc')
            df = pd.read_html(html)[0]
            # drop duplicate header rows and link to match logs
            df = df[df[("Unnamed: 0_level_0","Rk")]!="Rk"].reset_index(drop=True)
            df.drop(columns="Matches", level=1, inplace=True)
            # convert type from str to float
            for col in list(df.columns.get_level_values(0)):
                if 'Unnamed' not in col:
                    df[col] = df[col].astype("float")
            df = self.add_player_ids_and_links(df, new) # get player IDs
            return df
        else:
            df = pd.read_html(new)
            squad = df[0].copy()
            vs = df[1].copy()
            if normalize:
                if year >= 2018:
                    keep_cols = [("Aerial Duels","Won%")]
                    keep = squad[keep_cols]
                    squad.iloc[:,3:] = squad.iloc[:,3:].divide(squad[("Unnamed: 2_level_0","90s")], axis="rows")
                    squad[keep_cols] = keep
                    keep = vs[keep_cols]
                    vs.iloc[:,3:] = vs.iloc[:,3:].divide(vs[("Unnamed: 2_level_0","90s")], axis="rows")
                    vs[keep_cols] = keep
                else:
                    squad.iloc[:,3:] = squad.iloc[:,3:].divide(squad[("Unnamed: 2_level_0","90s")], axis="rows")
                    vs.iloc[:,3:] = vs.iloc[:,3:].divide(vs[("Unnamed: 2_level_0","90s")], axis="rows")
            # Get team IDs
            squad = self.add_team_ids(squad, 1, new, 'th') 
            vs = self.add_team_ids(vs, 1, new, 'th')
            return squad, vs
        
    ################################################################################
    def scrape_season(self, year, league, normalize=False, player=False):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        if year >= 2018:
            out = {"League Table":         self.scrape_league_table(year,league,normalize),
                   "Standard":             self.scrape_standard(year,league,normalize,player),
                   "Goalkeeping":          self.scrape_gk(year,league,normalize,player),
                   "Advanced Goalkeeping": self.scrape_adv_gk(year,league,normalize,player),
                   "Shooting":             self.scrape_shooting(year,league,normalize,player),
                   "Passing":              self.scrape_passing(year,league,normalize,player),
                   "Pass Types":           self.scrape_passing_types(year,league,normalize,player),
                   "GCA":                  self.scrape_goal_shot_creation(year,league,normalize,player),
                   "Defensive":            self.scrape_defensive(year,league,normalize,player),
                   "Possession":           self.scrape_possession(year,league,normalize,player),
                   "Playing Time":         self.scrape_playing_time(year,league,normalize,player),
                   "Misc":                 self.scrape_misc(year,league,normalize,player)}
        else:
            out = {"League Table":         self.scrape_league_table(year,league,normalize),
                   "Standard":             self.scrape_standard(year,league,normalize,player),
                   "Goalkeeping":          self.scrape_gk(year,league,normalize,player),
                   "Shooting":             self.scrape_shooting(year,league,normalize,player),
                   "Playing Time":         self.scrape_playing_time(year,league,normalize,player),
                   "Misc":                 self.scrape_misc(year,league,normalize,player)}
        return out

    ################################################################################
    def scrape_matches(self, year, league, save=False):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        season = str(year-1)+'-'+str(year)
        links = self.get_match_links(year,league)
        failures = []
        
        # initialize df
        if year >= 2018:
            cols = ['Date','Matchweek','Home Team','Away Team','Home Goals','Away Goals',
                    'Home Ast','Away Ast','FBRef Home xG','FBRef Away xG','FBRef Home npxG',
                    'FBRef Away npxG','FBRef Home xA','FBRef Away xA','FBRef Home psxG',
                    'FBRef Away psxG', 'Home Player Stats', 'Away Player Stats']
        else:
            cols = ['Date','Matchweek','Home Team','Away Team','Home Goals','Away Goals']
        matches = pd.DataFrame(columns=cols)
        
        # scrape match data
        print("Scraping matches.")
        time.sleep(1)
        for link in tqdm(links):
            try:
                match = self.scrape_match(link, year, league)
                matches = matches.append(match, ignore_index=True)
            except Exception as e:
                failures.append([link, e])
            
        # sort df by match date
        matches = matches.sort_values(by='Date').reset_index(drop=True)
            
        # Print out the failed scrapes
        if len(failures) > 0:
            print('Unable to scrape match data from')
            for failure in failures:
                print(failure, '\n')
        
        # save to CSV if requested by user
        if save:
            filename = '{}_{}_FBRef_matches.csv'.format(season, league.replace(' ','_'))
            matches.to_csv(path_or_buf=filename, index=False)
            print('Matches dataframe saved to ' + filename)
            return filename
        else:
            return matches
        
    ################################################################################    
    def scrape_match(self, link, year, league):
        err, valid = check_season(year,league,'FBRef')
        if not valid:
            print(err)
            return -1
        df = pd.read_html(link)
        
        """
        if year < 2016:
            0) cards
            1) home summary
            2) home gk
            3) away summary
            4) away gk
        elif year < 2018:
            0) home lineup
            1) away lineup
            2) team stats (possession, pass acc, sot, saves)
            3) home sumary
            4) home gk
            5) away summary
            6) away gk
        else:
            0) home lineup
            1) away lineup
            2) team stats (possession, pass acc, sot, saves)
            3) home summary
            4) home passing
            5) home pass types
            6) home def actions
            7) home possession
            8) home misc
            9) home gk
            10) away summary
            11) away passing
            12) away pass types
            13) away def actions
            14) away possession
            15) away misc
            16) away gk
            17) list of shots - both teams
            18) list of shots - home team
            19) list of shots - away team
        """
        
        """
        Get date of the match
        """
        league_replace = {"EPL"       : "-Premier-League",
                          "La Liga"   : "-La-Liga",
                          "Bundesliga": "-Bundesliga",
                          "Serie A"   : "-Serie-A",
                          "Ligue 1"   : "-Ligue-1" if year >= 2003 else "-Division-1",
                          "MLS"       : "-Major-League-Soccer",}
        date_elements = link.replace(league_replace[league],"").split("/")[-1].split("-")[-3:]
        date = "-".join(date_elements)
        date = datetime.datetime.strptime(date,'%B-%d-%Y').date()
            
        """
        Get matchweek
        """
        # DEBUG 17 July 2022 httperror 429 too many requests, trying to get retry after value
        try:
            response = requests.get(link)
        except HTTPError:
            print("-")
            print(response.reason)
            print("-")
            return -1
        soup = BeautifulSoup(response.content, "html.parser")
        dom = etree.HTML(str(soup))
        if league == "MLS":
            # 17Jul2022 - MLS stopped putting matchweek number on match pages
            # Fix from @hedonistrh in issue #8
            matchweek = dom.xpath('//*[@id="content"]/div[2]/div[3]/div[2]/text()')[0]\
                           .replace(')','')\
                           .replace('(', '')\
                           .strip()
        else:
            matchweek = int(
                dom.xpath('//*[@id="content"]/div[2]/div[3]/div[2]/text()')[0]\
                   .split('Matchweek')[-1]\
                   .replace(')','')\
                   .strip()
            )

        """
        Begin making match series
        """
        match = pd.Series()
        match['Date'] = str(date)
        match['Matchweek'] = matchweek
        
        """
        Team summary stats and gk stats dataframes
        """
        if year < 2016:
            home_summary_df = df[1]
            home_gk_df      = df[2]
            away_summary_df = df[3]
            away_gk_df      = df[4]
        elif year < 2018:
            home_summary_df = df[3]
            home_gk_df      = df[4]
            away_summary_df = df[5]
            away_gk_df      = df[6]
        else:
            home_summary_df = df[3]
            home_gk_df      = df[9]
            away_summary_df = df[10]
            away_gk_df      = df[16]
            
        """
        Team Names
        """
        if year < 2016:
            home_team = df[0].columns[0][0]
            away_team = df[0].columns[1][0]
        else:
            home_team = df[2].columns[0][0]
            away_team = df[2].columns[1][0]
        match['Home Team'] = home_team
        match['Away Team'] = away_team
            
        """
        Team formations
        """
        if year < 2016:
            pass
        else:
            match["Home Formation"] = df[0].columns[0].split("(")[-1].split(")")[0]
            match["Away Formation"] = df[1].columns[0].split("(")[-1].split(")")[0]
        
        """
        Goals, Assists, and GK stats
        """
        match['Home Goals'] = np.array(home_summary_df[('Performance','Gls')])[-1]
        match['Home Ast']   = np.array(home_summary_df[('Performance','Ast')])[-1]
        match['Away Goals'] = np.array(away_summary_df[('Performance','Gls')])[-1]
        match['Away Ast']   = np.array(away_summary_df[('Performance','Ast')])[-1]
        
        """
        Player stats
        Advanced stats if 2017/18 season or later. Else basic stats.
        """
        if year < 2018:
            match["Home Player Stats"] = pd.Series({"Summary": home_summary_df,
                                                    "GK"     : home_gk_df})
            match["Away Player Stats"] = pd.Series({"Summary": away_summary_df,
                                                    "GK"     : away_gk_df})
        else:
            match["Home Player Stats"] = pd.Series({"Team Sheet": df[0],
                                                    "Summary"   : home_summary_df,
                                                    "Passing"   : df[4],
                                                    "Pass Types": df[5],
                                                    "Defensive" : df[6],
                                                    "Possession": df[7],
                                                    "Misc"      : df[8],
                                                    "GK"        : home_gk_df})
            match["Away Player Stats"] = pd.Series({"Team Sheet": df[1],
                                                    "Summary"   : away_summary_df,
                                                    "Passing"   : df[11],
                                                    "Pass Types": df[12],
                                                    "Defensive" : df[13],
                                                    "Possession": df[14],
                                                    "Misc"      : df[15],
                                                    "GK"        : away_gk_df})
            
            match['FBRef Home xG']   = np.array( df[3][('Expected','xG')])[-1]
            match['FBRef Away xG']   = np.array(df[10][('Expected','xG')])[-1]
            match['FBRef Home npxG'] = np.array( df[3][('Expected','npxG')])[-1]
            match['FBRef Away npxG'] = np.array(df[10][('Expected','npxG')])[-1]
            match['FBRef Home xA']   = np.array( df[3][('Expected','xA')])[-1]
            match['FBRef Away xA']   = np.array(df[10][('Expected','xA')])[-1]
            match['FBRef Home psxG'] = np.array(df[16][('Shot Stopping','PSxG')])[-1]
            match['FBRef Away psxG'] = np.array( df[9][('Shot Stopping','PSxG')])[-1]
            
            # added by @hedonistrh
            match["Shots"] = pd.Series({"Both Team Shots": df[17].loc[~df[17].isna().all(axis=1)], 
                                        "Home Team Shots": df[18].loc[~df[18].isna().all(axis=1)],
                                        "Away Team Shots": df[19].loc[~df[19].isna().all(axis=1)]})
            
        return match
    
    ################################################################################
    def scrape_complete_scouting_reports(self, year, league, goalkeepers=False):
        # Get the player links
        if goalkeepers:
            player_links = self.scrape_gk(year, league, player=True)['player_link']
        else:
            player_links = self.scrape_standard(year, league, player=True)['player_link']
        clear_output()
        
        # initialize dataframes
        per90_df = pd.DataFrame()
        percentiles_df = pd.DataFrame()
        
        # gather complete reports and append to dataframes
        cnt = 0
        for player_link in player_links:
            cnt += 1
            print('{}/{}'.format(cnt, len(player_links)), end='\r')
            _, per90, percentiles = self.complete_report_from_player_link(player_link)
            
            # skip goalkeers or players who don't have a complete report
            if (type(per90) is int) or (type(percentiles) is int) \
                    or not goalkeepers and per90['Position'].values[0]=='Goalkeepers':
                continue
                
            # append
            per90_df = per90_df.append(per90, ignore_index=True)
            percentiles_df = percentiles_df.append(percentiles, ignore_index=True)
        
        return per90_df, percentiles_df
    
    ################################################################################
    def complete_report_from_player_link(self, player_link):
        # return -1 if the player has no scouting report
        player_link_html = urlopen(player_link).read().decode('utf8')
        if 'view complete scouting report' not in player_link_html.lower():
            return -1, -1, -1

        # Get the link to the complete report
        # self.driver.get(player_link)
        self.get(player_link)
        complete_report_button = self.driver.find_element(By.XPATH, 
                                                          '/html/body/div[2]/div[6]/div[2]/div[1]/div/div/div[1]/div/ul/li[2]/a')
        complete_report_link = complete_report_button.get_attribute('href')

        
        # self.driver.get(complete_report_link)
        self.get(complete_report_link)

        # Get the report table
        complete_report = pd.read_html(complete_report_link)[0]
        complete_report.columns = complete_report.columns.get_level_values(1)
        complete_report = pd.concat([pd.DataFrame(data={'Statistic': ['Standard Stats','Statistic'], 
                                                        'Per 90': ['Standard Stats','Per 90'], 
                                                        'Percentile': ['Standard Stats', 'Percentile']}),
                                     complete_report])
        complete_report.dropna(axis=0, inplace=True)
        complete_report.reset_index(inplace=True, drop=True)

        # Get the table section headers and stats to make a multiindex
        header_idxs = [i for i in complete_report.index \
                       if np.all(complete_report.iloc[i,:]==complete_report.iloc[i,0])]
        header_idxs.append(complete_report.shape[0])
        table_headers = list()
        sub_stats = list()
        for i in range(len(header_idxs)-1):
            table_headers.append(complete_report.iloc[header_idxs[i],0])
            table = complete_report.iloc[header_idxs[i]+2:header_idxs[i+1], :].T
            sub_stats.append(list(table.iloc[0,:].values)) # sub stats are in first row
        idx = pd.MultiIndex.from_tuples([(table_headers[i], sub_stats[i][j]) \
                                         for i in range(len(table_headers)) \
                                         for j in range(len(sub_stats[i]))])
        
        # Initiate the dataframes
        per90 = pd.DataFrame(data=-1*np.ones([1,len(idx)]), columns=idx)
        percentiles = pd.DataFrame(data=-1*np.ones([1,len(idx)]), columns=idx)
        
        # Populate the dataframes
        for i in range(len(header_idxs)-1):
            table_header = complete_report.iloc[header_idxs[i],0]
            table = complete_report.iloc[header_idxs[i]+2:header_idxs[i+1], :].T
            table.columns = table.iloc[0,:]
            table = table.reset_index(drop=True).drop(index=0)
            for col in table.columns:
                per90[(table_header,col)] = float(table.loc[1,col].replace('%',''))
                percentiles[(table_header,col)] = int(table.loc[2,col])
        
        # add player names, positions, and minutes played
        player_name = ' '.join(complete_report_link.split('/')[-1].split('-')[:-2])
        player_pos = self.driver.find_element(By.XPATH, '//*[@class="filter switcher"]/div/a').text.replace('vs. ', '')
        minutes = int(self.driver.find_element(By.XPATH, '//*[@class="footer no_hide_long"]/div') \
                .text \
                .split(' minutes')[0] \
                .split(' ')[-1])
        per90['Player'] = player_name
        per90['Position'] = player_pos
        per90['Minutes'] = minutes
        percentiles['Player'] = player_name
        percentiles['Position'] = player_pos
        percentiles['Minutes'] = minutes

        return complete_report, per90, percentiles
        