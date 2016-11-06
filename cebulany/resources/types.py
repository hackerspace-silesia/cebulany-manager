from datetime import datetime

dt_type = lambda val: datetime.strptime(val, '%Y-%m-%d')
month_type = lambda val: datetime.strptime(val, '%Y-%m')
