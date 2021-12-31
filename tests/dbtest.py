import dataset

# connecting to a SQLite database
db = dataset.connect('sqlite:///testdatabase.db')

# get a reference to the table 'user'
table = db['user']

print(table.find_one(name='Burrito#6743'))

# Insert a new record.
table.insert(dict(name='Burrito#6743', id=261236127581601793))

print(table.find_one(name='Burrito#6743'))