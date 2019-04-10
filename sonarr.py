import os
import sys
import notify

os.chdir(os.path.dirname(sys.argv[0]))
tvdbid = int(os.environ.get('sonarr_series_tvdbid'))
epnum = os.environ.get('sonarr_release_episodenumbers')
title = os.environ.get('sonarr_series_title')

notify.sonarr_notify(tvdbid, title, epnum)
