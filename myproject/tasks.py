from celery import shared_task
from datetime import datetime, timedelta, timezone

from myproject.db_config import session


@shared_task
def send_messages(start_hour):
    from myproject.models import Supplier, District, DistrictUtc
    from django.utils.timezone import now
    suppliers = list(filter(lambda a: not a.subscription_cancelled and not a.subscription_admin,
                            session.query(Supplier).all()))
    timezones = session.query(DistrictUtc).all()
    current_utc_time = now()
    for supplier in suppliers:
        district_id = supplier.district_id
        utc_offset = next(filter(lambda t: t.district_id == district_id, timezones)).utc
        local_time = current_utc_time + timedelta(hours=utc_offset)
        # Рассчитать время start_hour следующего дня в локальном часовом поясе
        target_time = local_time.replace(hour=int(start_hour), minute=0, second=0, microsecond=0) + timedelta(days=1)
        delay = (target_time - current_utc_time).total_seconds()
        # Запланировать отправку сообщения
        schedule_message.apply_async((supplier.phone, supplier.name), countdown=delay)


@shared_task
def schedule_message(phone, name):
    print(f"Sending message to {name} ({phone}) at {datetime.now()}")
