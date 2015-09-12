# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import logging
import re

from NFLProjectionsParser import NFLProjectionsParser

class ESPNNFLParser(NFLProjectionsParser):

    def __init__(self, **kwargs):

        NFLProjectionsParser.__init__(self, **kwargs)

        if 'logger' in kwargs:
            self.logger = kwargs['logger']
        else:
            self.logger = logging.getLogger(__name__) \
                .addHandler(logging.NullHandler())

    def _parse_row(self, row):
        '''
        Parses <tr> element into key-value pairs
        :param row(str): html <tr> element
        :return player(dict):
        '''
        player = {}

        # get the player name / id
        link = row.find("a", {"class": "flexpop"})
        player['espn_id'] = link.get('playerid')
        player['full_name'] = link.string

        # get the player position / team (, Phi WR)
        pos_tm_string = link.nextSibling.string
        pos_tm_string = re.sub(r'\s?,\s+', '', pos_tm_string).strip()
        logging.debug('position team string is %s', pos_tm_string)

        if 'D/ST' in pos_tm_string:
            player['position'] = 'DST'
            player['team'] = self._fix_team_code(link.string.split()[0])
            player['full_name'] = '{0}_DST'.format(player['team'])
            player['injury'] = False

        else:
            try:
                if '*' in pos_tm_string:
                    player['injury'] = True
                    pos_tm_string = player['full_name'].replace('*', '')

                else:
                    player['injury'] = False

                player_team, player_position = pos_tm_string.split()
                player['team'] = re.sub(r'\s+', '', player_team)
                player['position'] = re.sub(r'\s+', '', player_position)

            except ValueError:
                self.logger.exception("pos_tm_string error")

        # now get the projected points
        fantasy_points = row.find("td", {"class": "appliedPoints"}).string
        if '--' in fantasy_points:
            player['fantasy_points'] = 0
        else:
            player['fantasy_points'] = fantasy_points

        return player

    def projections(self, content):
        '''
        Takes HTML, returns list of player dictionaries
        :param content: html page of projections
        :return rows(list): player dictionaries
        '''

        rows = []
        soup = BeautifulSoup(content)

        for row in soup.findAll("tr", {"class": "pncPlayerRow"}):
            player = self._parse_row(row)
            rows.append(player)

        return rows

if __name__ == "__main__":
    pass