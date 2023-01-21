import discord
import pandas
from discord.ext import commands, tasks
from discord.utils import get
import json
import pandas as pd
from pandas.io.json import json_normalize
import requests
import datetime
from Utils import dataframeutils, discutils


class Apilistener(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.prop_get.start()

    def cog_unload(self):
        self.prop_get.cancel()

    async def send_new_messages(self, league_name, channel_id, data : pandas.DataFrame):

        chan = self.bot.get_channel(int(channel_id))
        try:
            df = data[data['attributes.league_y'] == league_name]
            l = df.drop(
                df.columns.difference(['attributes.line_score_y', 'attributes.stat_type_y', 'attributes.name_y']),
                axis=1)
            text = ''
            if l.empty:
                return
            for index, row in l.iterrows():
                l = row.to_csv(header=None, index=False).strip('\r\n').split('\r\n')
                s = f'{l[2]} - {l[1]}  ({l[0]}) \n'
                text += s

            embed = discord.Embed(title=league_name, description=text, color= discord.Color.green())
            embed.set_footer(text=f'{self.bot.user[:-5]} . {datetime.datetime.utcnow()}')

            await chan.send(embed=embed)
        except:
            return





    async def send_update_messages(self, league_name, channel_id, data: pandas.DataFrame):
        chan = self.bot.get_channel(int(channel_id))
        try:
            df = data[data['attributes.league_y'] == league_name]
            l = df.drop(
                df.columns.difference(
                    ['attributes.line_score_y', 'attributes.stat_type_y', 'attributes.name_y',
                     'attributes.description_x',
                     'attributes.line_score_x', 'attributes.updated_at_x', 'attributes.updated_at_y',
                     'attributes.team_name_x',
                     'attributes.image_url_y']),
                axis=1)

            for index, row in l.iterrows():


                l = row.to_csv(header=None, index=False).strip('\r\n').split('\r\n')
                if float(l[1]) == float(l[4]):
                    return
                if float(l[1]) < float(l[4]):
                    arrow = ':arrow_up:'
                else:
                    arrow = ':arrow_down:'
                embed = discord.Embed(timestamp=datetime.datetime.now(), color = discord.Color.teal())
                embed.add_field(name=l[8], value=f'{league_name} - vs {l[0]}',inline= False)
                embed.add_field(name=l[5], value=f'{l[1]} -> {l[4]} {arrow}',inline=False)
                embed.add_field(name='Time Taken to Bump',
                                value=f'{datetime.datetime.fromisoformat(l[6]) - datetime.datetime.fromisoformat(l[2])} \n\n', inline=False)
                embed.set_thumbnail(url=f'{l[7]}')
                embed.set_footer(text=self.bot.user.name, icon_url= self.bot.user.avatar)

                await chan.send(embed=embed)
        except:

            return



    @tasks.loop(seconds=10)
    async def prop_get(self):

        data = dataframeutils.parse_json_into_df()
        update_data = dataframeutils.get_update(data)
        new_data = dataframeutils.get_new(data)

        watchlist = discutils.get_watch_league()

        #send new message

        for league in watchlist['new']:

            await self.send_new_messages(league, watchlist['new'][league], new_data)

        #send update message

        for league in watchlist['update']:
            await self.send_update_messages(league, watchlist['update'][league], update_data)


def setup(bot):
    bot.add_cog(Apilistener(bot))



