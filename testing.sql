
SELECT m.body, m.vendor_id, v.business_name, MAX(m.time_sent)
FROM weddingapi_message m
JOIN weddingapi_vendor v ON m.vendor_id = v.id
GROUP BY vendor_id

SELECT m.id, m.body, m.vendor_id, m.sender_id, m.host_id,
                u.username, MAX(m.time_sent)
            FROM weddingapi_message m
            JOIN weddingapi_host h ON m.host_id = h.id
            JOIN auth_user u ON h.user_id = u.id
            GROUP BY host_id
            


SELECT id, MAX(time_sent), host_id, body
FROM (SELECT m.id, m.body, m.vendor_id, m.sender_id, m.host_id,
        u.username host_username, m.time_sent
FROM weddingapi_message m
JOIN weddingapi_host h ON m.host_id = h.id
JOIN auth_user u ON h.user_id = u.id
WHERE m.vendor_id IS 2)
GROUP BY host_id

SELECT m.id, m.body, m.vendor_id, m.sender_id, m.host_id,
                u.username host_username, MAX(m.time_sent)
            FROM weddingapi_message m
            JOIN weddingapi_host h ON m.host_id = h.id
            JOIN auth_user u ON h.user_id = u.id
            WHERE m.vendor_id IS 2
            GROUP BY host_id

SELECT * FROM weddingapi_vendor WHERE business_name IS "Used Hat"
SELECT * FROM authtoken_token WHERE user_id IS 182
SELECT * FROM auth_user WHERE id IS 182