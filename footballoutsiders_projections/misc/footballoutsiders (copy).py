#!/usr/env python

import requests

if __name__ == '__main__':

    s = requests.Session()

    values = {
        'name': 'eric.truett@gmail.com',
        'pass': 'cft0911'
    }

    login_url = 'http://www.footballoutsiders.com/frontpage?destination=frontpage'
    r = requests.post(login_url, data=values)
    download_url = 'http://www.footballoutsiders.com/store/myfiles/76159/download?file=KUBIAK2015.zip'
    local_filename = 'KUBIAK2015.zip'
    r = requests.get(download_url, stream=True)

    if r.status_code == 200:
        with open(local_filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)

    #with open(local_filename, 'wb') as f:
    #    for chunk in r.iter_content(chunk_size=1024):
    #        if chunk:
    #            f.write(chunk)
    #            f.flush()
