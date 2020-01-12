from django.shortcuts import render
from vanhanh.models import Typeproduct, Product, Nofication, Grouptype
# Create your views here.
from django.http import Http404
from django.template.defaultfilters import register
from django.shortcuts import render, redirect
import random


def index(request):

    type_product = Typeproduct.objects.filter(highlight=True)
    products = {}
    titles = {}
    for type in type_product:
        products[remove_accents(type.name).replace(" ","")] = Product.objects.filter(type=type)
    group_type = Grouptype.objects.filter(highlight=True)
    for _title in group_type:
        titles[_title.name] = Typeproduct.objects.filter(group_type=_title)
    return render(request, "content/index.html", {"type_product": type_product, "products": products, "titles":titles})


def type_product(request, pk, page):
    type = Typeproduct.objects.get(pk=pk)
    products = Product.objects.filter(type=type)
    # Filter header
    titles = {}
    group_type = Grouptype.objects.filter(highlight=True)
    for _title in group_type:
        titles[_title.name] = Typeproduct.objects.filter(group_type=_title)
    print([products])
    return render(request, "content/type_product.html",{"products":products,"type":type ,"titles":titles})

def cartboard(request):

    return render(request, "content/cartboard.html")


def success_post(request):

    return render(request, "content/success.html")

def search(request):
    if request.method == "GET":
        key_search = remove_accents(request.GET['search']).lower()
        products = [product for product in Product.objects.all() if key_search in product.name_remove_accents.lower()]
        print(products)
        return render(request, "content/search.html", { "products": products, "key_search": request.GET["search"] })

def detail(request, pk, page):

    titles = {}
    group_type = Grouptype.objects.filter(highlight=True)
    for _title in group_type:
        titles[_title.name] = Typeproduct.objects.filter(group_type=_title)

    product = Product.objects.get(pk=pk)
    related = Product.objects.all()
    random_related = []
    for i in range(15):
        random_related.append(random.choice(related))
    print(random_related)
    return render(request, "content/detail.html", {"product": product, "random_related": random_related, "titles":titles})

def register_email(request):
    if request.method == "POST":
        Nofication.objects.create(email=request.POST['email'])
        return redirect('index')
    else:
        return redirect('index', message='Gửi thông tin email thất bại')
def remove_accents(input_str):
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    s = ''
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s

@register.filter
def get_item(dictionary, key):
    return dictionary.get(remove_accents(key).replace(" ",""))

@register.filter
def get_first(array):
    return [array[0]]

@register.filter
def get_rest(array):
    return array[1:]

