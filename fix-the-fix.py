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
    # Start by getting all botched trailer topics
    trailer_topics = tx.query("""
SELECT `id`, `first_post_id`
FROM `forums_topics`
WHERE  `first_post_id` != 0 AND
`subject` LIKE 'Trailer - %';
    """)

    for topic in trailer_topics:
        print(f"\nCurrent topic: {topic.id}")

        # Taking the first post ID, go to the posts table
        # and delete the unneeded OP that was generated
        print("Deleting bad OP...")
        tx.query("DELETE FROM `forums_posts` WHERE `id` = :id;",
                 id=topic.first_post_id
                 )

        # Finally, we go back to the original topic
        # and remove the link to the dead OP
        print("Disassociating bad OP with topic...")
        tx.query("UPDATE `forums_topics` SET `first_post_id` = 0 WHERE `id` = :id;",
                 id=topic.id
                 )

    print("Successfully removed bad OPs for trailer topics")
