# migration scripts
> Scripts to use for migration

## Order of execution
1. `pip install -r requirements.txt`
1. `make-user-avatar-file.sql`
1. `import-avatars.py`
1. `migrate-forum.rb`
