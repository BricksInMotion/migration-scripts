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
    # Get the member who are banned but without posts
    print("Getting banned members without posts")
    people = tx.query("""
    SELECT forums_users.id
    FROM forums_bans
    JOIN forums_users ON forums_bans.username = forums_users.username
    WHERE forums_bans.username IN (
      SELECT username FROM forums_users
    )
    AND num_posts = 0
    ORDER BY forums_users.id
    """)
    for person in people:
        # Delete the people
        print(f"Deleting banned member {person.id}")
        tx.query("""
        DELETE FROM `forums_users`
        WHERE `id` = :poster_id
        """,
        poster_id=person.id)

    print("Successfully deleted banned members without posts")
