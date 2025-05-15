CREATE VIEW total_amount_per_day AS
SELECT
    c.name AS company_name,
    DATE(ch.created_at) AS day,
    SUM(ch.amount) AS total_amount
FROM
    charges ch
JOIN
    companies c ON ch.company_id = c.id
GROUP BY
    c.name, DATE(ch.created_at)
ORDER BY
    day, company_name;
