import hikari

async def getCourseInformation(bot, id):
    async with bot.d.aio_session.get(
        f"https://tgrcode.com/mm2/level_info/{id}"
    ) as response:
        res = await response.json()

        if response.ok and 'error' not in res:
            return(res)
        elif res['error'] == 'Code corresponds to a maker':
            return('Maker')
        else:
            return(None)

async def getMakerInformation(bot, id):
    async with bot.d.aio_session.get(
        f"https://tgrcode.com/mm2/user_info/{id}"
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
        .set_thumbnail(f"https://tgrcode.com/mm2/level_thumbnail/{course_id}")
        .set_image(f"https://tgrcode.com/mm2/level_entire_thumbnail/{course_id}")
        .set_author(name=course_id, icon="https://static.wikia.nocookie.net/supermariomaker2/images/d/d4/Course_World-0.png/revision/latest?cb=20200426215204")
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

async def createMakerEmbed(res):
    maker_id = '-'.join(res['code'][i:i+3] for i in range(0, len(res['code']), 3))
    embed = (
        hikari.Embed(
            title=res['name'],
            description=res['pose_name'],
            colour=0x4151B1
        )
        .set_thumbnail(res['mii_image'])
        .set_author(name=maker_id, icon="https://static.wikia.nocookie.net/supermariomaker2/images/d/d4/Course_World-0.png/revision/latest?cb=20200426215204")
        .add_field("Likes", str(res['likes']), inline=True)
        .add_field("Course Plays", str(res['courses_played']), inline=True)
        .add_field("Course Clears", res['courses_cleared'], inline=True)
        .add_field("Course Attempts", str(res['courses_attempted']), inline=True)
        .add_field("Course Deaths", str(res['courses_deaths']), inline=True)
        .set_footer(
            text=f"Last active on {res['last_active_pretty']}"
        )
        
    )
    return(embed)