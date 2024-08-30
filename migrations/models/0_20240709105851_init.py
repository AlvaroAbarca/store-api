from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(1024) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "is_verified" BOOL NOT NULL  DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "short_name" VARCHAR(255),
    "full_name" VARCHAR(255)
);
CREATE INDEX IF NOT EXISTS "idx_users_email_133a6f" ON "users" ("email");
CREATE TABLE IF NOT EXISTS "orders" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    "payment_type" VARCHAR(10) NOT NULL,
    "voucher" VARCHAR(50) NOT NULL,
    "subtotal" DECIMAL(10,2) NOT NULL,
    "discount" DECIMAL(10,2) NOT NULL,
    "total" DECIMAL(10,2) NOT NULL,
    "extra_data" JSONB,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "orders"."uuid" IS 'This is a username';
COMMENT ON COLUMN "orders"."status" IS 'CANCELED: CANCELED\nPENDING: PENDING\nSTARTED: STARTED\nIN_PROGRESS: IN_PROGRESS\nCOMPLETED: COMPLETED\nFINISHED: FINISHED\nALL_DISCOUNT: ALL_DISCOUNT';
COMMENT ON COLUMN "orders"."payment_type" IS 'DEBIT: DEBIT\nCREDIT: CREDIT\nCASH: CASH\nOTHER: OTHER\nNONE: NONE';
COMMENT ON TABLE "orders" IS 'The Order model';
CREATE TABLE IF NOT EXISTS "products" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "is_billable" BOOL NOT NULL  DEFAULT True,
    "price" DECIMAL(10,2) NOT NULL  DEFAULT 0,
    "image" TEXT,
    "code" VARCHAR(50),
    "barcode" VARCHAR(50),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "products"."name" IS 'This is a username';
COMMENT ON TABLE "products" IS 'The Product model';
CREATE TABLE IF NOT EXISTS "orderproducts" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "quantity" SMALLINT NOT NULL  DEFAULT 0,
    "order_id" INT NOT NULL REFERENCES "orders" ("id") ON DELETE RESTRICT,
    "product_id" INT NOT NULL REFERENCES "products" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
