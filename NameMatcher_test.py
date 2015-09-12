'''
NameMatcher_test.py
Uses names from xml file as reference point
Then uses NameMatcher class to update list of players with a site_id (such as espn_id)
Seems to work in the vast majority of cases
Uses subprocess so I can just run the scripts I have already written, which dump JSON to stdout
'''

import json
import logging
from subprocess import check_call, STDOUT
from tempfile import NamedTemporaryFile

from myfantasyleague_projections.MyFantasyLeagueNFLParser import MyFantasyLeagueNFLParser
import NameMatcher

logging.basicConfig(filename='namematcher.log', level=logging.DEBUG)

commands = {
    #'fpros': 'python $HOME/workspace/python-nfl-projections/fantasypros_ff_projections.py',
    #'ffcalc': 'python $HOME/workspace/python-nfl-projections/ffcalculator_ff_projections.py',
    'ffnerd': r'ffnerd-projections',

}

def run_command(command):
    '''

    :param command (str): the command you want to run
    :return result (str): the output of the command you ran
    '''
    # http://stackoverflow.com/questions/13835055/python-subprocess-check-output-much-slower-then-call
    with NamedTemporaryFile() as f:
        check_call([command], stdout=f, stderr=STDOUT)
        f.seek(0)
        result = f.read()

    return result

def main():

    p = MyFantasyLeagueNFLParser()
    matched_players = []
    unmatched_players = []

    # MyFantasyLeagueNFLParser.players returns a list of dictionaries
    # Easier to do name matching if transform to dictionary where full_name is key, player is value
    fname = 'myfantasyleague_projections/players.xml'
    positions = ['QB', 'RB', 'WR', 'TE']
    players_match_from = {player['full_name']: player for player in p.players(positions=positions, fname=fname)}

    # now get players from other sites
    for site, command in commands.items():

        result = run_command(command)

        try:
            players_to_match = json.loads(result)

            for player in players_to_match:

                try:
                    full_name, first_last = NameMatcher.fix_name(player['full_name'])
                    player['full_name'] = full_name
                    player['first_last'] = first_last
                    player = NameMatcher.match_player(to_match=player, match_from=players_match_from, site_id_key='espn_id')

                    if player.get('espn_id') is not None:
                        matched_players.append(player)
                    else:
                        unmatched_players.append(player)

                except Exception as ie:
                    logging.exception('%s: threw inner exception' % player['full_name'])

        except Exception as e:
            logging.exception('%s: threw outer exception')

    print json.dumps(matched_players, indent=4, sort_keys=True)
    # unmatched_heading = '\n\n****** UNMATCHED PLAYERS ******\n\n'
    # print '{0} {1}'.format(unmatched_heading, json.dumps(unmatched_players, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()