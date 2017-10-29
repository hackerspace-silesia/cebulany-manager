select -Sum("transaction".cost), strftime('%Y', "transaction"."date") from "transaction"
where "transaction".cost < 0
group by strftime('%Y', "transaction"."date")
order by strftime('%Y', "transaction"."date")