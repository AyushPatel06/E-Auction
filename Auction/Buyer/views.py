from django.conf import Settings, settings
from django.shortcuts import render, redirect
from django.utils.translation import get_language
#from Buyer import Checksum
from .models import ReviewRating, UserDetail,Contact
from .forms import ReviewForm, UserForm, addressForm, addressForm2, profileForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import authenticate, login, logout
from Seller.models import Product, SellerDetail, category, Bid, Orders
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Max
import random
import string
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def user_signup(request):
            if request.method == 'POST':
                first = request.POST.get('first_name')
                last = request.POST.get('last_name')
                username=request.POST['username']
                email=request.POST['email']
                password=request.POST['password']
                confirm = request.POST['confirmpassword']
                type = request.POST.get('RadioOptions','False')
                if type == 'buyer':
                    buyer = 'True'
                    seller = 'False'
                else:
                    seller = 'True'
                    buyer = 'False'
                error=[]
                if(len(username)<3):
                    error.append(1)
                    messages.warning(request,"Username Field must be greater than 3 character.")
                if(len(password)<5):
                    error.append(1)
                    messages.warning(request,"Password Field must be greater than 5 character.")
                if(password != confirm):
                    error.append(1)
                    messages.warning(request,"Password field and Confirm Password Field can be same")
                if(len(error)==0):
                    #password_hash = make_password(password)
                    usr = User.objects.create_user(username=username,first_name=first,last_name=last,email=email,password=password,is_staff=buyer,is_superuser=seller)
                    usr.save()
                    if usr.is_staff == 'True':
                        ur = User.objects.filter(username=username).first()
                        UserDetail(usr=ur).save()
                    else:
                        ur = User.objects.filter(username=username).first()
                        SellerDetail(usr=ur).save()
                    #messages.info(request,"Account Created Successfully, please Login to continue")
                    return redirect('Buyer:index')
            return redirect('Buyer:index')


def index(request):
    prod = Product.objects.filter(start__lte=datetime.now(),end__gte=datetime.now()).order_by('start')
    reviews = ReviewRating.objects.all()
    return render(request,'buyer/home.html',{'auctions':prod,'category':category.objects.all(),'reviews':reviews})

def user_login(request):
    if request.method=="POST":
        username=request.POST['username1']
        password=request.POST.get('password1')
        if not len(username):
            messages.warning(request,"Username field is empty")
            redirect('Buyer:index')
        elif not len(password):
            messages.warning(request,"Password field is empty")
            redirect('Buyer:index')
        else:
            pass
        user = authenticate(username=username, password=password)
        if user is not None:
                    if user.is_staff:
                        login(request, user)
                        redirect('Buyer:index')

                    elif user.is_superuser:
                        login(request,user)
                        return redirect('Seller:index')
    else:
        redirect('Buyer:index')
    return redirect('Buyer:index')

def user_logout(request):
        logout(request)
        return redirect('Buyer:index')
def about(request):
    return render(request,'buyer/about.html',{'category':category.objects.all()})

