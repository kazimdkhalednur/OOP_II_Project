import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction as database_transaction
from django.db.models import F, Sum
from django.http import HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, View

from accounts.models import Information
from products.models import Cart
from utils import SSLCommerz

from .forms import OrderForm
from .models import OrderItem, Transaction


class CheckoutView(LoginRequiredMixin, FormView):
    form_class = OrderForm
    template_name = "orders/checkout.html"

    def dispatch(self, request, *args, **kwargs):
        if not Cart.objects.filter(user=request.user, is_checked=True).exists():
            messages.warning(request, "No product in cart. Please add product to cart.")
            return redirect("products:list")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        intial = {"save_address": False}
        if Information.objects.filter(user=self.request.user).exists():
            information = Information.objects.get(user=self.request.user)
            intial.update(
                {
                    "save_address": True,
                    "address": information.address,
                    "address_2": information.address_2,
                    "postal_code": information.postal_code,
                    "district": information.district,
                }
            )
        return intial

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            if "cartCheckout" in data:
                return JsonResponse(
                    {"checkout": True, "url": reverse("orders:checkout")}
                )
        except json.JSONDecodeError:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        with database_transaction.atomic():
            order = form.save(user=self.request.user)

            order_item = []
            for cart in (
                Cart.objects.select_related("product")
                .only(
                    "quantity",
                    "product__id",
                    "product__price",
                )
                .select_for_update()
                .filter(user=self.request.user, is_checked=True)
            ):
                order_item.append(
                    OrderItem(
                        product=cart.product,
                        quantity=cart.quantity,
                        total_price=cart.product.price * cart.quantity,
                    )
                )
            order_items = OrderItem.objects.bulk_create(order_item)
            order.items.set(order_items)

            transaction = Transaction.objects.create(
                order=order,
                amount=order.items.aggregate(total=Sum(F("total_price")))["total"],
            )

            payment = SSLCommerz()
            url = self.request.build_absolute_uri(reverse("orders:ipn"))
            payment.set_urls(
                success_url=url,
                fail_url=url,
                cancel_url=url,
                ipn_url=url,
            )

            response_data = payment.init_payment(transaction, order, self.request.user)

            if response_data["status"] == "FAILED":
                messages.error(self.request, response_data["failedreason"])
                return redirect("orders:checkout")
            elif response_data["status"] == "SUCCESS":
                transaction.sessionkey = response_data["sessionkey"]
                transaction.gateway_page_url = response_data["GatewayPageURL"]
                transaction.save()

            Cart.objects.filter(user=self.request.user, is_checked=True).delete()

        return HttpResponsePermanentRedirect(response_data["GatewayPageURL"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_list"] = (
            Cart.objects.select_related("product")
            .only(
                "quantity",
                "product__title",
                "product__price",
            )
            .filter(user=self.request.user, is_checked=True)
        )
        return context


@method_decorator(csrf_exempt, name="dispatch")
class OrderInstantPaymentNotificationView(View):
    def post(self, request, **kwargs):
        payment_data = request.POST

        if payment_data["status"] == "VALID":
            transaction = get_object_or_404(Transaction, id=payment_data["tran_id"])
            transaction.tran_date = payment_data["tran_date"]
            transaction.status = payment_data["status"]
            transaction.val_id = payment_data["val_id"]
            transaction.store_amount = payment_data["store_amount"]
            transaction.bank_tran_id = payment_data["bank_tran_id"]
            transaction.save()
            messages.success(request, "Order has been placed successfully.")
            return redirect("products:list")

        elif payment_data["status"] == "FAILED":
            transaction = get_object_or_404(Transaction, id=payment_data["tran_id"])
            transaction.status = payment_data["status"]
            transaction.save()
            messages.warning(request, "Order has been failed.")
            return redirect("products:list")

        elif payment_data["status"] == "CANCELLED":
            transaction = get_object_or_404(Transaction, id=payment_data["tran_id"])
            transaction.status = payment_data["status"]
            transaction.save()
            messages.warning(request, "Order has been canceled by you.")
            return redirect("products:list")

        elif payment_data["status"] == "UNATTEMPTED":
            transaction = get_object_or_404(Transaction, id=payment_data["tran_id"])
            transaction.status = payment_data["status"]
            transaction.save()
            messages.warning(request, "Order has been unattempted.")
            return redirect("products:list")

        elif payment_data["status"] == "EXPIRED":
            transaction = get_object_or_404(Transaction, id=payment_data["tran_id"])
            transaction.status = payment_data["status"]
            transaction.save()
            messages.warning(request, "Order has been expired.")
            return redirect("products:list")


class OrderVerifyView(View):
    def post(self, request, **kwargs):
        data = request.POST
        transaction = Transaction.objects.get(id=data["tran_id"])
        if transaction.check_valid_transaction():
            return
