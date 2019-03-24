-- Create a new column to store a user's avatar file name.
-- This permits migrating existing avatars as PunBB does not store
-- this information in the database at all.
ALTER TABLE `forums_users`
  ADD COLUMN `avatar_file` VARCHAR(15) NULL AFTER `karma`;
