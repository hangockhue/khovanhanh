from django.shortcuts import render
from vanhanh.models import Typeproduct, Product, Nofication, Grouptype, Delivery
# Create your views here.
from django.http import Http404
from django.template.defaultfilters import register
from django.shortcuts import render, redirect
from django.core.mail import send_mail
import random
import json

def index(request):

    # Filter hightlight product
    type_product = Typeproduct.objects.filter(highlight=True)
    products = {}
    for type in type_product:
        products[remove_accents(type.name).replace(" ","")] = Product.objects.filter(type=type)


    # Filter title
    titles = {}
    group_type = Grouptype.objects.filter(highlight=True)
    for _title in group_type:
        titles[_title.name] = Typeproduct.objects.filter(group_type=_title)

    # Filter list show
    product_list = {}
    product_list_2 = []
    show_products = Typeproduct.objects.filter(list_show=True)
    for _title in show_products:
        product_list[_title.name] = Product.objects.filter(type=_title)
        product_list_2.append({_title: Product.objects.filter(type=_title)})
    print(product_list)
    print(product_list_2)

    return render(request, "content/index.html", {"type_product": type_product, "products": products,
                                                  "titles":titles, "product_list_2":product_list_2})


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
    # Filter header
    titles = {}
    group_type = Grouptype.objects.filter(highlight=True)
    for _title in group_type:
        titles[_title.name] = Typeproduct.objects.filter(group_type=_title)
    # End filter

    if request.method == "POST":
        total = len(Delivery.objects.all())
        if total == 0:
            delivery = "Đơn hàng 1"
        else:
            delivery = "Đơn hàng " + str(Delivery.objects.all()[total-1].pk + 1)
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        cart = json.loads(request.COOKIES["cart"])
        price = 0
        order_list = ""
        for i in cart:
            price += int(i['price_number'])*int(i['amount'])
            order = i['name'] + ":" + i['amount'] + "/n"
            order_list += order
        print(name, phone_number, address, delivery, price, order_list)
        Delivery.objects.create(name=name, number_phone=phone_number,address= address,
                             price=str(price), delivery=delivery, order_list=order_list)
        # send_mail("Bạn đã nhận được một đơn đặt hàng",
        #           "Người đặt: {}, số điện thoại: {}, đơn hàng: {}".format(name,phone_number,order_list),
        #           "nhokproxmenone@gmail.com",
        #           ["healwayhappy@gmail.com"]
        #           )
        return redirect("success")
    else:
        return render(request, "content/cartboard.html", {"titles": titles})


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

