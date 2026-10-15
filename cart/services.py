from django.db.models import Sum
from .models import Item

def get_top_purchaser():
    return (
        Item.objects
        .values("order__user__id", "order__user__username")
        .annotate(total_movies=Sum("quantity"))
        .order_by("-total_movies", "order__user__id")
        .first()
    )