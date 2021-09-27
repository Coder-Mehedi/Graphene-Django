from django.db import models
from category.models import Category

# Create your models here.
class Book(models.Model):
  title = models.CharField(max_length=50)
  description = models.TextField()
  category = models.ForeignKey(Category, related_name='books', on_delete=models.CASCADE, default=None, null=True, blank=True)

  def __str__(self) -> str:
      return self.title
