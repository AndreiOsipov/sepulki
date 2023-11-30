from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Shmurdik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Grymzik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Fufelnitsa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Sepulka(models.Model):
    hot = models.BooleanField()
    soft = models.BooleanField()
    square_or_small = models.TextField(choices=[('square','квадратная'), ('small', 'маленькая')])
    size = models.TextField(choices=[('XXS','XXS'),('XS','XS'),('S','S'),('M','M'),('L','L'),('XL','XL'),('XXL','XXL')])
    state = models.TextField(choices=[('C','создана'),('V','вакцинируется'),('P','обрабатывается напильником'), ('D','доставляется'), ('F', 'доставлена')], default='C')
    shmurdik = models.ForeignKey(Shmurdik, on_delete=models.CASCADE, related_name='sepulka')
    grymzik = models.OneToOneField(Grymzik, null=True, on_delete=models.SET_NULL, related_name='sepulka',default=None,blank=True)
    fufelnitsa = models.OneToOneField(Fufelnitsa, null=True, on_delete=models.SET_NULL, related_name='sepulka',default=None,blank=True)
    datetime_created = models.DateField()
    datetime_proccessd = models.DateField(null=True, blank=True)
    def get_grymzik_id_or_none(self):
        if not(self.grymzik is None):
            return self.grymzik.id