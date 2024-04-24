# Create a Mongita database with quotes and session information
import json
from mongita import MongitaClientDisk

quotes_data = [
    {"text":"The only thing we have to fear is fear itself.", "author":"Franklin D. Roosevelt", "owner":"Steve"},
    {"text":"Be yourself; everyone else is already taken.", "author":"Oscar Wilde", "owner":"Steve"},
    {"text":"To Each His Own", "author":"Mom", "owner":"mom"},
    {"text":"If life were predictable, it would cease to be life and be without flavor.", "author":"Eleanor Roosevelt", "owner":"Steve"},
]

# create a mongita client connection
client = MongitaClientDisk()

# create a quotes database
quotes_db = client.quotes_db

# create a quotes collection
quotes_collection = quotes_db.quotes_collection

# empty the collection
quotes_collection.delete_many({})

# put the quotes in the database
quotes_collection.insert_many(quotes_data)

# make sure the quotes are there
print("Quotes")
print(quotes_collection.count_documents({}))

# create a session database
session_db = client.session_db

# create a session collection
session_collection = session_db.session_collection

# empty the collection
session_collection.delete_many({})

print("Sessions")
print(session_collection.count_documents({}))