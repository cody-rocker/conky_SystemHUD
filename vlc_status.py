#!/usr/bin/env python
import sys
import urllib2
import base64
import json
import keyring

VLC_STATUS = 'http://localhost:8080/requests/status.json'


def get_status():
    """ return json object with current vlc status info """
    # request status from vlc http server
    req = urllib2.Request(VLC_STATUS)
    # build authentication header
    password = keyring.get_password('vlc_status', 'conky')
    base64string = base64.encodestring('%s:%s' % ('', password))[:-1]
    password = None
    authheader = "Basic %s" % base64string
    # add encoded header to request
    req.add_header("Authorization", authheader)
    try:
        handle = urllib2.urlopen(req)
    except IOError as e:
        sys.exit(1)
    source = handle.read()
    json_data = json.loads(source)

    return json_data


def extract_data(json_obj):
    meta = {}
    if json_obj['state'] == 'playing':
        meta['artist'] = json_obj['information']['category']['meta']['artist']
        meta['title'] = json_obj['information']['category']['meta']['title']
        # Soundcloud meta
        # meta['genre'] = json_obj['information']['category']['meta']['genre']
        # meta['art'] = json_obj['information']['category']['meta']['url']
    else:
        return None
    return meta



json_obj = get_status()
now_playing = extract_data(json_obj)
if now_playing is not None:
    print ('{artist} - {title}'.format(
        artist=now_playing['artist'], title=now_playing['title']))
else:
    print('')

## Dump json response to console
# print json.dumps(get_status(), indent=4)