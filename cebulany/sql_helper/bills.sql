select -Sum(bill.cost), strftime('%Y', "transaction"."date") from bill
inner join "transaction" on bill.transaction_id = "transaction".id
group by strftime('%Y', "transaction"."date")
order by strftime('%Y', "transaction"."date")