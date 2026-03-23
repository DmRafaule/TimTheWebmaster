from django.db import models
from django.conf import settings


class BTCPayCrowdfundApp(models.Model):
    app_id = models.CharField(max_length=256, unique=True)
    project = models.ForeignKey(to=settings.BTCPAY_CROWDFUND_MODEL_TO_BIND, on_delete=models.CASCADE)
    language_code = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES,
        db_index=True
    )

    def __str__(self):
        return f"{self.project} ({self.language_code}) - {self.app_id}"

class BTCPayCrowdfundDonation(models.Model):
    email = models.ForeignKey(to=settings.BTCPAY_CROWDFUND_EMAIL_MODEL_TO_BIND, on_delete=models.CASCADE)
    app = models.ForeignKey(to=BTCPayCrowdfundApp, on_delete=models.CASCADE)
    invoice_id = models.CharField(max_length=256, help_text="An invoice's ID to bind to this email")
    
    class DonationStatus(models.IntegerChoices):
        NEW         = 0
        PROCESSING  = 1
        EXPIRED     = 2
        INVALID     = 3
        SETTLED     = 4
    status = models.IntegerField(choices=DonationStatus, default=DonationStatus.NEW)

    def __str__(self):
        return f"{self.email} {self.invoice_id}"