SELECT b.name budget_name, pt.name type_name, t."date", t.title trans_title, round(sum(p.cost), 2) total from budget b
join payment p on b.id = p.budget_id
join paymenttype pt on pt.id = p.payment_type_id
join "transaction" t on p.transaction_id = t.id
where strftime('%Y', t."date") == '2018' and budget_name = "GRANT SZKOŁY"
group by p.id
order by t."date"