# TODO 1: ADD TYPE HINTS
# TODO 2: ADD tests for all functions


##############################################################################################
##      This Bot Will Log you to 1337.ma as soon as any tweet pushed about piscine          ##
##      To setup this bot you need first to get a twitterAPI v2 Bearer Token                ##
##      create a .credential folder                                                         ##
##      inside the .credentials/ create a json file with "credential.json" as a name        ##
##      Inside credential.json                                                              ##
##      {                                                                                   ##
##        "Bearer": "paste your twitter bearer here",                                       ##
##        "email": "email@example.com",                                                     ##
##        "password": "this is a password"                                                  ##
##      }                                                                                   ##
##############################################################################################

import json
import os
from threading import Thread
from time import sleep
from typing import Dict

import requests
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CREDS = "/home/redone/Projects/Personal/1337BOT/.credentials/credential.json"
LAST_TWEET = "/home/redone/Projects/Personal/1337BOT/last_tweet.txt"
SOUND = "/home/redone/Projects/Personal/1337BOT/assets/audio.mp3"

KEYWORDS = [
    "http://candidature.1337.ma",
    "pool",
    "open",
    "dates",
    "inscription",
    "piscine",
    "ouvert",
    "مسبح",
    "بول",
    "ترشيح",
    "بيسين",
    "choisissez",
]


def get_credentials() -> Dict:
    with open(CREDS, "r", encoding="utf-8") as f:
        return json.load(f)


def get_all_tweets() -> Dict:
    # the second url is just a dummy twitter account for testing!
    url = "https://api.twitter.com/2/tweets/search/recent?query=from:1337FIL"
    # url = "https://api.twitter.com/2/tweets/search/recent?query=from:underm18"
    bearer = get_credentials()["Bearer"]
    headers = {
        "Authorization": f"Bearer {bearer}",
    }
    try:
        all_tweets = requests.get(url, headers=headers).json()
    except ConnectionError as e:
        print(e)
        sleep(300)
        get_all_tweets()
    else:
        return all_tweets


def is_keyword_in_last_tweet(tweets: dict = None) -> bool:
    last_tweet = get_all_tweets()["data"][0]["text"].lower()
    tweet = last_tweet if tweets is None else tweets
    return any([True if key.lower() in tweet.lower() else False for key in KEYWORDS])


def open_browser():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.binary_location = "/usr/bin/brave"
    chrome_options.add_argument("--kiosk")  # To open Brave in Full Screen
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://candidature.1337.ma/users/sign_in")
    driver.find_element(By.ID, "user_email").send_keys(get_credentials()["email"])
    driver.find_element(By.ID, "user_password").send_keys(get_credentials()["password"])
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "div a.cc-btn.cc-allow",
            )
        )
    ).click()

    driver.find_element(By.XPATH, '//*[@id="new_user"]/div[2]/div[3]/input').click()


def alert_sound():
    os.system("pactl set-sink-volume 0 +500%")
    [playsound(SOUND) for _ in range(10)]


def alert_script():
    [print("\033[91mGO GO GOOOO GO GO GOOOO!!\033[00m") for _ in range(10)]


def trigger_alert():
    alert_script()
    Thread(target=open_browser).start()
    Thread(target=alert_sound).start()


def keep_searching():
    sleep(10)
    os.system("clear")


def main():
    os.system("clear")
    while True:
        if is_keyword_in_last_tweet():
            trigger_alert()
            break
        else:
            print("Nothing Found Yet!")
            keep_searching()


if __name__ == "__main__":
    main()
