'''
NFLDotComScraper

'''

from bs4 import BeautifulSoup
import json
import logging
import re
import urllib2

from EWTScraper import EWTScraper


class NFLDotComScraper(EWTScraper):
    '''

    '''

    def __init__(self, **kwargs):
        # see http://stackoverflow.com/questions/8134444
        EWTScraper.__init__(self, **kwargs)

        self.game_ids = []
        self.logger = logging.getLogger(__name__).addHandler(logging.NullHandler())

    def all_game_ids():
        starting_season = 2001
        ending_season = 2014
        
        for season in range(season_start, season_end + 1):
            self.week_pages(season)

    def _gamecenter(self, game_id):
        
        url = 'http://www.nfl.com/liveupdate/game-center/{0}/{0}_gtd.json'.format(game_id)
        return self.get(url)
    
    def _week_page(url):
        game_ids = []
        content = self.get(url)
        match = re.search(r'http://www.nfl.com/scores/(\d+)/(REG\d)+', url)
        
        if match:
            fname = match.group(1) + '_' + match.group(2) + '.html'
            self._to_file(fname)

        soup = BeautifulSoup(content)

        for a in soup.findAll('a', class_='game-center-link'):
            # <a href="/gamecenter/2014090400/2014/REG1/packers@seahawks" class="game-center-link" . . . </a>
            game_url = a['href']
            pattern = re.compile(r'/gamecenter/(\d+)/(\d+)/REG')
    
            match = re.search(pattern, game_url)       
            
            if match:
                game_ids.append(match.group(1))
    
        return game_ids
    
    def week_pages(self, season, start_week=None, end_week=None):

        base_url = 'http://www.nfl.com/scores/2014/REG'
        
        if start_week and end_week:
            weeks = range(start_week, end_week + 1)
        elif start_week:
            weeks = range(start_week, 18)
        elif end_week:
            weeks = range(1, end_week + 1)
        else:
            weeks = range(1, 18)

        for week in weeks:
            url = base_url + str(week)
            game_ids = self._week_page(url)
            self.game_ids.append(game_ids)
          
        return self.game_ids

if __name__ == "__main__":
    s = NFLDotComScraper()
    starting_season = 2001
    ending_season = 2014
        
    for season in range(season_start, season_end + 1):
        s.week_pages(season)

    with open('game_ids.json', 'w') as outfile:
        json.dump(self.game_ids, outfile, indent=4, sort_keys=True)

