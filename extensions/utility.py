import lightbulb
import os
from subprocess import Popen

ping_plugin = lightbulb.Plugin("Ping")

@ping_plugin.command
@lightbulb.command("ping", description="Get the bot's ping.", ephemeral=True)
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
            await ctx.respond("Update complete! The bot will restart momentarily...")
            if os.name != "nt":
                p = Popen(['pm2', 'restart', 'bot'])
                p.poll()

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ping_plugin)
    bot.add_plugin(update_plugin)