select
	other.name, "transaction".name, other.cost, "date"
from other
join "transaction" on "transaction".id = transaction_id
where "date" >= "2016-01-01" and "date" <= "2016-12-31"
order by "date"