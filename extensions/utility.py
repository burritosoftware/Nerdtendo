import lightbulb
import os

utility_plugin = lightbulb.Plugin("Utility")

@utility_plugin.command
@lightbulb.command("ping", description="Get the bot's ping.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Pong! Latency: {ctx.bot.heartbeat_latency*1000:.2f}ms")

@utility_plugin.command
@lightbulb.command("update", description="Pulls the latest release from GitHub and updates the bot.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def update(ctx: lightbulb.Context) -> None:
    if str(ctx.author.id) != "261236127581601793":
        await ctx.respond(f"You do not have permission to perform this command. ID: {ctx.author.id}")
    else:
        output = os.popen('git pull').read()
        if output == "Already up to date.":
            await ctx.respond("Bot already up to date.")
        else:
            await ctx.respond("Update complete, sending PM2 the restart signal on Linux, or restart manually now.")
            if __name__ == "__main__":
                if os.name != "nt":
                    os.system("pm2 restart bot")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(utility_plugin)