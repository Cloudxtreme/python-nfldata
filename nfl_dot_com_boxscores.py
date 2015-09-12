# nfl_dot_com_boxscores.py

from bs4 import BeautifulSoup
import re
import urllib2
from urlparse import urljoin

def gamecenter_page(game_id):
    
    #http://www.nfl.com/liveupdate/game-center/2014090400/2014090400_gtd.json

    response = urllib2.urlopen(url)
    content = response.read()
    soup = BeautifulSoup(content)
    
def weekly_boxscore_page(start_week, end_week):

    base_url = 'http://www.nfl.com/scores/2014/REG'
    weeks = range(start_week, end_week + 1)
    game_ids = []

    for week in weeks:
        url = base_url + str(week)
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)

        for a in soup.findAll('a', class_='game-center-link'):
            # <a href="/gamecenter/2014090400/2014/REG1/packers@seahawks" class="game-center-link" . . . </a>
            game_url = a['href']
            pattern = re.compile(r'/gamecenter/(\d+)/(\d+)/REG')
    
            match = re.search(pattern, game_url)       
            if match:
                game_ids.append(match.group(1))
      
    return game_ids

if __name__ == '__main__':
    
    print weekly_boxscore_page(1, 2)
