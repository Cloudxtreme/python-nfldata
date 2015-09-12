'''
ESPNNFLScraper

'''

from EWTScraper import EWTScraper
import logging


class ESPNNFLScraper(EWTScraper):
    '''

    '''

    def __init__(self, **kwargs):
        # see http://stackoverflow.com/questions/8134444
        EWTScraper.__init__(self, **kwargs)

        if 'logger' in kwargs:
            self.logger = kwargs['logger']
        else:
            self.logger = logging.getLogger(__name__) \
                .addHandler(logging.NullHandler())

        if 'maxindex' in kwargs:
            self.maxindex = kwargs['maxindex']
        else:
            self.maxindex = 400

        if 'projection_urls' in 'kwargs':
            self.projection_urls = kwargs['projection_urls']
        else:
            base_url = 'http://games.espn.go.com/ffl/tools/projections?'
            idx = [0, 40, 80, 120, 160, 200, 240, 280, 320, 360]
            self.projection_urls = [base_url + 'startIndex=' + x for x in idx]

    def get_projections(self, subset=None):
        pages = []
        if subset:
            for idx in subset:
                content = self.get(self.projection_urls[idx])
                pages.append(content)
        else:
            for url in self.projection_urls:
                content = self.get(url)
                pages.append(content)

        return pages

if __name__ == "__main__":
    pass
