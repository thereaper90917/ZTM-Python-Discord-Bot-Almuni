# ZTM-Python-Discord-Bot-Almuni

A Discord bot written in Python by and for the [Zero To Mastery](https://zerotomastery.io/) community during the [Frosty February hackathon](https://github.com/zero-to-mastery/frosty-february-hackathon).

## Goal

The main goal behind this project is to help members find projects. Each project will be categorized under Beginner, Intermediate or Advanced.

## Getting Started

This project was created using the latest version of discord.py. You can find the docs [here](https://discordpy.readthedocs.io/en/latest/)

### Prerequisites
* python v3.7
* discord v1.0.1
* discord.py v1.3.1
* praw v6.5.1
* tinydb v3.15.2
* requests v2.22.0
* beautifulsoup4 v4.8.2

### Running the bot locally

To run the bot locally, note that you must have the modules listed in the Prerequisites section installed and will need to create your own Discord Bot account. Follow the instructions [here](https://discordpy.readthedocs.io/en/latest/discord.html) to create and invite your bot to a server.

In the command line/terminal, enter the following commands:
```
git clone https://github.com/thereaper90917/ZTM-Python-Discord-Bot-Almuni.git
cd ZTM-Python-Discord-Bot-Almuni
```
Open the files in the folder with your preferred text editor. After this, you'll need to navigate to the `discordbot.py` file and replace the config token variable with the client token provided to you after you created your bot.

For example, if your token was 'abcdefgh', you'd replace:

```py
bot.run(config['token'], bot=True, reconnect=True)
```
with:

```py
bot.run('abcdefgh', bot=True, reconnect=True)
```
After doing this, save the file, go back to the terminal window and enter the following:

`python3 discordbot.py`

The bot should come online in your server and you can then use any of the available commands.

## Contributors

[![thereaper90917](https://avatars3.githubusercontent.com/u/42868546?s=170&v=4)](https://github.com/thereaper90917)
[![jerbeck](https://avatars1.githubusercontent.com/u/432648?s=170&v=4)](https://github.com/jerbeck)
[![solomon403](https://avatars0.githubusercontent.com/u/55158465?s=170&v=4)](https://github.com/Solomon403)
[![emryscass](https://avatars2.githubusercontent.com/u/54422867?s=170&v=4)](https://github.com/emryscass)
[<img src="https://avatars1.githubusercontent.com/u/24484139?s=60&v=4" height="170" alt="jwim">](https://github.com/jwim)
