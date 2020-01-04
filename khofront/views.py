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
    for type in type_product:
        products[remove_accents(type.name).replace(" ","")] = Product.objects.filter(type=type)
    group_type = Grouptype.objects.filter(highlight=True)
    type_product_all = Typeproduct.objects.all()
    print(group_type[0].name)

    print(Typeproduct.objects.filter(name=group_type[0].name))
        #     if title.name == type.group_type:
        #         print(type.group_type)
    return render(request, "content/index.html", {"type_product": type_product, "products": products, 'group_type':group_type, type_product_all:'type_group_all'})



def success_post(request):

    return render(request, "content/success.html")

def search(request):
    return render(request, "content/search.html")

def detail(request, pk, page):
    product = Product.objects.get(pk=pk)
    related = Product.objects.all()
    random_related = []
    for i in range(15):
        random_related.append(random.choice(related))
    print(random_related)
    return render(request, "content/detail.html", {"product": product, "random_related": random_related})

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

@register.filter
def get_title(array, obj):
    return array.objects.filter(obj)