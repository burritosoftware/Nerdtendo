from hikari.presences import Status
import lightbulb
import os
from subprocess import Popen
import hikari
import functions.dataManager as dataManager

bot_plugin = lightbulb.Plugin("Bot")

@bot_plugin.command
@lightbulb.command("ping", description="Get the bot's latency.", ephemeral=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f":ping_pong: **Pong!** Latency: {ctx.bot.heartbeat_latency*1000:.2f}ms")

@bot_plugin.command
@lightbulb.command("update", description="Pulls the latest source from GitHub and updates the bot.", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def update(ctx: lightbulb.Context) -> None:
    if str(ctx.author.id) != "261236127581601793":
        await ctx.respond(f"<:no:442206260151189518> You do not have permission to perform this command.")
    else:
        output = os.popen('git pull').read()
        if "Already up to date." in output:
            await ctx.respond("<:yes:459224261136220170> Bot already up to date.")
        else:
            ctx.bot.d.logger.info(f"Bot updated!\n\n{output}")
            await ctx.respond(f"<:yes:459224261136220170> **Update complete!** The bot will restart momentarily...\n\n```\n{output}\n```")
            await ctx.bot.update_presence(status=hikari.Status.IDLE, activity=hikari.Activity(name="Updating, please wait..."))
            if os.name != "nt":
                p = Popen(['pm2', 'restart', 'bot'])
                p.poll()

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(bot_plugin)