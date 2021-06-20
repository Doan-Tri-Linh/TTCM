from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
# Create your views here.
from .forms import SearchForm
from .models import Setting, ContactForm, ContactMessage, FAQ
from product.models import Category, Product, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    page="home"
    products_silder = Product.objects.all().order_by('id')[:4]
    products_latest = Product.objects.all().order_by('-id')[:4]
    products_picked = Product.objects.all().order_by('?')[:4]
    category = Category.objects.all()
    context = {'setting':setting,
               'page':page,
               'products_silder':products_silder,
               'products_latest': products_latest,
               'products_picked': products_picked,

               'category':category}
    return render(request,'home/index.html',context)

def aboutus(request):

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()

    context = {'setting': setting,'category':category}
    return render(request, 'home/about.html', context)

def category_products(request,id,slug):

    category = Category.objects.all()
    products = Product.objects.filter(category_id =id).order_by('-price')
    products_mo = Product.objects.all().order_by('-id')[:3]
    context = {
        'products':products,
        'category':category,
        'products_mo': products_mo,

    }

    return render(request,'home/category_product.html',context)

def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Tin của bạn đã được gửi.Cảm ơn về phản hồi của bạn.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form = ContactForm
    context = {'setting': setting,'form':form,'category':category}
    return render(request, 'home/contact.html', context)


def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query).order_by('-price') #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid).order_by('-price')

            category = Category.objects.all()
            context = {'products': products, 'query':query,
                       'category': category }
            return render(request, 'home/search_products.html', context)

    return HttpResponseRedirect('/')

def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q).order_by('-price')

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)



#detail product
def product_detail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True')
    context = {
        'product':product,
        'category':category,
        'images':images,
        'comments':comments,
    }

    return render(request,'home/product_detail.html',context)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")

    context = {
        'faq': faq,
        'category': category,
    }
    return render(request, 'home/faq.html', context)