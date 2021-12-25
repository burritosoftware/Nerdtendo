import hikari
import lightbulb
import functions.marioManager as marioManager
from lightbulb.ext import neon

search_plugin = lightbulb.Plugin("Search")

class fireMenu(neon.ComponentMenu):
    @neon.button("Open in course viewer", "viewer_button", hikari.ButtonStyle.PRIMARY, emoji="\N{MAG_RIGHT}")
    async def fire(self) -> None:
        await self.edit_msg("Course viewer coming soon!")

@search_plugin.command
@lightbulb.option(
    "id", "The course's ID to search for", str, required=True
)
@lightbulb.command(
    "search", "Search for a Super Mario Maker 2 course.",
    auto_defer=True
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def search(ctx: lightbulb.Context) -> None:
    id = ctx.options.id
    response = await marioManager.getCourseInformation(ctx.bot, id)
    if response != None:
        menu = fireMenu(ctx)
        embed = await marioManager.createCourseEmbed(response)
        resp = await ctx.respond(embed, components=menu.build())
        await menu.run(resp)
    else:
        await ctx.respond("Couldn't find a course by that ID!")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(search_plugin)