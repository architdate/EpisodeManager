import discord
import json
import os
import requests
import setupfeed as sf
import misc
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

    @commands.command(name='ongoing')
    async def ongoing(self, ctx):
        with open('config.json', 'r') as f:
            config = json.load(f)
        r = requests.get("http://api.jsonbin.io/b/{}/latest".format(config['jsonbin_key']))
        data = json.loads(r.text)
        shows = []
        for i in data:
            shows.append(i[0])
        e = discord.Embed(color=discord.Color.gold(), title = "Ongoing Shows", description= "Currently, there are **{}** ongoing shows being tracked.".format(len(shows)))
        e.add_field(name='Shows', value='\n'.join(shows))
        await ctx.send(embed=e)

    @commands.command(name='delshow')
    async def delshow(self, ctx, *, show:str = None):
        if show == None:
            await ctx.send('`USAGE: plex delshow <showname>`')
        else:
            with open('config.json', 'r') as f:
                config = json.load(f)
            r = requests.get("http://api.jsonbin.io/b/{}/latest".format(config['jsonbin_key']))
            data = json.loads(r.text)
            valid_shows = []
            showfound = False
            for i in data:
                if i[0] == show:
                    valid_shows.append(i)
            if len(valid_shows) == 1:
                data.remove(valid_shows[0])
                await ctx.send('`SHOW {} DELETED`'.format(show))
                r = requests.put("http://api.jsonbin.io/b/{}".format(config['jsonbin_key']), json = data, headers = {'Content-Type':'application/json'})
            elif len(valid_shows) > 1:
                await ctx.send('`{} SHOWS FOUND. PLEASE TYPE THE NUMBER OF THE SHOW YOU WANT TO DELETE`'.format(len(valid_shows)))
                e = discord.Embed(color=discord.Color.gold(), title = "Which show to delete?", description= "Currently, there are **{}** matched shows being tracked.".format(len(valid_shows)))
                showstr = ''
                for i in range(len(valid_shows)):
                    showstr += '{}. {}\n'.format(i+1, valid_shows[i][1])
                e.add_field(name='Shows', value=showstr.strip())
                await ctx.send(embed=e)
                reply = await self.check(ctx, 0)
                if reply:
                    if reply.content.strip().isdigit() and int(reply.content.strip())<= len(valid_shows):
                        print(valid_shows[int(reply.content.strip()) - 1])
                        data.remove(valid_shows[int(reply.content.strip()) - 1])
                        await ctx.send('`SHOW {} DELETED`'.format(show))
                    else:
                        return await ctx.send('`INVALID REPLY`')
                r = requests.put("http://api.jsonbin.io/b/{}".format(config['jsonbin_key']), json = data, headers = {'Content-Type':'application/json'})
            showfound = (len(valid_shows) > 0)
            if not showfound:
                await ctx.send('`NO SUCH SHOW FOUND IN CURRENT ONGOING EPISODES. USE ongoing COMMAND TO LIST OUT THE ONGOING SHOWS`')

    @commands.command(name='tsearch')
    async def tsearch(self, ctx, *, search:str = None, num:int = 10):
        def plexembed(title, description, color = discord.Color.gold()):
            return discord.Embed(color = color, title = title, description = description)
        if not search:
            await ctx.send(embed = plexembed("Appropriate Usage", '`plex tsearch <query>`'))
        else:
            r = requests.get('https://searx.org/?q={}&categories=files&language=en-US&format=json'.format(urllib.parse.quote(search)))
            data = json.loads(r.text)
            query = data['query']
            results = data['results']
            results = results[:num]
            e = discord.Embed(color=discord.Color.gold(), title = "Search Results", description= "The top {} results sorted by seeders are:".format(num))
            torrent, s, l, mag = [],[],[],[]
            for i in results:
                torrent.append(i['title'])
                s.append(i['seed'])
                l.append(i['leech'])
                mag.append(i['magnetlink'])
            e.add_field(name='Torrent', value='\n'.join([x[:20] for x in torrent]))
            e.add_field(name='Seeders', value='\n'.join([str(x) for x in s]))
            e.add_field(name='Leechers', value='\n'.join([str(x) for x in l]))
            e.add_field(name='Magnet', value='\n'.join(['[link]("{}")'.format(x) for x in mag]))
            try:
                await ctx.send(content='**`SEARCH RESULTS`**', embed= e)
            except:
                await ctx.send("Some error occured")


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

    @commands.command(name='addshowrss')
    async def addshowrss(self, ctx, *, showrssid:int = None):
        def plexembed(title, description, color = discord.Color.gold()):
            return discord.Embed(color = color, title= title, description=description)
        if not showrssid:
            await ctx.send(embed=plexembed("Appropriate Usage", '`plex addshowrss <rss_id>`'))
        else:
            r = requests.get('http://showrss.info/show/{}.rss'.format(showrssid))
            if r.status_code != 200:
                return await ctx.send(content='**`INVALID SHOWRSS ID`**', embed=plexembed("Invalid ID","Please use showrss command to search for your show. Error code: {}".format(r.status_code)))
            showname = r.text.split("showRSS feed: ")[1].split("</title>")[0].strip()
            await ctx.send(content = "**Setup Step 1**", embed = plexembed("Setup Plex Show", "What is resolution of the show? (Only enter a number among 480/720/1080)"))
            reply = await self.check(ctx, 0)
            if reply:
                await reply.delete()
                if reply.content == "cancel()": return
                resolution = reply.content.strip()
                await ctx.send(content= "**Setup Step 2**", embed = plexembed("Setup Plex Show", "Path to save this show?"))
                reply = await self.check(ctx, 0)
                if reply:
                    await reply.delete()
                    if reply.content == "cancel()": return
                    path = reply.content.strip()
                    await ctx.send(content = "**Setup Step 3**", embed=plexembed("Setup Plex Show", "Enter TVDB ID for being notified about the new episode. Recommended ID is: {}".format(tvdb_recommendation(showname))))
                    reply = await self.check(ctx, 0)
                    if reply:
                        await reply.delete()
                        if reply.content == "cancel()": return
                        tvdbid = reply.content.strip()
                        await ctx.send(content = "**Setup Step 4**", embed = plexembed("Setup Plex Show", "Download new episodes only? (Y/N)"))
                        reply = await self.check(ctx, 0)
                        if reply:
                            await reply.delete()
                            if reply.content == "cancel()": return
                            onlynew = reply.content.strip()
                            args = [showname, 'http://showrss.info/show/{}.rss'.format(showrssid), '{}p'.format(resolution), showname.replace(" ", "."), showname.lower().replace(" ",".")+".", ".", path, tvdbid, onlynew]
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
