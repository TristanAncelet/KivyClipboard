CREATE TABLE board (
    board_id INTEGER PRIMARY KEY AUTOINCREMENT,
    board_name VARCHAR(20) NOT NULL
);

--Making a default board so that we can still have the 
INSERT INTO board (board_name) VALUES ("Default");


-- The only things i am expecting to hold in these are images and text
CREATE TABLE clips (
    clip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    clip_type VARCHAR(10) NOT NULL,
    clip_data BLOB,
    board_id INTEGER NOT NULL,
    FOREIGN KEY (board_id) REFERENCES board(board_id)
);

INSERT INTO clips(clip_type, clip_data, board_id) VALUES 
    ("string", "I hope you enjoy this tool", 1); -- making a single insert into the default table



CREATE TABLE clip_ordering (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    clip_id INTEGER NOT NULL,
    board_id INTEGER NOT NULL,
    clip_index INTEGER NOT NULL,

    FOREIGN KEY (clip_id) REFERENCES clips(clip_id),
    FOREIGN KEY (board_id) REFERENCES board(board_id)
);

CREATE TABLE settings (
    clip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_name VARCHAR(20) NOT NULL,
    setting_type VARCHAR(10) NOT NULL,
    setting_value BLOB NOT NULL
);

INSERT INTO settings (setting_name, setting_type, setting_value) VALUES
    ("default_board", "string", "Default");
