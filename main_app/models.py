from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
# Create your models here.
MASKS = (
    ('L', 'LAME'),
    ('S', 'SCARY'),
    ('F', 'FRIGHTENING')
)

# Create your models here.
class Character(models.Model):
  name= models.CharField(max_length=100)
  description = models.CharField(max_length=100)
  alias = models.TextField(max_length=250)
  origin = models.TextField(max_length=250)
  
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def unmasked_for_today(self):
    return self.unmasking_set.filter(date=date.today()).count() >= len(MASKS)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('detail', kwargs={'characters_id': self.id})

class Unmasked(models.Model):
  date = models.DateField('unmasking date')
  masks = models.CharField(
    max_length=1,
  
    choices=MASKS,
   
    default=MASKS[0][0]
  )
  
  character = models.ForeignKey(Character, on_delete=models.CASCADE)

  def __str__(self):
    
    return f"{self.get_masks_display()} on {self.date}"

  # change the default sort
  class Meta:
    ordering = ['-date']

class Photo(models.Model):
  url = models.CharField(max_length=200)
  character = models.ForeignKey(Character, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for characters_id: {self.characters_id} @{self.url}"



