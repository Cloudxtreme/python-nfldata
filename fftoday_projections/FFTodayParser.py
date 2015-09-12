# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import logging
import re

from NFLProjectionsParser import NFLProjectionsParser


class FFTodayParser(NFLProjectionsParser):
    '''
    Parses html of NFL fantasy projections page of fantasyfootballtoday.com into player dictionaries

    Example:
        p = FFTodayParser()
        players = p.projections(content)
    '''

    def __init__(self,**kwargs):
        '''
        Args:
            **kwargs: logger (logging.Logger)
        '''

        if 'logger' in kwargs:
          self.logger = kwargs['logger']
        else:
          self.logger = logging.getLogger(__name__)


    def _parse_dst_row(self, row):

        player = {}

        # headers goofy to parse, so hardcode them here, plus don't need all data
        # headers = ['player_id', 'full_name', 'team', 'bye', 'fpts']

        # get the player name / id that is in the url of the 'a' element
        link = row.find('a')

        if link:
            url_pattern = re.compile(r'/stats/players\?TeamID\=(\d+)')
            m = re.search(url_pattern, link.get('href'))
        else:
            logging.debug('could not find link in %s' % row.prettify())

        if m:
            player['fftoday_id'] = m.group(1)
            player['full_name'] = self._fix_team_code(link.string)

        # I want the 3rd and last <td class=sort1 align=center>
        tds = row.findAll('td', {'class': 'sort1', 'align': 'center'})

        bye_td = tds[1]
        player['bye'] = bye_td.string

        fpts_td = tds[-1]
        player['fantasy_points'] = fpts_td.string

        return player

    def _parse_row(self, row):
        player = {}  
    
        # headers goofy to parse, so hardcode them here, plus don't need all data
        # headers = ['player_id', 'full_name', 'team', 'bye', 'fpts']
                
        # get the player name / id that is in the url of the 'a' element
        link = row.find('a')

        if link:
            url_pattern = re.compile(r'/stats/players/(.*?)/(.*?)\?')
            m = re.search(url_pattern, link.get('href'))
        else:
            logging.debug('could not find link in %s' % row.prettify())

        if m:
            player['fftoday_id'] = m.group(1)
            player['full_name'] = m.group(2).replace("_", " ")

        # I want the 2nd, 3rd, and last <td class=sort1 align=center>
        tds = row.findAll('td', {'class': 'sort1', 'align': 'center'})       

        team_td = tds[1]
        player['team'] = team_td.string

        bye_td = tds[2]
        player['bye'] = bye_td.string

        fpts_td = tds[-1]
        player['fantasy_points'] = fpts_td.string

        return player

    def _parse_page(self, content, position):
        players = []
        soup = BeautifulSoup(content)

        table = soup.find('table', {'cellpadding': '2', 'border': '0', 'cellspacing': '1'})

        if position == 'dst':
            for tr in table.findAll('tr', attrs={'class': None}):
                player = self._parse_dst_row(tr)
                player['position'] = 'dst'
                players.append(player)

        else:
            for tr in table.findAll('tr', attrs={'class': None}):
                player = self._parse_row(tr)
                player['position'] = position
                players.append(player)
        
        return players


    def fix_header(self, header):
        '''
        Looks at global list of headers, can provide extras locally
        :param headers:
        :return:
        '''

        fixed = {
        }

        # return fixed.get(header, header)
        fixed_header = self._fix_header(header)
        logging.debug('parser._fix_header fixed header')
        logging.debug(fixed_header)

        # fixed_header none if not found, so use local list
        if not fixed_header:
            return fixed.get(header, header)

        else:
            return fixed_header


    def fix_headers(self, headers):
        '''

        :param headers:
        :return:
        '''
        return [self.fix_header(header) for header in headers]


    def projections (self, content):
        '''
        Parses all pages, which have rows of html table using BeautifulSoup and returns list of player dictionaries
        Args:
            content (dictionary): keys are positions, values are list of html pages
        Returns:
            List of dictionaries if successful, empty list otherwise.
        '''

        players = []

        for position, pages in content.items():

            for page in pages:
                parsed = self._parse_page(page, position)
            
                if parsed:
                    players = players + parsed

        return players

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    p = FFTodayParser()
    logging.debug(dir(p))
