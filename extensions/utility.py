import lightbulb

utility_plugin = lightbulb.Plugin("Utility")

@utility_plugin.command
@lightbulb.command("ping", description="Get the bot's ping.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Pong! Latency: {ctx.bot.heartbeat_latency*1000:.2f}ms")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(utility_plugin)