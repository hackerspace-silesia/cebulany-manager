SELECT b.name, sum(p.cost) from budget b
join payment p on b.id = p.budget_id
join "transaction" t on p.transaction_id = t.id
where strftime('%Y', t."date") == '2018'
group by b.id