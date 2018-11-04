import discord
import os
import setupfeed as sf
from discord.ext import commands


"""A simple cog example with simple commands. Showcased here are some check decorators, and the use of events in cogs.

For a list of inbuilt checks:
http://dischttp://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checksordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checks

You could also create your own custom checks. Check out:
https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/core.py#L689

For a list of events:
http://discordpy.readthedocs.io/en/rewrite/api.html#event-reference
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#event-reference
"""


class SimpleCog:
    """SimpleCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='repeat', aliases=['copy', 'mimic'])
    async def do_repeat(self, ctx, *, our_input: str):
        """A simple command which repeats our input.
        In rewrite Context is automatically passed to our commands as the first argument after self."""

        await ctx.send(our_input)

    @commands.command(name='embeds')
    @commands.guild_only()
    async def example_embed(self, ctx):
        """A simple command which showcases the use of embeds.

        Have a play around and visit the Visualizer."""

        embed = discord.Embed(title='Example Embed',
                              description='Showcasing the use of Embeds...\nSee the visualizer for more info.',
                              colour=0x98FB98)
        embed.set_author(name='MysterialPy',
                         url='https://gist.github.com/MysterialPy/public',
                         icon_url='http://i.imgur.com/ko5A30P.png')
        embed.set_image(url='https://cdn.discordapp.com/attachments/84319995256905728/252292324967710721/embed.png')

        embed.add_field(name='Embed Visualizer', value='[Click Here!](https://leovoel.github.io/embed-visualizer/)')
        embed.add_field(name='Command Invoker', value=ctx.author.mention)
        embed.set_footer(text='Made in Python with discord.py@rewrite', icon_url='http://i.imgur.com/5BFecvA.png')

        await ctx.send(content='**A simple Embed for discord.py@rewrite in cogs.**', embed=embed)

    @commands.command(name='setup')
    async def setup(self, ctx):
        args = []
        embed = discord.Embed(title='Setup Plex Show', description='Setup an RSS feed for the shows to appear in your Plex')
        embed.add_field(name='Setup Step 1', value='What is the name of the Show?')
        await ctx.send(content='**Plex Show Setup**', embed = embed)
        reply = await self.bot.wait_for("message")
        args.append(reply.content)
        embed = discord.Embed(title='Setup Plex Show', description='Setup an RSS feed for the shows to appear in your Plex')
        embed.add_field(name='Setup Step 2', value='Enter a valid RSS feed for the show')
        await ctx.send(embed = embed)
        reply = await self.bot.wait_for("message")
        args.append(reply.content)
        embed = discord.Embed(title='Setup Plex Show', description='Setup an RSS feed for the shows to appear in your Plex')
        embed.add_field(name='Setup Step 3', value='Enter a unique file identifier for the RSS Shows (Only files with this string will be downloaded from the feed)')
        await ctx.send(embed = embed)
        reply = await self.bot.wait_for("message")
        args.append(reply.content)
        embed = discord.Embed(title='Setup Plex Show', description='Setup an RSS feed for the shows to appear in your Plex')
        embed.add_field(name='Setup Step 4', value="Enter a string to identify the media file from the torrent (Can be 'The.Big.Bang.Theory' or '.mkv' for example)")
        await ctx.send(embed = embed)
        reply = await self.bot.wait_for("message")
        args.append(reply.content)
        embed = discord.Embed(title='Setup Plex Show', description='Setup an RSS feed for the shows to appear in your Plex')
        embed.add_field(name='Setup Step 5', value='Enter First Split for episode rename')
        await ctx.send(embed = embed)
        reply = await self.bot.wait_for("message")
        args.append(reply.content)
        embed = discord.Embed(title='Setup Plex Show', description='Setup an RSS feed for the shows to appear in your Plex')
        embed.add_field(name='Setup Step 6', value='Enter Second Split for episode rename')
        await ctx.send(embed = embed)
        reply = await self.bot.wait_for("message")
        args.append(reply.content)
        embed = discord.Embed(title='Setup Plex Show', description='Setup an RSS feed for the shows to appear in your Plex')
        embed.add_field(name='Setup Step 7', value='Enter path for the new episode to be saved')
        await ctx.send(embed = embed)
        reply = await self.bot.wait_for("message")
        args.append(reply.content)
        embed = discord.Embed(title='Setup Plex Show', description='Setup an RSS feed for the shows to appear in your Plex')
        embed.add_field(name='Setup Step 8', value='Enter TVDB ID for being notified about the new episode')
        await ctx.send(embed = embed)
        reply = await self.bot.wait_for("message")
        args.append(reply.content)
        embed = discord.Embed(title='Setup Plex Show', description='Setup an RSS feed for the shows to appear in your Plex')
        embed.add_field(name='Setup Step 9', value='Download new episodes only? (Y/N)')
        await ctx.send(embed = embed)
        reply = await self.bot.wait_for("message")
        args.append(reply.content)
        sf.argsetup(args)
        embed = discord.Embed(title='Plex Show Setup Complete', description='Enjoy your show! You can check for updates in the #updates channel')
        await ctx.send(embed=embed)


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(SimpleCog(bot))
