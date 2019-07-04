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
    # Start by counting the number of posts for each person who has posted
    print("Getting user posts count...")
    people = tx.query("""
    SELECT poster_id, COUNT(*) AS num_of_posts
    FROM forums_posts
    GROUP BY poster_id
    ORDER BY poster_id
    """)
    for person in people:
        # Update the faux "post count" on profiles with the proper count
        print(f"User {person.poster_id} has {person.num_of_posts} posts")
        tx.query("""
        UPDATE `forums_users`
        SET `num_posts` = :num_posts
        WHERE `id` = :poster_id
        """,
        num_posts=person.num_of_posts,
        poster_id=person.poster_id)

    # Now we need to clear the post count for people who don't have any posts
    print("Get the members who haven't posted at all")
    people = tx.query("""
    SELECT id
    FROM forums_users
    WHERE id NOT IN (
        SELECT poster_id
        FROM forums_posts
        GROUP BY poster_id
        ORDER BY poster_id
    )
    ORDER BY id
    """)
    for person in people:
        print(f"User {person.id} has now has 0 posts")
        tx.query("""
        UPDATE `forums_users`
        SET `num_posts` = 0
        WHERE `id` = :poster_id
        """,
        poster_id=person.id)

    print("Successfully updated user post counts")
