CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 96ee93975f8a

INSERT INTO alembic_version (version_num) VALUES ('96ee93975f8a') RETURNING version_num;

-- Running upgrade 96ee93975f8a -> a69c80be508b

CREATE TABLE ppx_storage_var (
    id INTEGER NOT NULL, 
    "key" VARCHAR NOT NULL, 
    val VARCHAR DEFAULT '' NOT NULL, 
    remark VARCHAR DEFAULT '' NOT NULL, 
    created_at DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), 
    updated_at DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), 
    PRIMARY KEY (id)
);

CREATE INDEX ix_ppx_storage_var_key ON ppx_storage_var ("key");

UPDATE alembic_version SET version_num='a69c80be508b' WHERE alembic_version.version_num = '96ee93975f8a';

-- Running upgrade a69c80be508b -> 28a1b89eeb11

CREATE TABLE platform (
    id INTEGER NOT NULL, 
    name VARCHAR(80) NOT NULL, 
    comment VARCHAR(255), 
    created_at DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), 
    updated_at DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), 
    PRIMARY KEY (id), 
    UNIQUE (name)
);

CREATE TABLE platform_alias (
    id INTEGER NOT NULL, 
    platform_id INTEGER NOT NULL, 
    name VARCHAR(80) NOT NULL, 
    comment VARCHAR(255), 
    created_at DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), 
    updated_at DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), 
    PRIMARY KEY (id)
);

CREATE TABLE raw_password (
    id INTEGER NOT NULL, 
    raw_password VARCHAR(80) NOT NULL, 
    comment VARCHAR(255), 
    created_at DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), 
    updated_at DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), 
    PRIMARY KEY (id)
);

CREATE TABLE rule (
    id INTEGER NOT NULL, 
    name VARCHAR(80) NOT NULL, 
    comment VARCHAR(255), 
    min_length INTEGER, 
    max_length INTEGER, 
    lower_count INTEGER, 
    upper_count INTEGER, 
    number_count INTEGER, 
    special_count INTEGER, 
    is_deprecated BOOLEAN, 
    created_at DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), 
    updated_at DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), 
    PRIMARY KEY (id), 
    UNIQUE (name)
);

CREATE TABLE user (
    id VARCHAR(36) NOT NULL, 
    name VARCHAR(80) NOT NULL, 
    password VARCHAR(80) NOT NULL, 
    comment VARCHAR(255), 
    salt VARCHAR(80), 
    is_rule BOOLEAN, 
    is_deprecated BOOLEAN, 
    created_at DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), 
    updated_at DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), 
    PRIMARY KEY (id)
);

UPDATE alembic_version SET version_num='28a1b89eeb11' WHERE alembic_version.version_num = 'a69c80be508b';

