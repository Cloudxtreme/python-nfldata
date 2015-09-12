# -*- coding: utf-8 -*-

import logging
import pprint
import xlrd

from NFLProjectionsParser import NFLProjectionsParser

import NameMatcher

class FootballOutsidersNFLParser(NFLProjectionsParser):

    '''
    Parses xls file of fantasy projections from footballoutsiders.com into player dictionaries

    Example:
        p = FootballOutsidersNFLParser(projections_file='KUBIAK.xls')
        players = p.projections()
    '''

    def __init__(self, projections_file, **kwargs):
        '''
        Args:
            projections_file(str)
            **kwargs: wanted_sheets(list of str): the sheets in the workbook you want to scrape
        '''

        self.projections_file = projections_file

        if 'wanted_cols' in 'kwargs':
            self.wanted_cols = kwargs['wanted_cols']
        else:
            self.wanted_cols = ['player', 'team', 'bye', 'pos', 'age', 'risk', 'dynamic fantasy points', 'position rank', 'auction value']

        if 'wanted_sheets' in 'kwargs':
            self.wanted_sheets = kwargs['wanted_sheets']
        else:
            self.wanted_sheets = ['2015 KUBIAK Projections']

    def _is_not_def(self, val):
        '''
        Exclude players of position IDP
        :param val:
        :return boolean:
        '''

        if val.lower() == 'd':
            return False
        else:
            return True

    def _is_not_idp(self, val):
        '''
        Exclude players of position IDP
        :param val:
        :return boolean:
        '''

        if 'IDP' in val:
            return False
        else:
            return True

    def _is_not_kicker(self, val):
        '''
        Exclude players of position IDP
        :param val:
        :return boolean:
        '''

        if val.lower() == 'k':
            return False
        else:
            return True

    def _parse_row(self, sheet, rowidx, column_map):
        '''
        Private method  
        :param sheet(xlrd worksheet object):
        :return players (list of dictionary):
        '''

        cells = []

        # loop through list of columns you want to scrape
        for column in self.wanted_cols:
            colidx = column_map.get(column, None)

            if colidx is not None:
                cell_value = str(sheet.cell(rowidx,colidx).value)
                cells.append(cell_value)
            else:
                logging.error('could not find column index for %s' % column)

        fixed_column_names = self._fix_headers(self.wanted_cols)
        player = dict(zip(fixed_column_names, cells))
        first_last, full_name = NameMatcher.fix_name(player['full_name'])
        player['first_last'] = first_last
        player['full_name'] = full_name
        logging.debug('player is %s' % player)
        return player

    def _parse_sheet(self, sheet):
        '''
        Private method  
        :param sheet(xlrd worksheet object):
        :return players (list of dictionary):
        '''

        players = []

        # get the column_map, key is name and value is index
        column_map = self._column_map(sheet)

        for rowidx in range(1, sheet.nrows):

            position_colidx = column_map.get('pos', None)
            position = str(sheet.cell(rowidx, position_colidx).value)

            if position_colidx:
                if self._is_not_idp(position) and self._is_not_kicker(position) and self._is_not_def(position):
                    player = self._parse_row(sheet=sheet, rowidx=rowidx, column_map=column_map)
                    players.append(player)
                else:
                    logging.debug('skipped %s' % position)
            else:
                logging.error('no position_colidx')

        return players

    def projections(self):
        '''

        :return players(list of dictionary): player dictionaries
        '''

        wb = xlrd.open_workbook(self.projections_file)

        players = []

        for sheet in wb.sheets():
            if sheet.name in self.wanted_sheets:
                players = players + self._parse_sheet(sheet)

        return players


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    p = FootballOutsidersNFLParser()
    logging.debug(p)
