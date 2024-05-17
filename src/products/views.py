from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, View

from .forms import CartForm
from .models import Cart, Product


class ProductsView(ListView):
    model = Product
    paginate_by = 16

    def get_queryset(self):
        return Product.objects.published().select_related("category")


class ProductView(DetailView):
    model = Product

    def get_queryset(self):
        return (
            Product.objects.published()
            .select_related("category")
            .prefetch_related("images")
        )

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in for adding cart")
            return redirect("accounts:login")

        form = CartForm(request.POST)
        if form.is_valid():
            product_slug = form.cleaned_data["product_slug"]
            quantity = form.cleaned_data["quantity"]
            cart, created = Cart.objects.get_or_create(
                product=Product.objects.get(slug=product_slug),
                user=request.user,
                defaults={"quantity": quantity},
            )
            if created:
                messages.success(request, "Product added to cart")
            else:
                cart.quantity = form.cleaned_data["quantity"]
                cart.save(update_fields=["quantity"])
                messages.success(request, "Cart already added")
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CartForm(initial={"product_slug": self.object.slug})
        return context


class CartsView(LoginRequiredMixin, ListView):
    model = Cart

    def get_queryset(self):
        Cart.objects.filter(user=self.request.user).update(is_checked=True)
        return (
            Cart.objects.select_related("product")
            .only(
                "quantity",
                "is_checked",
                "product__title",
                "product__slug",
                "product__discount_price",
                "product__price",
            )
            .filter(user=self.request.user)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = (
            Cart.objects.filter(user=self.request.user, is_checked=True)
            .annotate(total=F("product__price") * F("quantity"))
            .aggregate(Sum("total"))["total__sum"]
        )
        return context


class CartAddView(View):
    def post(self, request, slug):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in for adding cart")
            return redirect("products:list")

        cart = Cart.objects.get(product__slug=slug, user=request.user)
        cart.quantity += 1
        cart.save(update_fields=["quantity"])
        total_price = (
            Cart.objects.filter(user=self.request.user)
            .annotate(total=F("product__price") * F("quantity"))
            .aggregate(Sum("total"))["total__sum"]
        )

        return JsonResponse(
            {
                "added": True,
                "total": cart.get_total(),
                "quantity": cart.quantity,
                "total_price": total_price,
                "has_discount": cart.product.has_discount(),
                "amount_saved": cart.get_amount_saved(),
            }
        )


class CartRemoveView(View):
    def post(self, request, slug):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in for adding cart")
            return redirect("products:list")

        cart = Cart.objects.get(product__slug=slug, user=request.user)

        data = {}
        data["deleted"] = False
        if cart.quantity == 1:
            data["total"] = cart.get_total()
            cart.delete()
            data["deleted"] = True

        else:
            cart.quantity -= 1
            cart.save(update_fields=["quantity"])
            total_price = (
                Cart.objects.filter(user=self.request.user)
                .annotate(total=F("product__price") * F("quantity"))
                .aggregate(Sum("total"))["total__sum"]
            )
            data["removed"] = True
            data["total"] = cart.get_total()
            data["quantity"] = cart.quantity
            data["total_price"] = total_price
            data["has_discount"] = cart.product.has_discount()
            data["amount_saved"] = cart.get_amount_saved()

        return JsonResponse(data)


class CartDeleteView(View):
    def delete(self, request, slug):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in for adding cart")
            return redirect("products:list")

        cart = Cart.objects.get(product__slug=slug, user=request.user)
        cart.delete()
        total = (
            Cart.objects.filter(user=self.request.user)
            .annotate(total=F("product__price") * F("quantity"))
            .aggregate(Sum("total"))["total__sum"]
        )
        return JsonResponse({"deleted": True, "total": total})


class CartCheckedView(View):
    def post(self, request, slug):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in for adding cart")
            return redirect("products:list")

        cart = Cart.objects.get(product__slug=slug, user=request.user)
        cart.is_checked = False
        cart.save(update_fields=["is_checked"])
        return JsonResponse({"checked": cart.is_checked})
