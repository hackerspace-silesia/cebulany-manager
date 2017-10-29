select Sum("transaction".cost), strftime('%Y', "transaction"."date") from "transaction"
group by strftime('%Y', "transaction"."date")
order by strftime('%Y', "transaction"."date")