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
            await self.edit_msg(":repeat: Course viewer coming soon!")
        elif button.custom_id == "delete_button":
            await self.context.event.message.delete()

@search_plugin.command
@lightbulb.add_cooldown(length=2, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option(
    "id", "The course/maker's ID to search for", str, required=True
)
@lightbulb.command(
    "search", "Searches for a Super Mario Maker 2 course/maker.",
    auto_defer=False
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def search(ctx: lightbulb.Context) -> None:
    id = ctx.options.id
    course = await marioManager.getCourseInformation(ctx.bot, id)
    if course != 'Maker' and course != None:
        await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
        menu = levelMenu(ctx)
        embed = await marioManager.createCourseEmbed(course)
        resp = await ctx.respond(embed, components=menu.build())
        await menu.run(resp)
    elif course == 'Maker':
        maker = await marioManager.getMakerInformation(ctx.bot, id)
        if maker != None:
            await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
            embed = await marioManager.createMakerEmbed(maker)
            await ctx.respond(embed)
        else:
            await ctx.respond("<:no:442206260151189518> Couldn't find a course/maker by that ID!", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond("<:no:442206260151189518> Couldn't find a course/maker by that ID!", flags=hikari.MessageFlag.EPHEMERAL)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(search_plugin)