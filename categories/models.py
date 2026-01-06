from django.db import models
from django.conf import settings


class CategoryType(models.TextChoices):
    EXPENSE = "expense", "Expense"
    INCOME = "income", "Income"


class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    type = models.CharField(max_length=7, choices=CategoryType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["type", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name", "type"],
                name="category_unique_per_user",
            )
        ]

    def save(self, *args, **kwargs):
        self.name = (self.name or "").strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
