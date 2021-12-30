import hikari
import lightbulb
import os
import aiohttp
import re
import functions.marioManager as marioManager
from dotenv import load_dotenv
import dataset

# Loading .env values
load_dotenv()

# Ininitializing bot instance
bot = lightbulb.BotApp(token=os.getenv('TOKEN'), prefix='n!', banner=None, intents=hikari.Intents.ALL_UNPRIVILEGED, default_enabled_guilds=(173146091640848384,419367512262705152,755956418619637820,439591923070533652,))

# Create and close an aiohttp.ClientSession on start and stop of bot
@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.aio_session = aiohttp.ClientSession()
    bot.d.db = dataset.connect('sqlite:///database.db')

@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.aio_session.close()

#############################################
# SMM2 auto-code search                     #
#############################################
codeRegex = r"(([0-9]|[a-h]|[j-n]|[p-y]){3}(\-|\s)([0-9]|[a-h]|[j-n]|[p-y]){3}(\-|\s)([0-9]|[a-h]|[j-n]|[p-y]){3})"
@bot.listen()
async def on_message_create(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return

    codes = re.findall(codeRegex, event.content, flags=re.I | re.M)
    embeds = []
    if codes != []:
        if len(codes) > 5:
            await event.message.respond("Too many IDs in message, limit 5!")
        else:
            for code in codes:
                realcode = code[0]
                res = await marioManager.getCourseInformation(bot, realcode)
                if res != None or 'Maker':
                    await bot.rest.trigger_typing(event.get_channel())
                    embed = await marioManager.createCourseEmbed(res)
                    embeds.append(embed)
                elif res == 'Maker':
                    await bot.rest.trigger_typing(event.get_channel())
                    maker = await marioManager.getMakerInformation(bot, realcode)
                    embed = await marioManager.createMakerEmbed(maker)
                    embeds.append(embed)
            if embeds != []:
                await event.message.respond(embeds=embeds)

# Loading all extensions
bot.load_extensions_from("./extensions/", must_exist=True)

# uvloop for performance on UNIX systems
if os.name != "nt":
    import uvloop
    uvloop.install()

bot.run()