import discord
from discord.ext import commands

import sys, traceback

"""This is a multi file example showcasing many features of the command extension and the use of cogs.
These are examples only and are not intended to be used as a fully functioning bot. Rather they should give you a basic
understanding and platform for creating your own bot.

These examples make use of Python 3.6.2 and the rewrite version on the lib.

For examples on cogs for the async version:
https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5

Rewrite Documentation:
http://discordpy.readthedocs.io/en/rewrite/api.html

Rewrite Commands Documentation:
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html

Familiarising yourself with the documentation will greatly help you in creating your bot and using cogs.
"""


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['!', 'plex ', '.']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['cogs.setup',
                      'cogs.members',
                      'cogs.owner']

bot = commands.Bot(command_prefix=get_prefix, description='A Plex Show Setup Bot')

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}.'.format(extension), file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print('Logged In')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    print('Successfully logged in and booted...!')

with open('config.json', 'r') as f:
    config = json.load(f)
bot.run(config['bot_token'], bot=True, reconnect=True)
