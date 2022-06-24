CREATE TABLE board (
    board_id INTEGER PRIMARY KEY AUTOINCREMENT,
    board_name VARCHAR(20) NOT NULL
);

CREATE TABLE clips (
    clip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    clip_type VARCHAR(10) NOT NULL,
    clip_data BLOB,
    board_id INTEGER NOT NULL,
    FOREIGN KEY (board_id) REFERENCES board(board_id)
);

