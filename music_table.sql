-- Схема БД музыкального сервиса

BEGIN;

-- 1) Базовые сущности

CREATE TABLE genre (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUEgit initgit initпшвыы
);

CREATE TABLE artist (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL
);

CREATE TABLE album (
    id           SERIAL PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    release_year INTEGER NOT NULL CHECK (release_year >= 1900)
);

CREATE TABLE track (
    id       SERIAL PRIMARY KEY,
    title    VARCHAR(200) NOT NULL,
    duration INTEGER NOT NULL CHECK (duration > 0),
    album_id INTEGER NOT NULL REFERENCES album(id) ON DELETE CASCADE
);

CREATE TABLE compilation (
    id           SERIAL PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    release_year INTEGER NOT NULL CHECK (release_year >= 1900)
);

-- 2) Таблицы-связки (M:N)

-- Исполнители <-> Жанры
CREATE TABLE artist_genre (
    artist_id INTEGER NOT NULL REFERENCES artist(id) ON DELETE CASCADE,
    genre_id  INTEGER NOT NULL REFERENCES genre(id)  ON DELETE CASCADE,
    PRIMARY KEY (artist_id, genre_id)
);

-- Альбомы <-> Исполнители
CREATE TABLE album_artist (
    album_id  INTEGER NOT NULL REFERENCES album(id)  ON DELETE CASCADE,
    artist_id INTEGER NOT NULL REFERENCES artist(id) ON DELETE CASCADE,
    PRIMARY KEY (album_id, artist_id)
);

-- Сборники <-> Треки
CREATE TABLE compilation_track (
    compilation_id INTEGER NOT NULL REFERENCES compilation(id) ON DELETE CASCADE,
    track_id       INTEGER NOT NULL REFERENCES track(id)       ON DELETE CASCADE,
    PRIMARY KEY (compilation_id, track_id)
);

COMMIT;