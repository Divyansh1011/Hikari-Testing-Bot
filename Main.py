from __future__ import annotations

from __init__ import __version__
import hikari
from hikari import intents
import lightbulb
from datetime import datetime
from pytz import timezone as tz
import Utils

bot = lightbulb.Bot(
			token = Utils.token, 
			prefix = "?",
			intents = hikari.Intents.ALL,
			owner_ids = [515097702057508882]
		)

@bot.listen(hikari.ShardReadyEvent)
async def ready_listener(event: hikari.ShardReadyEvent):
	extensions = ['Meta', 'Fun', 'Mod']
	for ext in extensions:
		bot.load_extension(f"Plugins.{ext}")
	await bot.update_presence(
				status = hikari.Status.ONLINE,
				activity = hikari.Activity(
						name = f"?help | v{__version__}", 
						type = hikari.ActivityType.LISTENING
				)
	)
	print(Utils.LOGCHANNELID)
	await bot.rest.create_message(Utils.LOGCHANNELID, f"Bot is online at time {datetime.now().astimezone(tz('Asia/Kolkata')).strftime('%d.%m.%Y - %H:%M:%S')}")
	print(f"Bot is ready")

@lightbulb.checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
@bot.command(name = 'load')
async def load_ext(ctx : lightbulb.Context, ext : str | None) -> None:
	"""
	Loads a plugin that is placed in the Plugins folder.
	"""
	if ext is None:
		await ctx.respond(
			f"Please provide a Plugin name.",
			reply = True
	)
	elif ext is not None:
		try:
			bot.load_extension(f"Plugins.{ext}")
			await ctx.respond(f"Successfully loaded {ext} Plugin")
		except Exception as e:
			await ctx.respond(f"Failed to load {ext} Plugin. Reason : {e}")
@load_ext.command_error()
async def load_ext_error(error):
	await error.context.respond(f"Error occured. \nError Traceback:\n ```{error}```")

@lightbulb.checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
@bot.command(name = 'unload')
async def unload_ext(ctx : lightbulb.Context, ext : str | None) -> None:
	"""
	Unloads an already loaded plugin.
	"""
	if ext is None:
		await ctx.respond(
			f"Please provide a Plugin name.",
			reply = True
	)
	elif ext is not None:
		try:
			bot.unload_extension(f"Plugins.{ext}")
			await ctx.respond(f"Successfully unloaded {ext} Plugin")
		except Exception as e:
			await ctx.respond(f"Failed to unload {ext} Plugin. Reason : {e}")
@unload_ext.command_error()
async def unload_ext_error(error):
	await error.context.respond(f"Error occured. \nError Traceback:\n ```{error}```")

@lightbulb.checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
@bot.command(name = 'reload')
async def reload_ext(ctx : lightbulb.Context, ext : str | None) -> None:
	"""
	Reloads an already loaded plugin.
	"""
	if ext is None:
		await ctx.respond(
			f"Please provide a Plugin name.",
			reply = True
	)
	elif ext is not None:
		try:
			bot.reload_extension(f"Plugins.{ext}")
			await ctx.respond(f"Successfully reloaded {ext} Plugin")
		except Exception as e:
			await ctx.respond(f"Failed to reload {ext} Plugin. Reason : {e}")
@reload_ext.command_error()
async def reload_ext_error(error):
	await error.context.respond(f"Error occured. \nError Traceback:\n ```{error}```")

@lightbulb.owner_only()
@bot.command(name = 'logout', aliases = ['shutdown'])
async def logout_command(ctx : lightbulb.Context) -> None:
	"""Shuts down the bot"""
	await ctx.respond(f"Logging out...")
	await ctx.bot.close()

"""
@bot.command(name = 'test')
async def test(ctx : lightbulb.Context) -> None:
	await bot.rest.create_message(810521948312174624, "Test")

@bot.command()
async def ping(ctx):
	await ctx.respond("Pong!")
"""

bot.run()
