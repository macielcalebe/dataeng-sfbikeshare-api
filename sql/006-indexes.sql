CREATE INDEX idx_status_time_btree
    ON status USING btree(time);