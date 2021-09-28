import copy
import json
import urllib2

from armagomen.constants import HEADERS
from armagomen.utils.common import logWarning

URL = "https://api.worldoftanks.ru/wot/account/info/?"
API_KEY = "application_id=2a7b45c57d9197bfa7fcb0e342673292&account_id="
STAT_URL = "{url}{key}{ids}&extra=statistics.random&fields=statistics.random&" \
           "language=en".format(url=URL, key=API_KEY, ids="{ids}")
WTR = "{url}{key}{ids}&fields=global_rating&language=en".format(url=URL, key=API_KEY, ids="{ids}")
SEPARATOR = "%2C+"
CACHE = {}
WTR_CACHE = {}


def urlResponse(apiUrl):
    try:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), urllib2.HTTPRedirectHandler())
        opener.addheaders = HEADERS
        response = opener.open(apiUrl)
    except urllib2.URLError:
        logWarning("Technical problems with the server, please inform the developer.")
    else:
        return json.load(response)


def getCachedStatisticData(databaseIDS, update=True):
    databaseIDS = [databaseID for databaseID in databaseIDS if databaseID not in CACHE]
    if not update or not databaseIDS:
        return CACHE
    result = urlResponse(STAT_URL.format(ids=SEPARATOR.join(databaseIDS)))
    if not result:
        return CACHE
    data = result.get("data")
    if data:
        for databaseID in databaseIDS:
            CACHE[databaseID] = copy.deepcopy(data[str(databaseID)]["statistics"]["random"])
    return CACHE


def getStatisticData(databaseIDS):
    result = urlResponse(STAT_URL.format(ids=SEPARATOR.join(databaseIDS)))
    if not result:
        return {}
    data = result.get("data")
    if data:
        return {databaseID: data[str(databaseID)]["statistics"]["random"] for databaseID in databaseIDS}


def getCachedWTR(databaseIDS, update=True):
    databaseIDS = [databaseID for databaseID in databaseIDS if databaseID not in CACHE]
    if not update or not databaseIDS:
        return WTR_CACHE
    result = urlResponse(WTR.format(ids=SEPARATOR.join(databaseIDS)))
    if not result:
        return WTR_CACHE
    data = result.get("data")
    if data:
        for databaseID, value in data:
            WTR_CACHE[int(databaseID)] = value["global_rating"]
    return WTR_CACHE


def getWTRRating(databaseIDS):
    result = urlResponse(WTR.format(ids=SEPARATOR.join(databaseIDS)))
    data = result.get("data")
    if data:
        return {int(databaseID): value["global_rating"] for databaseID, value in data}