import records


# Fill these in with proper credentials
DB_USERNAME = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_DBNAME = ""

# Define the user details used for making new OPs
OP_USER_ID = 141084
OP_USER_NAME = "Mouldy [BOT]"
OP_USER_IP = '127.0.0.1'
OP_USER_MSG = "[b]This post has been deleted.[/b]"


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
    # Start by getting the newest post ID
    newest_post_id = tx.query("""
SELECT MAX(forums_posts.id) AS `newest_post_id` FROM `forums_posts`;
    """).first().newest_post_id
    print(f"The newest post ID is {newest_post_id}")

    # Next, get all the orphaned topics
    orphaned_topics = tx.query("""
SELECT `id`, `posted`
FROM `forums_topics`
WHERE `first_post_id` = 0 AND
`subject` NOT LIKE 'Trailer - %';
    """)

    for topic in orphaned_topics:
        print(f"\nCurrent topic: {topic.id}")

        # Taking the topic, go to the posts table and fabricate an OP,
        # setting it's ID to the newest post ID + 1,
        # assigning the post to a specially created user,
        # giving the new OP the topic date posted,
        # and associating it with the topic
        newest_post_id += 1
        print(f"The next post ID will be {newest_post_id}")
        print("Creating new OP...")
        tx.query("""
INSERT INTO `forums_posts` (
`id`, `poster`, `poster_id`, `poster_ip`, `message`, `posted`, `topic_id`
) VALUES (
    :id, :poster, :poster_id, :poster_ip, :message, :posted, :topic_id
);
        """,
        id=newest_post_id,
        poster=OP_USER_NAME,
        poster_id=OP_USER_ID,
        poster_ip=OP_USER_IP,
        message=OP_USER_MSG,
        posted=topic.posted,
        topic_id=topic.id
        )

        # Finally, we go back to the original topic and
        # set the OP ID column to our newly fabricated OP
        tx.query("""
UPDATE `forums_topics`
SET `first_post_id` = :first_post_id
WHERE `id` = :id;""",
            first_post_id=newest_post_id,
            id=topic.id
        )
        print("Associating new OP with topic...")

    print("Successfully created new OPs for orphaned topics")
