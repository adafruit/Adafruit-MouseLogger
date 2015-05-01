-- This creates a table with structure like:
-- id | timestamp | event_type

CREATE TABLE events(id INTEGER PRIMARY KEY, timestamp TEXT, value INTEGER, event_type INTEGER);

-- Event type will reference the id of a row in event_types - this lets us
-- extend the table later on to include more sensors.

CREATE TABLE event_types(id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO event_types (id, name) VALUES (1, 'motion');
INSERT INTO event_types (id, name) VALUES (2, 'trap');

-- You'd log a motion event, like the mouse nosing around the entrance
-- to the trap, with:
-- INSERT INTO events(timestamp, value, event_type) VALUES (DATETIME(), 1, 1);

-- And an increment of the trap-tipping count a few seconds later with:
-- INSERT INTO events(timestamp, value, event_type) VALUES (DATETIME(), 1, 2);
