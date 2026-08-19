from django.db import models


class Book(models.Model):
    class Cover(models.TextChoices):
        HARD = "HARD", "Hard"
        SOFT = "SOFT", "Soft"

    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    cover = models.CharField(max_length=4, choices=Cover.choices, default=Cover.HARD)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name="unique_book",
            )
        ]

    def __str__(self):
        return self.title
