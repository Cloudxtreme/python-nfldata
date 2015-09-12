#!/usr/env python
# -*- coding: utf-8 -*-
# fantasycalculator_ff_projections.py

from bs4 import BeautifulSoup
import json
import logging
import memcache
import pprint
import re
from urllib2 import Request, urlopen, URLError, HTTPError

def get(url):

    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    content = mc.get(url)

    if not content:
        try:
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'
            headers = { 'User-Agent' : user_agent }
            req = Request(url=url, data=None, headers=headers)
            response = urlopen(req)
            content = response.read()
            logging.debug('successfully got %s' % url)
            mc.set(url, content)
                
        except HTTPError as e:
            logging.error('Error code: ', e.code)

        except URLError as e:
            logging.error('Reason: ', e.reason)

        except Exception as e:
            logging.error(e)

    else:
        logging.debug("got %s from cache" % url)

    return content


def parse_row(row):

    player = {}
    
    # get the player name / id
    link = row.find("a", {"class": "flexpop"})
    player['id'] = link.get('playerid')
    player['name'] = link.string

    # get the player position / team (, Phi WR)
    position_team_string = link.nextSibling.string
    position_team_string = re.sub('\s?,\s+', '', position_team_string)
    
    if 'D/ST' in position_team_string:
        player['position'] = 'DST'
           
    else:
        try:
            player_team, player_position = position_team_string.split()
            player['team'] = re.sub('\s+', '', player_team)
            player['position'] = re.sub('\s+', '', player_position)
    
        except Exception as e:
            logging.error("position_team_string error: %s" % e)

    # now get the projected points
    player['fpts'] = row.find("td", {"class": "appliedPoints"}).string

    return player

def parse_page(content):

    players = []
    soup = BeautifulSoup(content)

    table = soup.find('table', {'cellpadding': '2', 'border': '0', 'cellspacing': '1'})

    # headers
    header_row = table.find('tr', class_='tablehdr')
    headers = [td.string for td in header_row]
    logging.debug(headers)

    # players - use regular expression to include header row (which has no class)
    #for row in table.findAll('tr', {'class': re.compile(r'\w+')}):
    #    logging.debug(row)
    #    tds = [td.string for td in row.findAll("td")]
    #    players.append(dict(zip(headers, tds)))

    return players
    
def save_to_file(fn, data):
    with open(fn, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)

def urls():
    return [
        'http://www.fftoday.com/rankings/playerproj.php?Season=2015&PosID=10&LeagueID=26955',
        'http://www.fftoday.com/rankings/playerproj.php?Season=2015&PosID=20&LeagueID=26955',
        'http://www.fftoday.com/rankings/playerproj.php?Season=2015&PosID=30&LeagueID=26955',
        'http://www.fftoday.com/rankings/playerproj.php?Season=2015&PosID=40&LeagueID=26955',
        'http://www.fftoday.com/rankings/playerproj.php?Season=2015&PosID=99&LeagueID=26955',
    ]
    
if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    players = []

    for url in urls():
        content = get(url)
        players = players + parse_page(content)

    save_to_file('fftoday_nfl_projections.json', players)
    
