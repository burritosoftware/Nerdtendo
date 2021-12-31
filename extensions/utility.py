from hikari.presences import Status
import lightbulb
import os
from subprocess import Popen
import hikari
import functions.dataManager as dataManager

ping_plugin = lightbulb.Plugin("Ping")

@ping_plugin.command
@lightbulb.command("ping", description="Get the bot's latency.", ephemeral=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Pong! Latency: {ctx.bot.heartbeat_latency*1000:.2f}ms")

update_plugin = lightbulb.Plugin("Update")

@update_plugin.command
@lightbulb.command("update", description="Pulls the latest source from GitHub and updates the bot.", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def update(ctx: lightbulb.Context) -> None:
    if str(ctx.author.id) != "261236127581601793":
        await ctx.respond(f"You do not have permission to perform this command.")
    else:
        output = os.popen('git pull').read()
        if "Already up to date." in output:
            await ctx.respond("Bot already up to date.")
        else:
            ctx.bot.d.logger.info(f"Bot updated!\n\n{output}")
            await ctx.respond(f"Update complete! The bot will restart momentarily...\n\n```\n{output}\n```")
            await ctx.bot.update_presence(status=hikari.Status.IDLE, activity=hikari.Activity(name="Updating, please wait..."))
            if os.name != "nt":
                p = Popen(['pm2', 'restart', 'bot'])
                p.poll()

# test_plugin = lightbulb.Plugin("Test")
# @test_plugin.command
# @lightbulb.option(
#     "makerid", "The maker id to add to the database", str, required=True
# )
# @lightbulb.command("setmakerid", description="Test command to try databasing.", auto_defer=True)
# @lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
# async def setmakerid(ctx: lightbulb.Context) -> None:
#     table = await dataManager.tableLookup(ctx.bot, 'user')
#     await dataManager.tableInsert(table, dict(id=ctx.author.id, makerid=ctx.options.makerid))
#     await ctx.respond("Added your ID to the database! Please don't run this again or things may break from this point lmao")

# test2_plugin = lightbulb.Plugin("Test2")
# @test2_plugin.command
# @lightbulb.option(
#     "user", "The user to lookup their maker ID", hikari.User, required=True
# )
# @lightbulb.command("getmakerid", description="Test command to try databasing.", auto_defer=True)
# @lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
# async def getmakerid(ctx: lightbulb.Context) -> None:
#     table = await dataManager.tableLookup(ctx.bot, 'user')
#     user = await dataManager.findUser(table, ctx.options.user.id)
#     await ctx.respond(user['makerid'])

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ping_plugin)
    bot.add_plugin(update_plugin)
    # bot.add_plugin(test_plugin)
    # bot.add_plugin(test2_plugin)