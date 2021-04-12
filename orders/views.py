
import stripe 

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.models import Permission

from django.conf import settings

# Create your views here.
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY 

class OrdersPageView(TemplateView):
    template_name = 'orders/purchase.html'

    '''
    In Django each template is rendered with context data 
    provided by the views.py file. By overriding get_context_data(),
    we can elegantly pass this information in with our TemplateView.
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_key'] = settings.STRIPE_TEST_PUBLISHABLE_KEY
        return context

def charge(request):
    permission = Permission.objects.get(codename='special_status')
    user = request.user
    user.user_permissions.add(permission)
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount = 3900,
            currency = 'usd',
            description = 'Purchase all books',
            source = request.POST['stripeToken']
        )
        return render(request, 'orders/charge.html')