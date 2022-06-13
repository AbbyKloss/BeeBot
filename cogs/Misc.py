import discord
from discord.ext import commands

import httplib2
import json
import pygsheets
from random import choice as choose

from apiclient import discovery
from google.oauth2 import service_account

def RandNameFromSheet():
    # obtaining the specific modifiers
    with open("files/modifiers.json", 'r') as mods:
        data = json.load(mods)
        key = data["APIKey"]
        spreadsheetId = data["SpreadsheetID"]
    
    # obtaining creds for pygsheets
    with open("files/credentials.json", "r") as creds:
        info = json.load(creds)
    credentials = service_account.Credentials.from_service_account_info(info)
    client = pygsheets.authorize(service_account_file='files/credentials.json')
    
    # pygsheets setup
    sheet = client.open_by_key(spreadsheetId)
    wks = sheet.worksheet_by_title("Form Responses 3")

    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build(
        'sheets',
        'v4',
        http=httplib2.Http(),
        discoveryServiceUrl=discoveryUrl,
        developerKey=key)

    service = discovery.build('sheets', 'v4', credentials=credentials)

    rangeName = f'Form Responses 3!A1:E{wks.rows}' # range of col A row 1 to col E and max row
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        return 'No data found.'
    else:
        lastRow = len(values)
        lastNum = lastRow-1
        # print(f"Found {lastRow} rows")
        # print(f"Last num: {lastNum}")
        randchoice = choose(values)
        string = f"\"{randchoice[3]}\", submitted "
        if (randchoice[2] != ""):
            string += f"by {randchoice[2]}"
        else:
            string += "anonymously"
        return string

class Misc(commands.Cog, description="Things that currently don't fit under existing categories"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='randName', help='randomly picks from crowdsourced names', usage='')
    async def rand_name(self, ctx):
        await ctx.reply(RandNameFromSheet(), mention_author=False)


def setup(bot):
    bot.add_cog(Misc(bot))