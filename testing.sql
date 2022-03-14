
SELECT m.body, m.vendor_id, v.business_name, MAX(m.time_sent)
FROM weddingapi_message m
JOIN weddingapi_vendor v ON m.vendor_id = v.id
GROUP BY vendor_id