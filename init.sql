CREATE DATABASE weather_db;

\c weather_db;

CREATE TABLE temperatures (
    id SERIAL PRIMARY KEY,
    date VARCHAR(50) NOT NULL,
    temperature FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/* Insert the data */
INSERT INTO temperatures (date, temperature) VALUES
('22-10-18-15-49-01', 19),
('22-10-18-15-49-51', 18),
('22-10-18-16-01-55', 19),
('22-10-18-16-01-56', 18),
('22-10-18-16-01-58', 18),
('22-10-18-16-02-00', 18),
('22-10-18-16-02-01', 20),
('22-10-18-16-21-28', 18);