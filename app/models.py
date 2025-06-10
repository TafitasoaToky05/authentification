from django.db import models

from io import BytesIO
from django.core.files import File


# Create your models here.
class Material(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    reference = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, blank=False, null=False)
    stat = models.BooleanField(
        default=True
    )  # True for available, False for unavailable
    repere = models.BooleanField(default=False)  # True for repere, False for non-repere

    def __str__(self):
        return self.name

    # def generate_qr_code(self):
    #     data = f"Matériel: {self.name} | Réf: {self.reference} | Catégorie: {self.category}"
    #     qr = qrcode.make(data)
    #     buffer = BytesIO()
    #     qr.save(buffer, format='PNG')
    #     filename = f"material_{self.reference}.png"
    #     self.qr_code.save(filename, File(buffer), save=False)
    #     buffer.close()

    # def save(self, *args, **kwargs):
    #     if not self.qr_code:
    #         self.generate_qr_code()
    #     super().save(*args, **kwargs)