def password_reset_request(request):
    if request.method == "POST":
        data = request.POST['email']
        associated_users = User.objects.filter(Q(email=data))
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name = "password_reset_email.txt"
                c = {
                "email":user.email,
                'domain':'127.0.0.1:8000',
                'site_name': 'E-Auction',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, Settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect ("/password_reset/done/",{'category':category.objects.all()})
    return render(request,"forgot_password.html",{'category':category.objects.all()})

def MenuFilter(request, querys):
        activeauc = [j for j in Product.objects.filter(start__lte = datetime.now(), end__gte=datetime.now()).order_by('start') if str(j.category).lower() == querys.split(',')[0].lower() and str(j.subcategory).lower()==querys.split(',')[1].lower()]
        pastauc = [i for i in Product.objects.filter(end__lte=datetime.now()) if str(i.category).lower() == querys.split(',')[0].lower() and str(i.subcategory).lower()==querys.split(',')[1].lower()]
        comingauc = [k for k in Product.objects.filter(start__gte=datetime.now()).order_by('start') if str(k.category).lower() == querys.split(',')[0].lower() and str(k.subcategory).lower()==querys.split(',')[1].lower()]
        if request.method == 'POST':
            r = request.POST['reminder']
            print(r)
        params = {
            'pastauctions':pastauc,
            'catg':querys.split(',')[0],
            'subcatg':querys.split(',')[1],
            'activeauctions':activeauc,
            'comingauctions':comingauc,
            'category':category.objects.all(),
            }
        return render(request, 'buyer/shop-grid.html', params)
    

def search(request):
        query = request.GET.get('query', '')
        activeauc = [j for j in Product.objects.filter(start__lte = datetime.now(), end__gte=datetime.now()).order_by('start') if query.lower() in j.product_name.lower() or query.lower() in j.description.lower() or query.lower() in j.subcategory.lower()]
        pastauc = [i for i in Product.objects.filter(end__lte=datetime.now()) if query.lower() in i.product_name.lower() or query.lower() in i.description.lower() or query.lower() in i.subcategory.lower()]
        comingauc = [k for k in Product.objects.filter(start__gte=datetime.now()).order_by('start') if query.lower() in k.product_name.lower() or query.lower() in k.description.lower() or query.lower() in k.subcategory.lower()]
        prods = []
        for i in Product.objects.all():
            if query.lower() in i.product_name.lower() or query.lower() in i.description.lower() or query.lower() in i.subcategory.lower():
                prods.append(i)
        params = {
            'pastauctions':pastauc,
            'activeauctions':activeauc,
            'comingauctions':comingauc,
            'category':category.objects.all(),
            }
        return render(request, 'buyer/shop-grid.html', params) 


@login_required(login_url="Buyer:index")
def productView(request, prod_id):
        activeauc = Product.objects.filter(product_id = prod_id,start__lte = datetime.now(), end__gte=datetime.now()).first()
        if activeauc is None:
            activeauc =Product.objects.filter(product_id = prod_id,end__lte=datetime.now()).first()    
        bids = Bid.objects.filter(product_id=prod_id)
        auc=Product.objects.filter(product_id = prod_id).aggregate(Max('current_bid'))['current_bid__max']
        win = Bid.objects.filter(product_id = prod_id,current_bid=auc).values_list('user',flat=True).first()
        winner = User.objects.filter(id=win).values_list('username',flat=True).first()
        Product.objects.filter(product_id = prod_id).update(winner=winner)
        if bids:
           b=bids[::-1][0]
        else:
            b=0
        if request.method == 'POST':
            bid1 = request.POST.get('Bid')
            timeleft =  request.POST.get('timer')
            product = Product.objects.get(product_id=prod_id)
            user = request.user
            total_bid =  activeauc.total_bid
            auc=Product.objects.filter(product_id = prod_id).aggregate(Max('current_bid'))['current_bid__max']
            if bid1:
                if int(bid1) <= auc or int(bid1) <= activeauc.price:
                    messages.warning(request,"You don't place bid less & equal to current bid....")
                else:
                    total_bid = total_bid + 1 
                    bid = Bid.objects.create(bid_date=datetime.now(), user=user, current_bid=bid1, product=product)
                    bid.save()
                    args = Bid.objects.filter(product_id=product)
                    value = args.aggregate(Max('current_bid'))['current_bid__max']
                    if value is None:
                        value = 0
                    Product.objects.filter(product_id = prod_id).update(total_bid=total_bid,current_bid=value,winner=winner,winning_bid=value)
                    bids = Bid.objects.filter(product_id=prod_id)
                    if bids:
                       b=bids[::-1][0]
                    else:
                        b=0
                    return render(request, 'buyer/product-details.html',{'product':activeauc,'bids':bids,'value':value, 'category':category.objects.all(),'bd':b,"winbid":auc,"winner":winner})
            if timeleft == '0':
                Product.objects.filter(product_id = prod_id).update(end=datetime.now())

        return render(request, 'buyer/product-details.html',{'product':activeauc,'bids':bids,'value':activeauc.current_bid, 'category':category.objects.all(),'bd':b,"winbid":auc,"winner":winner})

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@login_required(login_url="Buyer:index")
def checkout(request, prod_id):
    address_form = addressForm(instance=request.user.userdetail)
    profile_form = addressForm2(instance=request.user)
    prod = Product.objects.filter(product_id=prod_id).first()
    if request.method == 'POST':
        address_form = addressForm(request.POST, instance=request.user.userdetail)
        profile_form = addressForm2(request.POST, instance=request.user)
        if address_form.is_valid() and profile_form.is_valid():
            address_form.save()
            profile_form.save()
            type = request.POST.get('RadioOptions1','False')
            if type == 'COD':
                c = 'COD'  
                if Orders.objects.filter(products=prod_id).exists():
                    return redirect('/myorders')
                else:
                    order_id = random_string_generator()
                    Orders(order_id=order_id,user=request.user,saller=Product.objects.filter(product_id=prod_id).first().seller,products=prod_id,payment=c,status='Placed',date=datetime.now(),price=prod.current_bid).save()
                    return redirect('/myorders')
            

            

    context ={
        'address':address_form,
        'profile':profile_form,
        'prod':prod,
    }
    return render(request,'buyer/checkout.html',context)

@csrf_exempt
def response(request):
    if request.method == "POST":
        # MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]
        
       
    return HttpResponse(status=200)



def MyOrders(request):
        if request.method == 'POST':
            order_id = request.POST.get('order_id')
            o = Orders.objects.filter(order_id=order_id)[0]
            o.status = 'Cancel'
            o.save()
        params = {
            'orders': [i for i in Orders.objects.all() if i.user == request.user and i.status != 'Delivered' and i.status != 'Cancel'],
            'delivered': [i for i in Orders.objects.all() if i.user == request.user and i.status == 'Delivered'],
            'cancel': [i for i in Orders.objects.all() if i.user == request.user and i.status == 'Cancel'],
            'category':category.objects.all()
        }
        return render(request,'buyer/myorders.html', params)

@login_required(login_url="Buyer:index")
def contact(request):
        if request.method == 'POST':
                cont_name = request.POST.get('Name', default='')
                cont_email = request.POST.get('Email', default='')
                cont_subject = request.POST.get('Subject', default='')
                cont_phone = request.POST.get('Phone', default='')
                cont_mess = request.POST.get('Message', default='')
                con = Contact(name = cont_name, email = cont_email, subject = cont_subject, message = cont_mess, phone = cont_phone)
                con.save()
                messages.success(request, 'Your message has been sent. Thank you!')

        return render(request, 'buyer/contact.html', {'category':category.objects.all()})

@login_required(login_url="Buyer:index")
def Profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user.userdetail)
        profile_form = profileForm(request.POST, instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Account is updated successfully...')
            return render(request,'buyer/profile.html',{'address':user_form,'profile':profile_form})
    else:
        user_form = UserForm(instance=request.user.userdetail)
        profile_form = profileForm(instance=request.user)
    return render(request,'buyer/profile.html',{'address':user_form,'profile':profile_form,'category':category.objects.all()})

def submit_review(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.user_id = request.user.id
                data.fn = request.user.first_name
                data.ln = request.user.last_name
                data.img = request.user.userdetail.photo.url
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
def faq(request):
    return render(request,'buyer/faq.html')