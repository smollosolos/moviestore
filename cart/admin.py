from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.urls import path

from .models import Order, Item
from .services import get_top_purchaser


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "admin/cart/order/change_list.html"

    def get_urls(self):
        custom_urls = [
            path(
                "purchase-leader/",
                self.admin_site.admin_view(self.purchase_leader),
                name="cart_order_purchase_leader",
            ),
        ]
        return custom_urls + super().get_urls()

    def purchase_leader(self, request):
        if not self.has_view_permission(request):
            raise PermissionDenied

        context = {
            **self.admin_site.each_context(request),
            "title": "Top Movie Purchaser",
            "opts": self.model._meta,
            "top_purchaser": get_top_purchaser(),
        }

        return TemplateResponse(
            request,
            "admin/cart/order/purchase_leader.html",
            context,
        )


admin.site.register(Item)