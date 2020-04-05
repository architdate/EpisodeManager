import discord
from discord.ext import commands
import misc

def plexembed(title, description, color = discord.Color.gold()):
    return discord.Embed(color = color, title= title, description=description)

class PlexControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def users(self, ctx):
        """Lists all plex users"""
        members = misc.get_users(self.bot.plexacc)
        await ctx.send(embed=plexembed('List of Users:', "\n".join(members['friends'])))

    @commands.command(name='scan')
    async def scan(self, ctx, category):
        """Category scan"""
        if category != "movies" and category != "anime" and category != "tv":
            await ctx.send('**`INVALID CATEGORY. PLEASE USE EITHER movies OR anime OR tv AS CATEGORIES`**')
        if category == "movies":
            misc.scan_movies(self.bot.plex)
            await ctx.send('**`SCAN COMPLETE`**')
        if category == "anime":
            misc.scan_anime(self.bot.plex)
            await ctx.send('**`SCAN COMPLETE`**')
        if category == "tv":
            misc.scan_tv(self.bot.plex)
            await ctx.send('**`SCAN COMPLETE`**')


def setup(bot):
    bot.add_cog(PlexControl(bot))
