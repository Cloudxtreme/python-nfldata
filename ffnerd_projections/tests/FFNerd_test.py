import json
import logging
import os
import pprint

from ffnerd_projections.FFNerdNFLScraper import FFNerdNFLScraper
from ffnerd_projections.FFNerdNFLParser import FFNerdNFLParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
api_key = os.environ.get('FFNERD_API_KEY')

if api_key:
    s = FFNerdNFLScraper(api_key=api_key)
    logging.debug(dir(s))
    content = s.get_projections()
    logging.debug(json.dumps(content, indent=4, sort_keys=True))
    p = FFNerdNFLParser()
    players = p.projections(content=content)
    pprint.pprint(players, indent=4)