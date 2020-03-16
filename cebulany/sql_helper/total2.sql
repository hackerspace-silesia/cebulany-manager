SELECT 'total' "type", '2016-12-31' "day", round(sum(p.cost), 2) total from payment p
join "transaction" t on p.transaction_id = t.id
where t."date" <= '2016-12-31'
UNION ALL
SELECT 'total' "type", '2016-01-01' "day", round(sum(p.cost), 2) total from payment p
join "transaction" t on p.transaction_id = t.id
where t."date" <= '2016-01-01'
UNION ALL
SELECT 'total' "type", '2017-12-31' "day", round(sum(p.cost), 2) total from payment p
join "transaction" t on p.transaction_id = t.id
where t."date" <= '2017-12-31'
UNION ALL
SELECT 'total' "type", '2017-01-01' "day", round(sum(p.cost), 2) total from payment p
join "transaction" t on p.transaction_id = t.id
where t."date" <= '2017-01-01'