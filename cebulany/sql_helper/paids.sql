select Sum(paidmonth.cost), strftime('%Y', "transaction"."date") from paidmonth
inner join "transaction" on paidmonth.transaction_id = "transaction".id
group by strftime('%Y', "transaction"."date")
order by strftime('%Y', "transaction"."date")