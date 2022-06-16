from discord.ext import commands
from discord.ext.commands import Cog, command, is_owner, guild_only

from rich import print
from rich.progress import track

from utils.useful import custom, get_data, success, failure, auto_bump

import asyncio, time, discord, random


class utility(commands.Cog):
  """Utility commands."""
  def __init__(self, bot : discord.Client):
    self.bot = bot
    # self.hidden = True
    self.data = get_data()
    self.sleep_time_high = [2, 2.2, 2.4, 2.6, 2.8]
    self.sleep_time_low = [1, 1.2, 1.4, 1.6, 1.8]

  @command(aliases = ["guildsack"])
  @is_owner()
  async def ackguilds(self, ctx):
    try: await ctx.message.delete()
    except: pass
    for guild in track(self.bot.guilds, description = f"[bold white]{time.strftime('[%H:%M:%S]', time.localtime())}:[/bold white] [bold blue]Marking guilds as read...[/bold blue]"):
      await guild.ack()
      await asyncio.sleep(random.choice(self.sleep_time_low))
    success("All guilds marked as read.", header = "Guilds Ack")

  @command(aliases = ['rmfriends', 'rmf'])
  @is_owner()
  async def removefriends(self, ctx):
    try: await ctx.message.delete()
    except: pass
    for friend in track(self.bot.user.friends, description = f"[bold white]{time.strftime('[%H:%M:%S]', time.localtime())}:[/bold white] [bold blue]Removing friends...[/bold blue]"):
      await friend.delete()
      await asyncio.sleep(random.choice(self.sleep_time_low))
    success("Removed all friends.", header = "Remove Friends")
  
  @command(aliases = ['leavegroups', 'leavegdms', 'lgdm'])
  @is_owner()
  async def leavegroupdms(self, ctx):
    try: await ctx.message.delete()
    except: pass
    for group in track(self.bot.private_channels, description = f"[bold white]{time.strftime('[%H:%M:%S]', time.localtime())}:[/bold white] [bold blue]Leaving group DMs...[/bold blue]"):
      if isinstance(group, discord.GroupChannel):
        await group.leave()
        await asyncio.sleep(random.choice(self.sleep_time_high))
    success("Left all group DMs.", header = "Leave Group DMs")

  @command(aliases = ['abump', 'autob'])
  @is_owner()
  @guild_only()
  async def autobump(self, ctx, command : str, delay : int):
    try: await ctx.message.delete()
    except: pass
    if ctx.channel.id in self.bot.bumping_channels:
      return await ctx.reply("This channel is already being automatically bumped.")
    self.bot.loop.create_task(auto_bump(ctx.channel, command, int(delay)))
    self.bot.bumping_channels.append(ctx.channel.id)
    success(f"Started bumping task for channel: #{ctx.channel.name}", header = "Auto Bump")


async def setup(bot):
  await bot.add_cog(utility(bot))