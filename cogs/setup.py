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

        embed = discord.Embed(color=discord.Color.gold(), title='Example Embed',
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
                    args.append(reply.content.strip())
                    await ctx.send(content = "**Setup Step 3**", embed = plexembed("Setup Plex Show", "Enter a unique file identifier for the RSS Shows (Only files with this string will be downloaded from the feed)"))
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
                                        await ctx.send(content = "**Setup Step 8**", embed = plexembed("Setup Plex Show", "Enter TVDB ID for being notified about the new episode"))
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
    bot.add_cog(SimpleCog(bot))
