from account.models import Offer, SalesDashboard
from celery import shared_task


@shared_task(default_retry_delay=10 * 60)
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
    recipient = [str(offer.deal.broker.owner.email)]

    print(f"{subject}\n{message}\n{recipient}")


@shared_task(default_retry_delay=10 * 60)
def notification_salesdashboard_soon_over_control(sale_id):
    sale = SalesDashboard.objects.get(id=sale_id)

    subject = (
        f"Hello {sale.broker.owner.first_name}. "
        f"You put up for sale {sale.asset.name}."
    )
    message = f"Your asset {sale.asset.name} soon will be over"
    recipient = [str(sale.broker.owner.email)]

    print(f"{subject}\n{message}\n{recipient}")


@shared_task(default_retry_delay=10 * 60)
def notification_salesdashboard_is_over(sale_id):
    sale = SalesDashboard.objects.get(id=sale_id)

    subject = (
        f"Hello {sale.broker.owner.first_name}. "
        f"You put up for sale {sale.asset.name}."
    )
    message = f"Your asset {sale.asset.name} sold completely"
    recipient = [str(sale.broker.owner.email)]

    print(f"{subject}\n{message}\n{recipient}")