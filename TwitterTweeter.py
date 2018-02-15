# -*- coding: utf-8 -*-

# Lisätään polku kansioon, missä käytetään koodin toista osaa
import sys
sys.path.append("/home/pi/")
# Lisätään viittaus funkitoon youtube_search()
from YoutubeSearch import youtube_search
import urllib.request, json
# Twitter api
from twython import Twython
# Painonappi
import RPi.GPIO as GPIO
import time, random

# Siirretään vaadittavat tiedot client_sercet tiedostosta
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Määritetään ISO-koodeja youtube data apin hakua varten
regionCode = [
    "FI",
    "RU",
    "US",
    "GB",
    "SE"]
# Ja koodia vastaava valtio
country = [
    "Suomi",
    "Venäjä",
    "Yhdysvallat",
    "Iso-Britannia",
    "Ruotsi"]

while True:
    if GPIO.input(18) == False:
        # Jos kaikki maat on käyty läpi, lopetetaan ohjelma lopputekstillä
        if not regionCode:
            print ("Kaikki maat käyty läpi!")
            sys.exit()
        randomRegion = random.choice(regionCode)      # Valitaan satunnainen koodi regionCode-listasta 
        regionIndex = regionCode.index(randomRegion)  # Tallennetaan satunnaisen koodin indeksi listasta
        countryTag = country[regionIndex]             # Valitaan koodia vastaava valtio country-listasta
        message = ("Tässä trendaavin video maasta {}".format(countryTag))
        query = (" https://www.youtube.com/watch?v="
                 + youtube_search(randomRegion))
        result = message +  query
        twitter.update_status(status=result)          # Suoritetaan twitter päivitys twythonin avulla 
        regionCode.remove(randomRegion)               # Poistetaan molemmista listoista jo käytetty ISO-koodi
        country.remove(countryTag)                    # sekä sitä vastaava valtio (Twitteriin ei saa tietyn ajan sisällä 
        time.sleep(0.2)                               # julkaista kahta samanlaista twiittiä)

