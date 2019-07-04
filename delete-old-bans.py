import records


# Fill these in with proper credentials
DB_USERNAME = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_DBNAME = ""

# Connect to the database
print("Connecting to database...")
conn_str = "mysql+pymysql://{}:{}@{}/{}".format(
    DB_USERNAME,
    DB_PASSWORD,
    DB_HOST,
    DB_DBNAME
)
db = records.Database(conn_str)

with db.transaction() as tx:
    print("Getting outdated ban rules")
    bans = tx.query("""
    SELECT id
    FROM forums_bans
    WHERE username not IN (
    SELECT username FROM forums_users
    )
    """)
    for ban in bans:
        print(f"Deleting ban {ban.id}")
        tx.query("""
        DELETE FROM `forums_bans`
        WHERE `id` = :ban_id
        """,
        ban_id=ban.id)

    print("Successfully deleted outdated ban rules")
