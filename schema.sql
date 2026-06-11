CREATE DATABASE IF NOT EXISTS web_data;
USE web_data;

CREATE TABLE IF NOT EXISTS events (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    created_at  DATETIME NOT NULL,   
    user_id     VARCHAR(64) NOT NULL,
    event_type  VARCHAR(64)  NOT NULL,
    
    -- for event_type "view"
    page_name   VARCHAR(64),

    -- for event_type "buy"
    purchase    VARCHAR(64),

    -- for event_type "error"
    error_code  INT

    
);

CREATE INDEX idx_event_type ON events (event_type);
CREATE INDEX idx_created_at ON events (created_at);