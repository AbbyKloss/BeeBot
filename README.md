# BeeBot
just a bot im making. no real plans yet

incrementally adding new features as i get the inspiration and motivation to

## commands
default prefix is '<', you can change that with prefix (under Info:)

Command    |   Usage

### Autosend:
- fgoOptIn  
- fgoOptOut 
- fgoTimeUp 
- OptIn     
- optOut

### BotCommands:
- 3         [@user]
- f         [@user]
- google    \<search terms\>
- hi        [@user]
- roll      \<'n'd'x'\> [adv/dis]

### Images:
- Imgur     [imgur album url/ID]
- iSearch   \<search terms\>

### Info:
- github    
- invite
- prefix    \<prefix\>

#### note: \<this is a required parameter\>

there are also hidden commands but those are just for the person hosting the bot

## Requirements to run the bot yourself:
(i think this is it, im not entirely sure)  
  pip installs:  
  - [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) (req. for google-images-search)
  - [google-api-python-client](https://github.com/googleapis/google-api-python-client)
  - [google-images-search](https://github.com/arrrlo/Google-Images-Search)
  - [python-dotenv](https://github.com/theskumar/python-dotenv)
  - [py-cord](https://github.com/Pycord-Development/pycord)
  - [requests](https://github.com/psf/requests)
  - [discord-pretty-help](https://github.com/stroupbslayen/discord-pretty-help) (i'd rather build my own, this won't stay too long)

## Recent Edits
(6/12/2022) (v0.3.5)
- Added randName, for all your crowdsourced naming needs
- probably also a few other things, I've made changes without committing them in the last half year

(11/28/2021) (v0.3.3)
- added r34, gelbooru, danbooru commands

(9/14/2021) (v0.3.1)
- made the optouts not make new database entries. They also delete empty ones (i.e. Auto/FGOBool == 0)
- made every ctx.author.name into ctx.author.display_name. now everyone has a nickname in the eyes of BeeBot
- added an echo command in Owner, will later use it to test channel things, probably
- toyed with a prefixless change prefix command. didn't work, look at it more later

(9/9/2021) (v0.3.0) (yes im saying it's major enough for a new number)
- moved from dumb text files to a sqlite3 database
- made it possible to change bot prefix per guild
- added database things that happen when BeeBot leaves/joins a guild
- database opens and closes once each function call
- fun fact: sqlite3 is included in most linux distros and every python install (to my knowledge)

(9/6/2021) (v0.2.4)
- removed imgurpython
- brought on discord-pretty-help
- made the help prettier
- actually added all the pip installs needed to the readme
- divided BotCommands into 2 more files
- giving this version numbers now? retroactively, as well

(9/5/2021)(v0.2.3)
- added <imgur, using requests
- im kinda proud of the requests part
- rewrote <notcat to follow suit
- made <cimage slightly more robust

(9/1/2021) (v0.2.1)
- imageSearch and currentImage are now iSearch and cImage

(8/31/2021) (v0.2.0)
- added a google image search, works with safesearch to keep nsfw out of not that areas
- modified all the commands to reply to the person that sent them
- added an owner-only command to send the last-sent image

(8/5/2021) (v0.1.3)
- added a reminder for Fate/Grand Order so people don't forget to log in
- <fgoTimeUp to know how far away the daily reset is

(7/15/2021) (v0.1.2)
- Added Autosend (feliz jueves)
- modified the invite link, no longer has admin perms (should've never had that, whoops)
- added <homeowneredcheck
- tacked the new cog onto the load list in the main file

(6/17/2021) (v0.1.1)
- temporarily turned off the 'hope' listener (everyone in my main server was getting annoyed at it, myself included)
- added a dice rolling function, uses the [n]d[x] system

(6/11/2021) (V 1.0? V <1? idk what a full release of this would look like) (v0.1.0)
- added commands to change the bot's status to something not in the random lists
- migrated a surprising amount of things from the main file to Owner.py
- BeeBot.py is kind of just a shell from which to manage everything else now

## Todo
- figure out tweepy so i can add out of touch thursdays to this
- ~~maybe move all the optin/optout files to a different folder~~ did a database
- test webhooks
- ~~maybe separate BotCommands a bit?~~
