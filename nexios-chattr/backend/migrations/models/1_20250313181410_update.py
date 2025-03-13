from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "chatentity" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "is_group" INT NOT NULL DEFAULT 0
);
        CREATE TABLE IF NOT EXISTS "messages" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "message_type" VARCHAR(50) NOT NULL,
    "content" TEXT,
    "media_url" TEXT,
    "status" VARCHAR(20) NOT NULL DEFAULT 'sent',
    "is_deleted" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "chat_id" CHAR(36) NOT NULL REFERENCES "chatentity" ("id") ON DELETE CASCADE,
    "receiver_id" INT NOT NULL REFERENCES "userentity" ("id") ON DELETE CASCADE,
    "reply_to_id" CHAR(36) REFERENCES "messages" ("id") ON DELETE SET NULL,
    "sender_id" INT NOT NULL REFERENCES "userentity" ("id") ON DELETE CASCADE
);
        CREATE TABLE "chatentity_userentity" (
    "chatentity_id" CHAR(36) NOT NULL REFERENCES "chatentity" ("id") ON DELETE CASCADE,
    "userentity_id" INT NOT NULL REFERENCES "userentity" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "chatentity_userentity";
        DROP TABLE IF EXISTS "chatentity";
        DROP TABLE IF EXISTS "messages";"""
