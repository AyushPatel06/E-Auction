from tarfile import ExtractError
from django.http import JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from Seller.chart import *
from Seller.forms import UserForm1, pUpdateForm, profileForm1
from .models import Orders, SellerDetail, category,Product
from django.contrib import messages
from django.db.models import F, Sum
from django.db.models.functions import ExtractMonth,ExtractYear

# Create your views here.
def index(request):
    ordered = len([p for p in Orders.objects.all() if p.saller == request.user.username])
    delivered = len([p for p in Orders.objects.all() if p.saller == request.user.username if p.status == 'Delivered'])
    pending = len([p for p in Orders.objects.all() if p.saller == request.user.username if p.status != 'Delivered' and p.status != 'Cancle'])
    params = {
        'ordered':ordered,
        'delivered':delivered,
        'pending':pending
    }
    return render(request,'seller/home.html',params)

def add_product(request):
    if request.method == 'POST':
        prod_name = request.POST['prod_name']
        cat = request.POST['category']
        sub = request.POST['subcategory']
        start = request.POST['start']
        end = request.POST['end']
        sbp = request.POST['price']
        desc = request.POST['desc']
        img1 = request.FILES.get('img1')
        if Product.objects.all():
                    prod_id2 = 'pr'+hex(Product.objects.all().last().product_id+1)
        else:
                    prod_id2 = 'pr'+hex(0)
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        img4 = request.FILES.get('img4')
        img5 = request.FILES.get('img5')
        img6 = request.FILES.get('img6')
        Product(product_id2=prod_id2,seller=request.user.username,product_name=prod_name,category=category.objects.get(id=int(cat)),subcategory=sub,price=sbp,start=start,end=end,description=desc,image1=img1).save()
        p = Product.objects.filter(product_id2=prod_id2)[0]
        if img2:
            p.image2=img2
        if img3:
            p.image3=img3
        if img4:
            p.image4=img4
        if img5:
            p.image5=img5
        if img6:
            p.image6=img6
        p.save()
        messages.success(request, f'Product Added !')
    subcat=[]
    for cat in category.objects.all():
        x = cat.sub_Categories.split(',')
        x.insert(0, cat)
        subcat.append(x)
    return render(request,'seller/add-product.html',{'subcat':subcat})   

def view_product(request):
        prod = [p for p in Product.objects.all() if p.seller == request.user.username]
        if request.method == 'GET':
            pro_id = request.GET.get('pro_id')
            pro_id1 = request.GET.get('pro_id1')
            if pro_id:
                prod = [p.product_id for p in Product.objects.all() if p.seller == request.user.username]
                if int(pro_id) in prod:
                    Product.objects.filter(product_id=int(pro_id))[0].delete()
                    messages.success(request, f'The Product of id {pro_id} is deleted !')
                    return redirect('Seller:my_product')
            if pro_id1:
                prod = [p.product_id for p in Product.objects.all() if p.seller == request.user.username]
                subcat=[]
                for cat in category.objects.all():
                    x = cat.sub_Categories.split(',')
                    x.insert(0, cat)
                    subcat.append(x)
        params = {
            'prod': prod[::-1],
            
            }
        return render(request, 'seller/my-product.html',params)

def editproduct(request,prod_id):
    product_to_edit = get_object_or_404(Product, product_id=prod_id)
    if request.method == 'POST':
        product_form = pUpdateForm(request.POST, request.FILES, instance=product_to_edit)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, f'Account is updated successfully...')
            return render(request,'seller/edit-product.html',{'form':product_form,'category':category.objects.all()})
    else:
        product_form = pUpdateForm(instance=product_to_edit)
        return render(request,'seller/edit-product.html',{'form':product_form,'category':category.objects.all()})


def myorders(request):
    if request.method == 'POST':
            order_id = request.POST['odrr']
            st = request.POST.get('st')
            ps = request.POST.get('ps')
            if st:
                o = Orders.objects.filter(order_id=order_id)[0]
                o.status = st
                o.save()
            else:
                o = Orders.objects.filter(order_id=order_id)[0]
                o.paymentstatus = ps
                o.save()
    params = {
            'orders': [i for i in Orders.objects.all() if i.saller == request.user.username and i.status != 'Delivered' and i.status != 'Cancel'],
            'delivered': [i for i in Orders.objects.all() if i.saller == request.user.username and i.status == 'Delivered'],
            'cancel': [i for i in Orders.objects.all() if i.saller == request.user.username and i.status == 'Cancel'],
        }
    return render(request,'seller/myorders.html',params)

def search(request):
    query = request.GET.get('query')
    order = Orders.objects.filter(order_id=query)[0]
    product = Product.objects.filter(product_id=order.products)[0]
    user = User.objects.filter(id=order.user_id)[0]
    if request.method == 'POST':
        order_id = request.POST.get('odrr')    
        ps = request.POST.get('ps')
        o = Orders.objects.filter(order_id=order_id)[0]
        o.paymentstatus = ps
        o.save()
    return render(request,'seller/orderdetail.html',{'order':order,'product':product,'user':user})

def profile(request):
    if request.method == 'POST':
        user = get_object_or_404(SellerDetail, usr_id=request.user)
        user_form = UserForm1(request.POST, request.FILES, instance=user)
        profile_form = profileForm1(request.POST, instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Account is updated successfully...')
            return render(request,'seller/profile.html',{'address':user_form,'profile':profile_form})
    else:
        user = get_object_or_404(SellerDetail, usr_id=request.user)
        user_form = UserForm1(instance=user)
        profile_form = profileForm1(instance=request.user)
    return render(request,'seller/profile.html',{'address':user_form,'profile':profile_form})


def get_filter_options(request):
    grouped_purchases = Orders.objects.filter(saller=request.user.username).annotate(year=ExtractYear('date')).values('year').order_by('-year').distinct()
    options = [purchase['year'] for purchase in grouped_purchases]

    return JsonResponse({
        'options': options,
    })


def get_sales_chart(request, year):
    purchases = Orders.objects.filter(date__year=year,saller=request.user.username)
    grouped_purchases = purchases.annotate(month=ExtractMonth('date')).values('month').annotate(average=Sum('price')).values('month', 'average').order_by('month')

    sales_dict = get_year_dict()

    for group in grouped_purchases:
        sales_dict[months[group['month']-1]] = round(group['average'], 2)

    return JsonResponse({
        'title': f'Sales in {year}',
        'data': {
            'labels': list(sales_dict.keys()),
            'datasets': [{
                'label': 'Amount',
                'lineTension':0,
                'backgroundColor': 'transparent',
                'borderColor': '#012657',
                'pointBackgroundColor':'#012657',
                'borderWidth':4,
                'data': list(sales_dict.values()),
            }]
        },
    })