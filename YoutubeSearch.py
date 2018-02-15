# -*- coding: utf-8 -*-

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "AIzaSyC7LUGtNke_tq3nmFDXLs1tqHtGcfkFnao"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"



def youtube_search(mRegion) :
    
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # https://developers.google.com/youtube/v3/docs/videos/list
    # Käytetään videos().list() parametreja
    search_response = youtube.videos().list(
        part="snippet",
        chart="mostPopular",
        regionCode=mRegion).execute()

    # Ilman looppia tallennetaan vain ensimmäinen osuma (suosituin video)
    # siltikin kyseessä on array, joten id täytyy hakea kohdasta [0]
    mostPopularInfo = search_response.get("items", [])
    theMostPopular = mostPopularInfo[0]["id"]
    return theMostPopular

