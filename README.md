# AbBot
just a bot im making. no real plans yet

incrementally adding new features as i get the inspiration and motivation to

## commands
do <help lmao  
there are also hidden commands but those are just for the person hosting the bot

## Requirements to run the bot yourself:
(i think this is it, im not entirely sure)  
  pip installs:  
  - beautifulsoup4 (may come with google)
  - google (may break)
  - python-dotenv  
  - discord
  - time
  - datetime

## Recent Edits
(9/5/2021)
- added <imgur, using requests
- im kinda proud of the requests part

(9/1/2021)
- imageSearch and currentImage are now iSearch and cImage

(8/31/2021)
- added a google image search, works with safesearch to keep nsfw out of not that areas
- modified all the commands to reply to the person that sent them
- added an owner-only command to send the last-sent image

(8/5/2021)
- added a reminder for Fate/Grand Order so people don't forget to log in
- <fgoTimeUp to know how far away the daily reset is

(7/15/2021)
- Added Autosend (feliz jueves)
- modified the invite link, no longer has admin perms (should've never had that, whoops)
- added <homeowneredcheck
- tacked the new cog onto the load list in the main file

(6/17/2021)
- temporarily turned off the 'hope' listener (everyone in my main server was getting annoyed at it, myself included)
- added a dice rolling function, uses the [n]d[x] system

(6/11/2021) (V 1.0? V <1? idk what a full release of this would look like)
- added commands to change the bot's status to something not in the random lists
- migrated a surprising amount of things from the main file to Owner.py
- AbBot.py is kind of just a shell from which to manage everything else now

## Todo
- figure out tweepy so i can add out of touch thursdays to this
- maybe move all the optin/optout files to a different folder
- test webhooks
- need to rewrite <notcat to use requests, should be simple