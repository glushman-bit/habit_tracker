import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message

logger = logging.getLogger(__name__)

@shared_task
def send_habit_reminders():
    """Задача для периодической отправке уведомлений в телеграм."""

    now = timezone.localtime(timezone.now())
    correct_date = now.date()
    correct_time = now.time().replace(second=0, microsecond=0)

    habits = Habit.objects.filter(
        is_pleasant=False,
        date_time__day=correct_date.day,
        date_time__hour=correct_time.hour,
        date_time__minute=correct_time.minute,
        owner__tg_chat_id__isnull=False,
    )

    if not habits:
        logger.info("Привычки не найдены!")
        return

    for habit in habits:
        delta_date = habit.date_time + timedelta(days=habit.periodicity)
        message = f"Напоминание! Вы обещали {habit.action} в {habit.date_time.strftime('%H:%M')} {habit.place}."
        send_telegram_message(chat_id=habit.owner.tg_chat_id, message=message)

        logger.info(f"Напоминание отправлено: {habit.owner.tg_chat_id}")
        habit.date_time = delta_date
        habit.save()
