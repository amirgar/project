docker compose down --remove-orphans
docker compose up --build


SELECT * 
FROM (
    SELECT 
        ROW_NUMBER() OVER (
            PARTITION BY window 
            ORDER BY count DESC
        ) AS row_number, 
        name, 
        value,
        type,
        ts,
        count
    FROM (
        SELECT 
            name, 
            value,
            type,
            ts,
            count
            hop(INTERVAL '10' SECOND, INTERVAL '5' HOUR) AS window,
            COUNT(*) AS count 
        FROM connect 
        GROUP BY name, value, window
    ) AS grouped_bids
) AS ranked_bids 



CREATE TABLE act_tool_data (
    name String CODEC(LZ4),
    value String CODEC(LZ4),  -- Use LZ4 compression for the value column
    type String CODEC(LZ4),
    ts DateTime CODEC(DoubleDelta) -- Use LZ4 compression for the ts column as an integer
) ENGINE = MergeTree()
PARTITION BY toStartOfHour(toDateTime(ts))  -- Partition by the start of the hour of the timestamp
ORDER BY (name, ts)  -- Order by name first, then by timestamp for efficient querying
SETTINGS index_granularity = 8192;  -- Adjust index granularity as needed
