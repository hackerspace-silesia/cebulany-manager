SELECT b.name budget_name, pt.name type_name, round(sum(p.cost), 2) total from budget b
join payment p on b.id = p.budget_id
join paymenttype pt on pt.id = p.payment_type_id
join "transaction" t on p.transaction_id = t.id
where strftime('%Y', t."date") == '2018'
group by b.id, pt.id