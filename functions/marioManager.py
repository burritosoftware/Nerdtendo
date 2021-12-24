import hikari

async def getCourseInformation(bot, id):
    async with bot.d.aio_session.get(
        f"https://tgrcode.com/mm2/level_info/{id}"
    ) as response:
        res = await response.json()

        if response.ok and 'error' not in res:
            return(res)
        else:
            return(None)

async def createCourseEmbed(res):
    course_id = '-'.join(res['course_id'][i:i+3] for i in range(0, len(res['course_id']), 3))
    uploader_code = '-'.join(res['uploader']['code'][i:i+3] for i in range(0, len(res['uploader']['code']), 3))
    difficulty_name =  res['difficulty_name'].title()
    embed = (
        hikari.Embed(
            title=res['name'],
            description=res['description'],
            colour=0x26AEA0
        )
        .set_thumbnail("https://static.wikia.nocookie.net/supermariomaker2/images/d/d4/Course_World-0.png/revision/latest?cb=20200426215204")
        .set_author(name=course_id)
        .set_footer(
            text=f"Created by {res['uploader']['name']} | {uploader_code}",
            icon=res['uploader']['mii_image'],
        )
        .add_field("Likes", str(res['likes']), inline=True)
        .add_field("Boos", str(res['boos']), inline=True)
        .add_field("Clear Rate", res['clear_rate'], inline=True)
        .add_field("Difficulty", difficulty_name, inline=True)
        .add_field("Clears", str(res['clears']), inline=True)
        .add_field("Attempts", str(res['attempts']), inline=True)
        
        
    )
    return(embed)