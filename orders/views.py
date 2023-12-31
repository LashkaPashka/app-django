import stripe
from http import HTTPStatus
from products.models import Product, Baskets
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from orders.forms import OrderForm
from coom.views import TitleMixin
from django.conf import settings
from django.urls import reverse_lazy, reverse
from orders.models import OrdersCreate


stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = 'whsec_a662bae8e79c311f2cdd94574c82a291964f18079658309324728f188cbd9dcc'


class CreateOrderViews(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    title = 'Оформление заказа'
    form_class = OrderForm
    success_url = reverse_lazy('orders:create_order')

    def post(self, request, *args, **kwargs):
        super(CreateOrderViews, self).post(request, *args, **kwargs)
        baskets = Baskets.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_product(),
            metadata={'order_id': self.request.user.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:my-success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:my-channel')),
        )
        return HttpResponseRedirect(checkout_session.url, HTTPStatus.SEE_OTHER)


    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(CreateOrderViews, self).form_valid(form)



class ChannelViews(TitleMixin, TemplateView):
    template_name = 'orders/chanel.html'
    title = 'Checkout canceled'


class SuccessOrdersViews(TitleMixin, TemplateView):
        template_name = 'orders/success.html'
        title = 'Store - Спасибо за заказ!'



class OrdersViews(TitleMixin, TemplateView):
    template_name = 'orders/orders.html'
    title = 'Заказы'




@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body.decode('utf-8')
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
    )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
    # Invalid signature
        return HttpResponse(status=400)

  # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
    # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
        event['data']['object']['id'],
        expand=['line_items'],
    )
        metadata = session.metadata

        fulfill_order(metadata)

  # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(metadata):
    order_id = int(metadata.order_id)
    order = OrdersCreate.objects.get(id=order_id)
    order.after_payment()
    print(order_id)
