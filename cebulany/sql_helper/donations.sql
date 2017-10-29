select Sum(donation.cost), strftime('%Y', "date") from donation
inner join "transaction" on donation.transaction_id = "transaction".id
group by strftime('%Y', "transaction"."date")
order by strftime('%Y', "transaction"."date")