from account.models import Offer, SalesDashboard
from celery import shared_task
from utils.notification_handlers.notification_manager import (
    notification_manager,
    notify,
)


@shared_task
def notification_success_offer(offer_id):
    offer = Offer.objects.get(id=offer_id)

    subject = (
        f"Hello {offer.deal.broker.owner.first_name}. "
        f"You put up for sale {offer.deal.asset.name}."
    )
    message = (
        f"user {offer.client.owner.username} "
        f"bought {offer.count} {offer.deal.asset.name} in {offer.timestamp}."
    )
    recipient = [f"{offer.deal.broker.owner.email}"]
    notification_manager(
        offer.deal.broker.id,
        tg_text=f"{subject}\n{message}\nbuyer email: {offer.client.owner.email}",
        tg_chat_id=offer.broker.account_contacts_data["tg_chat_id"],
        subject=subject,
        message=message,
        recipient=recipient,
    )


@shared_task
def notification_salesdashboard_soon_over_control(sale_id):
    sale = SalesDashboard.objects.get(id=sale_id)

    subject = (
        f"Hello {sale.broker.owner.first_name}. "
        f"You put up for sale {sale.asset.name}."
    )
    message = f"Your asset {sale.asset.name} soon will be over"
    recipient = f"{sale.broker.owner.email}"

    notification_manager(
        sale.broker.id,
        tg_text=f"{subject}\n{message}",
        tg_chat_id=sale.broker.account_contacts_data["tg_chat_id"],
        subject=subject,
        message=message,
        recipient=recipient,
    )


@shared_task
def notification_salesdashboard_is_over(sale_id):
    sale = SalesDashboard.objects.get(id=sale_id)

    subject = (
        f"Hello {sale.broker.owner.first_name}. "
        f"You put up for sale {sale.asset.name}."
    )
    message = f"Your asset {sale.asset.name} sold completely"
    recipient = f"{sale.broker.owner.email}"

    notification_manager(
        sale.broker.id,
        tg_text=f"{subject}\n{message}",
        tg_chat_id=sale.broker.account_contacts_data["tg_chat_id"],
        subject=subject,
        message=message,
        recipient=recipient,
    )


@shared_task
def common_notify_task(notification_type, account_id, **data):
    notify(notification_type, account_id, **data)
