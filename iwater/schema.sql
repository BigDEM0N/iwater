DROP TABLE IF EXISTS app_user;

CREATE TABLE app_user
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT        NOT NULL,
    created_time  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status   INTEGER     NOT NULL DEFAULT 0
);
--插入初始用户 admin 密码 admin
INSERT INTO app_user(username, password, status)
    values ('admin', 'pbkdf2:sha256:260000$BMdY3jT0Y2ldxwPm$87e2965f39c4718410f4bd76829f46795960bbc77bd4ba7c80e23a417229e46e', 1);

