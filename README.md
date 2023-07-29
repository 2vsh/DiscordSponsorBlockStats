# DiscordSponsorBlockStats
Synchronize your SponsorBlock contributions to your Discord about me / server bio. Showcase your ad-skipping stats and stay updated effortlessly.

## Overview

This tool is designed for active [SponsorBlock](https://sponsor.ajay.app/) contributors who wish to automatically update their Discord bios with their latest contribution stats. Display the number of segments you've submitted, the collective time you've saved for others, and more, all in real-time.

## Features

- **Stat Syncing**: Update your time saved, submissions, and time you've helped others save!
- **Customizable Update Intervals**: Decide how often the tool checks for updates to avoid unnecessary API calls.
- **Logging**: Keep track of all bio updates with an optional logging feature.

## Prerequisites

- Python 3.x
- `requests` library (Install via `pip install requests`)

## Setup 

1. Clone the repository.
   ```
   git clone https://github.com/2vsh/DiscordSponsorBlockStats.git
   ```
2. Navigate to the cloned directory.
3. Run the script once to generate a default configuration file (`SponsorStats.txt`).
   ```
   python main.py
   ```
4. Edit the `SponsorStats.txt` with your SponsorBlock UserID, Discord token, and other preferences.
5. Run the script again.
   ```
   python main.py
   ```

## Configuration

The `SponsorStats.txt` file contains several sections:

- **Logging**: Enable or disable the logging feature.
- **SponsorBlock**: Your UserID and the API endpoint (usually default).
- **Discord**: Your Discord token, bio preference (main or per server), and optional server ID.
- **Settings**: Update interval and a random delay to add some variation.

Ensure to keep your Discord token secret. It is only used locally and is never sent to any other server.

## Contributions

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---
