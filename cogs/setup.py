import discord
import json
import os
import requests
import setupfeed as sf
import urllib.parse
from bs4 import BeautifulSoup
from discord.ext import commands

def nyaarss(searchterm):
    return "https://nyaa.si/?page=rss&q={}&c=0_0&f=0".format(urllib.parse.quote(searchterm))

def parserss(rssfeed):
    if rssfeed.startswith('nyaa::'):
        return nyaarss(rssfeed.split('nyaa::')[1])
    else:
        return rssfeed

def tvdb_recommendation(searchterm):
    with open('config.json', 'r') as f:
        config = json.load(f)
    apikey = config['tvdb_api']
    tvdbtoken = json.loads(requests.post("https://api.thetvdb.com/login", data = json.dumps({"apikey":apikey}), headers = {"Content-Type": "application/json", "Accept":"application/json"}).text)['token']
    query = {"name":searchterm}
    headers = {"Accept":"application/json", "Authorization":"Bearer {}".format(tvdbtoken)}
    try:
        series_id = int(json.loads(requests.get("https://api.thetvdb.com/search/series?" + urllib.parse.urlencode(query), headers=headers).text)['data'][0]['id'])
    except:
        series_id = -1
    return series_id

class Setup:
    """SimpleCog"""

    def __init__(self, bot):
        self.bot = bot

    async def check(self, ctx, val):
        def is_numb(msg):
            if msg.author == ctx.message.author:
                if msg.content.isdigit() and val != 0:
                    return 0 < int(msg.content) < val
                elif val == 0:
                    return True
                else:
                    return False
            else:
                return False

        reply = await self.bot.wait_for("message", check=is_numb)
        return reply

    @commands.command(name='showrss')
    async def showrss(self, ctx, *, search:str = None):
        def plexembed(title, description, color = discord.Color.gold()):
            return discord.Embed(color = color, title= title, description=description)
        if not search:
            await ctx.send(embed = plexembed("Appropriate Usage", '`plex showrss <query>`'))
        else:
            r = requests.get('http://showrss.info/browse')
            s = BeautifulSoup(r.text, 'html.parser')
            listopt = s.find_all('option')
            listopt.pop(0)
            showlist = {}
            for i in listopt:
                if search.lower() in i.get_text().lower():
                    showlist[i.get_text()] = i.get('value')
            e = discord.Embed(color=discord.Color.gold(), title = "Search Results", description= "showrss.info returned with **{}** results:".format(len(showlist)))
            show, val = [], []
            for k, v in showlist.items():
                show.append(k)
                val.append('http://showrss.info/show/{}.rss'.format(v.strip()))
            e.add_field(name='Shows', value='\n'.join(show))
            e.add_field(name='RSS Link', value='\n'.join(val))
            try:
                await ctx.send(content='**`SEARCH RESULTS`**', embed=e)
            except:
                await ctx.send(content='**`SEARCH RESULTS`**', embed=plexembed("Too many Results", "The search returned too many results (**{}** Results). Please search with more specificity".format(len(showlist))))

    @commands.command(name='setup')
    async def setup(self, ctx, *, msg:str = None):
        args = []
        def plexembed(title, description, color = discord.Color.gold()):
            return discord.Embed(color = color, title= title, description=description)
        if not msg:
            await ctx.send(content = "**Setup Step 1**", embed = plexembed("Setup Plex Show", "What is the name of the Show?"))
            reply = await self.check(ctx, 0)
            if reply:
                await reply.delete()
                if reply.content == "cancel()": return
                args.append(reply.content.strip())
                await ctx.send(content = "**Setup Step 2**", embed = plexembed("Setup Plex Show", "Enter a valid RSS feed for the show"))
                reply = await self.check(ctx, 0)
                if reply:
                    await reply.delete()
                    if reply.content == "cancel()": return
                    args.append(parserss(reply.content.strip()))
                    await ctx.send(content = "**Setup Step 3**", embed = plexembed("Setup Plex Show", "Enter a unique file identifier for the RSS Shows (Only files with this string will be downloaded from the feed). The recommendation is : `*{}*`".format(args[0])))
                    reply = await self.check(ctx, 0)
                    if reply:
                        await reply.delete()
                        if reply.content == "cancel()": return
                        args.append(reply.content.strip())
                        await ctx.send(content = "**Setup Step 4**", embed = plexembed("Setup Plex Show", "Enter a string to identify the media file from the torrent (Can be 'The.Big.Bang.Theory' or '.mkv' for example)"))
                        reply = await self.check(ctx, 0)
                        if reply:
                            await reply.delete()
                            if reply.content == "cancel()": return
                            args.append(reply.content.strip())
                            await ctx.send(content = "**Setup Step 5**", embed = plexembed("Setup Plex Show", "Enter First Split for episode rename"))
                            reply = await self.check(ctx, 0)
                            if reply:
                                await reply.delete()
                                if reply.content == "cancel()": return
                                args.append(reply.content.strip())
                                await ctx.send(content = "**Setup Step 6**", embed = plexembed("Setup Plex Show", "Enter Second Split for episode rename"))
                                reply = await self.check(ctx, 0)
                                if reply:
                                    await reply.delete()
                                    if reply.content == "cancel()": return
                                    args.append(reply.content.strip())
                                    await ctx.send(content = "**Setup Step 7**", embed = plexembed("Setup Plex Show", "Enter path for the new episode to be saved"))
                                    reply = await self.check(ctx, 0)
                                    if reply:
                                        await reply.delete()
                                        if reply.content == "cancel()": return
                                        args.append(reply.content.strip())
                                        await ctx.send(content = "**Setup Step 8**", embed = plexembed("Setup Plex Show", "Enter TVDB ID for being notified about the new episode. Recommended ID is: {}".format(tvdb_recommendation(args[0]))))
                                        reply = await self.check(ctx, 0)
                                        if reply:
                                            await reply.delete()
                                            if reply.content == "cancel()": return
                                            args.append(reply.content.strip())
                                            await ctx.send(content = "**Setup Step 9**", embed = plexembed("Setup Plex Show", "Download new episodes only? (Y/N)"))
                                            reply = await self.check(ctx, 0)
                                            if reply:
                                                await reply.delete()
                                                if reply.content == "cancel()": return
                                                args.append(reply.content.strip())
                                                await ctx.send(content="**Confirm Selections? (Y/N)**", embed = plexembed("Selections", ", ".join(args)))
                                                reply = await self.check(ctx, 0)
                                                if reply:
                                                    await reply.delete()
                                                    if reply.content.lower() == "n":
                                                        await ctx.send(embed = plexembed("Plex Show Setup Cancelled", "The Show **{}** was not added".format(args[0])))
                                                        return
                                                    else:
                                                        sf.argsetup(args)
                                                        embed = discord.Embed(color=discord.Color.gold(), title='Plex Show Setup Complete', description='The Show **{}** was added successfully. Enjoy your show! You can check for updates in the #updates channel'.format(args[0]))
                                                        await ctx.send(embed=embed)


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(Setup(bot))
