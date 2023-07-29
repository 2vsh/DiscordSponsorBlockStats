import os
import requests
import json
import configparser
import time
import random

# Configuration handling
CONFIG_FILE = "SponsorStats.txt"

def create_default_config():
    """
    Create a default configuration file with comments.
    """
    config = configparser.ConfigParser()

    config["Logging"] = {
        "# Enable or disable logging of stats. Set to True to enable and False to disable.": "",
        "enablelogging": "True"
    }

    config["SponsorBlock"] = {
        "# This is the ID associated with your SponsorBlock account.": "",
        "userid": "<Your_User_ID>",
        "# The base API endpoint for SponsorBlock. You probably don't need to modify this.": "",
        "# WARNING: Making requests too frequently can lead to being rate-limited or banned.": "",
        "base_url": "https://sponsor.ajay.app/api"
    }

    config["Discord"] = {
        "# Your Discord token. Keep this secret! This is not sent to any server and is kept locally.": "",
        "# If you don't know how to get your token, watch this video: https://www.youtube.com/watch?v=9XJt6EbZWPU": "",
        "token": "<Your_Discord_Token>",
        "# Set to 'mainbio' to update the main account bio; which is good for users who don't have Nitro.": "",
        "# Set to 'specificserver' to update the bio for a specific server (Nitro required)": "",
        "biosetting": "mainbio",
        "# The server ID for the specific server bio update. Defaults to the SponsorBlock server.": "",
        "guildid": "603643120093233162"
    }

    config["Settings"] = {
        "# Time interval (in minutes) after which the program should update the Discord bio.": "",
        "# WARNING: Do not set this too low to avoid spamming requests to Discord and SponsorBlock.": "",
        "# Excessive requests can lead to being rate-limited or banned.": "",
        "# Default is 720 minutes (12 hours).": "",
        "updateinterval": "720",
        "# A random delay (in minutes) that will be added to the update interval to vary the bio update timings.": "",
        "# Default is 60 minutes.": "",
        "randomdelay": "60"
    }

    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)





if not os.path.exists(CONFIG_FILE):
    create_default_config()
    print("No configuration file detected. A default one has been created named 'SponsorStats.txt'. Please edit it with your settings before running the script again.")
    input("Press Enter to close...")
    exit()

def read_config():
    """
    Read the configuration file and return the settings.
    """
    config = configparser.ConfigParser()
    config.optionxform = str  # Preserve the original casing of keys
    config.read(CONFIG_FILE)
    
    sponsorblock_settings = dict(config["SponsorBlock"])
    discord_settings = dict(config["Discord"])
    app_settings = dict(config["Settings"])
    logging_settings = dict(config["Logging"])

    return sponsorblock_settings, discord_settings, app_settings, logging_settings


# Fetch user information
def fetch_user_info(user_id):
    response = requests.get(f"{sponsorblock_settings['base_url']}/userInfo", params={"publicUserID": user_id})
    response.raise_for_status()
    return response.json()

# Corrected bio generation function using provided user_info data
def generate_final_bio(user_info):
    hours_saved_others = user_info['minutesSaved'] / 60
    segments_submitted = user_info['segmentCount']
    segments_saved_others = user_info['viewCount']
    bio = (f"🕒 Saved people from {segments_saved_others} segments (equating to {hours_saved_others:.2f} hours) "
           f"thanks to {segments_submitted} submissions.")
    return bio

def set_discord_bio(token, bio, bio_setting, guild_id=None):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    data = json.dumps({'bio': bio})

    if bio_setting == 'mainbio':
        response = requests.patch('https://discord.com/api/v10/users/@me', headers=headers, data=data)
    elif bio_setting == 'specificserver' and guild_id:
        url = f'https://discord.com/api/v10/guilds/{guild_id}/profile/@me'
        response = requests.patch(url, headers=headers, data=data)
    else:
        print("Invalid setting or missing Guild ID.")
        return

    if response.status_code == 200:
        print("Bio updated successfully!")
    else:
        print(f"Failed to update bio. Response: {response.text}")

    print(response.content)

def log_stats(bio):
    """
    Log the bio stats to a log.txt file.
    """
    with open('log.txt', 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {bio}\n")

while True: #Loop updates
    user_info_data = fetch_user_info(sponsorblock_settings['userid'])
    bio = generate_final_bio(user_info_data)
    print(bio)
    set_discord_bio(discord_settings['token'], bio, discord_settings['biosetting'], discord_settings['guildid'])

    if logging_settings['enablelogging'] == 'True':
        log_stats(bio) # for logging

    sleep_duration = int(app_settings['updateinterval']) * 60  # Convert minutes to seconds
    random_delay = random.randint(0, int(app_settings['randomdelay']) * 60)  # Convert minutes to seconds
    print(f"Sleeping for {sleep_duration + random_delay} seconds before the next update.")
    time.sleep(sleep_duration + random_delay)
