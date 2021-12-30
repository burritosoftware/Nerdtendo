import hikari
import lightbulb
import functions.marioManager as marioManager
from lightbulb.ext import neon

search_plugin = lightbulb.Plugin("Search")

class levelMenu(neon.ComponentMenu):
    @neon.button("", "delete_button", hikari.ButtonStyle.DANGER, emoji="🗑️")
    @neon.button("Open in course viewer", "viewer_button", hikari.ButtonStyle.PRIMARY, emoji="🔎")
    @neon.button_group()
    async def buttonPanel(self, button: neon.Button) -> None:
        if button.custom_id == "viewer_button":
            await self.edit_msg("Course viewer coming soon!", flags=hikari.MessageFlag.EPHEMERAL)
        elif button.custom_id == "delete_button":
            await self.edit_msg("Self-deletion coming soon!")

@search_plugin.command
@lightbulb.option(
    "id", "The course's ID to search for", str, required=True
)
@lightbulb.command(
    "search", "Search for a Super Mario Maker 2 course or maker.",
    auto_defer=True
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def search(ctx: lightbulb.Context) -> None:
    id = ctx.options.id
    course = await marioManager.getCourseInformation(ctx.bot, id)
    if course != 'Maker':
        menu = levelMenu(ctx)
        embed = await marioManager.createCourseEmbed(course)
        resp = await ctx.respond(embed, components=menu.build())
        await menu.run(resp)
    elif course == 'Maker':
        maker = await marioManager.getMakerInformation(ctx.bot, id)
        embed = await marioManager.createMakerEmbed(maker)
        await ctx.respond(embed)
    else:
        await ctx.respond("Couldn't find a course or maker by that ID!")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(search_plugin)