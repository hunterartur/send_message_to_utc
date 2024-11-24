from celery import shared_task
from datetime import datetime, timedelta

from myproject.db_config import session


@shared_task
def send_messages(start_hour):
    from myproject.models import Supplier, District, DistrictUtc
    from django.utils.timezone import now
    suppliers = filter(lambda a: not a.subscription_cancelled and not a.subscription_admin,
                       session.query(Supplier).all())
    for s in suppliers:
        print(s)
    # timezones = {3: 3, 7: 9}  # Данные о часовых поясах
    timezones = session.query(DistrictUtc).all()
    print(timezones)

    current_utc_time = now()
    for supplier in suppliers:
        district_id = supplier.district_id
        if district_id in timezones:
            utc_offset = timezones[district_id]
            local_time = current_utc_time + timedelta(hours=utc_offset)

            # Рассчитать время 10:00 следующего дня в локальном часовом поясе
            target_time = local_time.replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
            delay = (target_time - current_utc_time).total_seconds()

            # Запланировать отправку сообщения
            schedule_message.apply_async((supplier.phone, supplier.name), countdown=delay)


@shared_task
def schedule_message(phone, name):
    print(f"Sending message to {name} ({phone}) at {datetime.now()}")
