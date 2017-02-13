try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

import calendar
from datetime import datetime, timedelta

def current_calendar(year, month):
    c = calendar.Calendar(firstweekday=calendar.SUNDAY)
    return c.monthdatescalendar(year, month)

""" dayindex starts at 1 """
def day_instance(year, month, calendarday, dayindex):
    monthcal = current_calendar(year, month)
    return [day for week in monthcal for day in week if day.weekday() == calendarday and day.month == month][dayindex-1]

def next_day(date):
    return date + timedelta(days=1)

class Command(BaseCommand):
    help = "Load CSPC data into the db"

    def handle(self, **options):
        from schedule.models import Calendar
        from schedule.models import Event
        from schedule.models import Rule

        print("checking for existing data ...")
        try:
            cal = Calendar.objects.get(name="CSPC")
            print("It looks like you already have loaded this sample data, quitting.")
            import sys
            sys.exit(1)
        except Calendar.DoesNotExist:
            print("CSPC data not found in db.")
            print("Install it...")

        print("Create CSPC Calendar ...")
        cal = Calendar(name="CSPC", slug="cspc")
        cal.save()
        print("The CSPC Calendar is created.")
        print("Do we need to install the most common rules?")
        try:
            rule = Rule.objects.get(name="Daily")
        except Rule.DoesNotExist:
            print("Need to install the basic rules")
            rule = Rule(frequency="YEARLY", name="Yearly", description="will recur once every Year")
            rule.save()
            print("YEARLY recurrence created")
            rule = Rule(frequency="MONTHLY", name="Monthly", description="will recur once every Month")
            rule.save()
            print("Monthly recurrence created")
            rule = Rule(frequency="WEEKLY", name="Weekly", description="will recur once every Week")
            rule.save()
            print("Weekly recurrence created")
            rule = Rule(frequency="DAILY", name="Daily", description="will recur once every Day")
            rule.save()
            print("Daily recurrence created")
        print("Rules installed.")
        today = datetime.today()
        monthly_rule = Rule.objects.get(frequency="MONTHLY")
        weekly_rule = Rule.objects.get(frequency="WEEKLY")

        print("Create some events")
        second_saturday = day_instance(today.year, today.month, calendar.SATURDAY, 2)
        end_second_saturday = next_day(second_saturday)
        data = {
            'title': 'Power Play Mixed Tape',
            'start': datetime(second_saturday.year, second_saturday.month, second_saturday.day, 20, 0, 0),
            'end': datetime(end_second_saturday.year, end_second_saturday.month, end_second_saturday.day, 2, 0, 0),
            'end_recurring_period': datetime(today.year + 30, 6, 1, 0, 0),
            'rule': monthly_rule,
            'calendar': cal
        }
        event = Event(**data)
        event.save()

        third_friday = day_instance(today.year, today.month, calendar.FRIDAY, 3)
        end_third_friday = next_day(third_friday)
        data = {
            'title': 'Intro-PER-verted',
            'start': datetime(third_friday.year, third_friday.month, third_friday.day, 17, 0, 0),
            'end': datetime(third_friday.year, third_friday.month, third_friday.day, 2, 0, 0),
            'end_recurring_period': datetime(today.year + 20, 6, 1, 0, 0),
            'rule': monthly_rule,
            'calendar': cal
        }
        event = Event(**data)
        event.save()

        first_wednesday = day_instance(today.year, today.month, calendar.WEDNESDAY, 1)
        end_first_wednesday = next_day(first_wednesday)
        data = {
            'title': 'The Hump',
            'start': datetime(first_wednesday.year, first_wednesday.month, first_wednesday.day, 18, 0, 0),
            'end': datetime(end_first_wednesday.year, end_first_wednesday.month, end_first_wednesday.day, 0, 0, 0),
            'end_recurring_period': datetime(today.year + 20, 6, 1, 0, 0),
            'rule': weekly_rule,
            'calendar': cal
        }
        event = Event(**data)
        event.save()
