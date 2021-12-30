import functools
import asyncio

# Running stuff asynchronously https://github.com/balkierode/assortedscripts/blob/master/python/blockex.py
def run_in_executor(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, lambda: f(*args, **kwargs))
    return inner

# Provide bot from an extension and the table name you want to lookup, and this will look it up and return it
def blockingTableLookup(bot, tablename):
    table = bot.d.db[f'{tablename}']
    return table

# Provide a table, and a dictionary entry to insert, and this will return the inserted table
def blockingTableInsert(table, dict):
    record = table.insert(dict)
    return record

# Provide a table and a userid, and this will return their object from the db
def blockingFindUser(table, id):
    record = table.find_one(id=id)
    return record

@run_in_executor
def tableLookup(bot, tablename):
    resp = blockingTableLookup(bot, tablename)
    return resp

@run_in_executor
def tableInsert(table, dict):
    resp = blockingTableInsert(table, dict)
    return resp

@run_in_executor
def findUser(table, id):
    resp = blockingFindUser(table, id)
    return resp