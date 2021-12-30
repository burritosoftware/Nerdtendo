import dataset

# connecting to a SQLite database
db = dataset.connect('sqlite:///mydatabase.db')

# get a reference to the table 'user'
table = db['user']

# Insert a new record.
table.insert(dict(name='Burrito#6743', id=261236127581601793))