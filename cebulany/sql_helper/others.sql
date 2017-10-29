select Sum(other.cost), strftime('%Y', "transaction"."date") from other
inner join "transaction" on other.transaction_id = "transaction".id
group by strftime('%Y', "transaction"."date")
order by strftime('%Y', "transaction"."date")