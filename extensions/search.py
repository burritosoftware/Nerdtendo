import lightbulb
import functions.marioManager as marioManager

search_plugin = lightbulb.Plugin("Search")

@search_plugin.command
@lightbulb.option(
    "code", "The course's code to search for", str, required=True
)
@lightbulb.command(
    "search", "Search for a Super Mario Maker 2 course.",
    auto_defer=True
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def search(ctx: lightbulb.Context) -> None:
    code = ctx.options.code
    response = await marioManager.getCourseInformation(ctx.bot, code)
    if response != None:
        embed = await marioManager.createCourseEmbed(response)
        await ctx.respond(embed)
    else:
        await ctx.respond("Couldn't find a course by that ID!")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(search_plugin)