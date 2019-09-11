from django.db import models

# Create your models here.


class Todo(models.Model):
    """Model definition for Todo."""

    title = models.CharField(max_length=150)
    due_date = models.DateField()

    def __str__(self):
        """Unicode representation of Todo."""
        return self.title
