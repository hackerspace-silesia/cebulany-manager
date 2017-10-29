select 
	*,
	required_months - payed_months as diff
from (
	select
		member.name,
		member.join_date,
		count(paidmonth.id) as payed_months,
		(
			2017 * 12 + 5
			- (
				strftime('%Y', max(member.join_date, '2015-06-01')) * 12
				+ strftime('%m', max(member.join_date, '2015-06-01'))
			)
		) as required_months
	from member
	outer join paidmonth on paidmonth.member_id = member.id
	where paidmonth.date >= max(member.join_date, '2015-06-01')
	and member.is_active = 1
	group by member.id
) order by diff