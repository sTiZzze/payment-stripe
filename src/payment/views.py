import stripe
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.views import View

from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY

def success_page(request):
    # Ваш код для отображения страницы успешной оплаты
    return render(request, 'success.html')

def cancel_page(request):
    # Ваш код для отображения страницы успешной оплаты
    return render(request, 'success.html')


class CreateCheckoutSessionView(View):
    def get(self, request, id):
        domain = 'http://localhost:8000'
        item = Item.objects.get(id=id)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(item.price * 100), # Stripe использует цены в центах
                        'product_data': {
                            'name': item.name,
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return JsonResponse({'session_id': session.id})


class CreateCheckoutSessionViewOrder(View):
    def get(self, request, id):
        domain = 'http://localhost:8000'
        order = Order.objects.get(order_number=id)

        # Создаем список line_items
        line_items = []
        for item in order.items.all():
            line_item = {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(item.price * 100),  # Преобразуем цену каждого продукта в центы
                    'product_data': {
                        'name': item.name,  # Имя продукта
                    },
                },
                'quantity': 1,
            }
            line_items.append(line_item)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,  # Передаем список продуктов
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )

        return JsonResponse({'session_id': session.id, 'line_items': line_items})


def item_detail(request, id):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    context = {
        'stripe_public_key': stripe_public_key,
    }
    item = Item.objects.get(id=id)
    return render(request, 'home.html', {'item': item, **context})


def order_detail(request, id):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    context = {
        'stripe_public_key': stripe_public_key,
    }
    order = Order.objects.get(order_number=id)
    return render(request, 'order.html', {'order': order, **context})