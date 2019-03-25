import os
import records


# Fill these in with proper credentials and file path
DB_USERNAME = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_DBNAME = ""
AVATAR_FILES_PATH = ""


# Connect to the database
print("Connecting to database...")
conn_str = "mysql+pymysql://{}:{}@{}/{}".format(
    DB_USERNAME,
    DB_PASSWORD,
    DB_HOST,
    DB_DBNAME
)
db = records.Database(conn_str)

# The possible image file types
file_types = [".jpg", ".png", ".gif"]

# Build a list of all the avatars
print("Collecting avatars...")
avatars = []
all_files = os.listdir(AVATAR_FILES_PATH)
for f in all_files:
    name, ext = os.path.splitext(f)
    if ext in file_types:
        avatars.append({
            "name": name,
            "ext": ext
        })


# Insert the avatars into the database
# using a transaction, of course, to ensure everything works
print("Importing avatars...")
with db.transaction() as tx:
    for avatar in avatars:
        tx.query("""
UPDATE `forums_users`
SET `avatar_file` = :avatar_file
WHERE `id` = :user_id;""",
            avatar_file=f"{avatar['name']}{avatar['ext']}",
            user_id=avatar['name']
        )
    print("Successfully imported avatars")
