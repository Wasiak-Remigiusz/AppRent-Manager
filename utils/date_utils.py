import calendar
from datetime import date, timedelta


def get_months_between_dates (start_date, end_date, payment_due_date):
    
    if isinstance(start_date, str):
        start_date = date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = date.fromisoformat(end_date)
        
    if isinstance(payment_due_date, str):
        payment_due_date = int(payment_due_date)
        
    
    months_dict = {}
    iterated_date = start_date.replace(day=1)
    
    while iterated_date <= end_date.replace(day=1):
        
        # Find the last day of the month
        _, last_day = calendar.monthrange(iterated_date.year, iterated_date.month)
        
        # Adjust the payment due date
        if payment_due_date > last_day:
            due_date = date(iterated_date.year, iterated_date.month, last_day)
        else:
            due_date = date(iterated_date.year, iterated_date.month, payment_due_date)
        
        months_dict[iterated_date.strftime("%Y-%m-%d")] = due_date.strftime("%Y-%m-%d")
        
        
        next_month = iterated_date.month % 12 + 1
        year_month = iterated_date.year + ( iterated_date.month // 12)
        iterated_date = iterated_date.replace(year= year_month , month = next_month)
        
    return months_dict
    

