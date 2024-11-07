SELECT 'payments cost' label, round(sum(p.cost), 2) total from "transaction" t
join payment p on p.transaction_id = t.id
where strftime('%Y', t."date") == '2019'
UNION ALL 
SELECT 'transactions cost' label, round(sum(t.cost), 2) total from "transaction" t
where strftime('%Y', t."date") == '2019'