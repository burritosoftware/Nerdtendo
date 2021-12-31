import hikari
import lightbulb
import functions.marioManager as marioManager
import functions.dataManager as dataManager

async def addOrUpdateUser(bot, id, makerid) -> None:
    table = await dataManager.tableLookup(bot, 'user')
    user = await dataManager.findUser(table, id)
    if user == None:
        await dataManager.tableInsert(table, dict(id=id, makerid=makerid))
        return(True)
    else:
        await dataManager.tableUpdate(table, dict(id=id, makerid=makerid), ['id'])
        return(False)

cw_plugin = lightbulb.Plugin("Course World")
@cw_plugin.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option(
    "makerid", "The maker ID to add to the database", str, required=True
)
@lightbulb.command("setmakerid", description="Sets your maker ID to allow others to look up your profile.", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def setmakerid(ctx: lightbulb.Context) -> None:
    status = await addOrUpdateUser(bot=ctx.bot, id=ctx.author.id, makerid=ctx.options.makerid)
    if status:
        await ctx.respond("<:yes:459224261136220170> Added your ID to the database!")
    else:
        await ctx.respond("<:yes:459224261136220170> Updated your ID in the database!")

@cw_plugin.command
@lightbulb.add_cooldown(length=2, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option(
    "user", "The user to lookup their maker profile", hikari.User, required=True
)
@lightbulb.command("lookup", description="Looks up a user's maker profile.", auto_defer=False)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def getmakerid(ctx: lightbulb.Context) -> None:
    table = await dataManager.tableLookup(ctx.bot, 'user')
    user = await dataManager.findUser(table, ctx.options.user.id)
    if user != None:
        await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
        maker = await marioManager.getMakerInformation(ctx.bot, user['makerid'])
        if maker != None:
            embed = await marioManager.createMakerEmbed(maker)
            await ctx.respond(embed)
        else:
            await ctx.respond("<:no:442206260151189518> This user has an invalid ID set. Ask them to set their ID again.")
    else:
        await ctx.respond("<:no:442206260151189518> This user does not have their maker profile set.", flags=hikari.MessageFlag.EPHEMERAL)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(cw_plugin)