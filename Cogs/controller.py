import discord
import pickle
import json
from discord.ext import commands


class ControllerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('leaguelist.txt', 'rb') as f:
        llist = pickle.load(f)

    league = discord.SlashCommandGroup("league", "Commands to add/remove/edit what leagues are loaded",
                                       )

    async def get_channel_names(ctx: discord.AutocompleteContext):
        c_list = []
        for channel in ctx.bot.get_all_channels():
            c_list.append(channel.name)

        return c_list

    @league.command()
    async def add(self,ctx: discord.ApplicationContext,league_name : discord.Option(str, choices=llist), channelname:discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_channel_names)), option:discord.Option(str, choices=["new", "update"])):
        chan = None
        for channel in ctx.bot.get_all_channels():
            if channel.name == channelname:
                chan = channel
                break
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                config['watchlist'][option][league_name] = chan.id
            with open('config.json', 'w') as f:
                json.dump(config, f)
            await ctx.respond(f"{league_name} added to watchlist!")
        except:
            await ctx.respond("Error")






    @league.command()
    async def remove(self,ctx, league_name: discord.Option(str, choices=llist),  option:discord.Option(str, choices=["new", "update"])):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                config['watchlist'][option].pop(league_name)
            with open('config.json', 'w') as f:
                json.dump(config,f)
            await ctx.respond(f"{league_name} has been removed from watchlist")
        except:
            await ctx.respond('Error')





def setup(bot):
    bot.add_cog(ControllerCog(bot))