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
    # Start by getting all the trailer topics
    orphaned_topics = tx.query("""
SELECT `id`
FROM `forums_topics`
WHERE `first_post_id` = 0 AND
`subject` LIKE 'Trailer - %';
    """)

    for topic in orphaned_topics:
        print(f"\nCurrent topic: {topic.id}")

        # Taking the topic ID, go to the posts table, find
        # the topic post for this trailer, and get its ID and the user ID
        print("Getting OP information...")
        op_info = tx.query("""
SELECT `id`, `poster_id`
FROM `forums_posts`
WHERE `topic_id` = :topic_id
ORDER BY `id` ASC;
        """, topic_id=topic.id).first()

        # Now we go back to the topic listing and
        # set the first post ID column to the actual ID
        print("Associating OP with topic...")
        tx.query("""
UPDATE `forums_topics`
SET `first_post_id` = :first_post_id
WHERE `id` = :id;""",
                 first_post_id=op_info.id,
                 id=topic.id)

        # Finally, go to this user and increase their post count
        print("Updating user's post count...")
        tx.query("""
UPDATE `forums_users`
SET `num_posts` = `num_posts` + 1
WHERE `id` = :user_id;
""", user_id=op_info.poster_id)

    print("Successfully linked OPs to trailer topics")
