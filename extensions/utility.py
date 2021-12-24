import lightbulb
import os

ping_plugin = lightbulb.Plugin("Ping")

@ping_plugin.command
@lightbulb.command("ping", description="Get the bot's ping.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Pong! Latency: {ctx.bot.heartbeat_latency*1000:.2f}ms")

update_plugin = lightbulb.Plugin("Update")

@update_plugin.command
@lightbulb.command("update", description="Pulls the latest release from GitHub and updates the bot.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def update(ctx: lightbulb.Context) -> None:
    if str(ctx.author.id) != "261236127581601793":
        await ctx.respond(f"You do not have permission to perform this command. ID: {ctx.author.id}")
    else:
        output = os.popen('git pull').read()
        if "Already up to date." in output:
            await ctx.respond("Bot already up to date.")
        else:
            await ctx.respond("Update complete, sending PM2 the restart signal on Linux, or restart manually now.")
            if os.name != "nt":
                os.system("pm2 restart bot")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ping_plugin)
    bot.add_plugin(update_plugin)