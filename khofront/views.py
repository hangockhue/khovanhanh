from django.shortcuts import render
from vanhanh.models import Typeproduct, Product, Nofication, Grouptype, Delivery, Classification
# Create your views here.
from django.http import Http404
from django.template.defaultfilters import register
from django.shortcuts import render, redirect
from django.core.mail import send_mail
import random
import json
from khofront.config import WAFF_TOKEN
import requests

def filter_titles():
    titles = []
    classifications = Classification.objects.all()
    for classification in classifications:
        titles.append({classification: Grouptype.objects.filter(classification=classification)})
    return titles

def index(request):
    # Filter hightlight product
    type_product = Typeproduct.objects.filter(highlight=True)
    products = {}
    for type in type_product:
        products[remove_accents(type.name).replace(" ","")] = Product.objects.filter(type=type)

    # Filter title
    titles = filter_titles()

    # Filter list show
    product_list = {}
    product_list_2 = []
    show_products = Typeproduct.objects.filter(list_show=True)
    for _title in show_products:
        product_list[_title.name] = Product.objects.filter(type=_title)
        product_list_2.append({_title: Product.objects.filter(type=_title)})

    return render(request, "content/index.html", {"type_product": type_product, "products": products,
                                                   "titles":titles,"product_list_2":product_list_2})
def group(request, pk, page):
    # Filter titles
    titles = filter_titles()
    # End filter
    group_type = Grouptype.objects.get(pk=pk)

    types = Typeproduct.objects.filter(group_type=group_type)
    products = Product.objects.filter(type__in=types)
    print(products)

    return render(request, 'content/group_product.html', {'titles': titles, 'types':types, 'group_type':group_type 
                                                            ,'products':products})

def type_product(request, pk, page):
    type = Typeproduct.objects.get(pk=pk)
    products = Product.objects.filter(type=type)
    group_type = type.group_type
    types = Typeproduct.objects.filter(group_type=group_type)
    # Filter header
    titles = filter_titles()
    return render(request, "content/type_product.html",{"products":products,"type":type 
                                                        ,"titles":titles, 'types':types, 'group_type':group_type})

def cartboard(request):
    # Filter header
    titles = filter_titles()
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
            order = (str(i['name']) + ":" + str(i['amount']) + ":" 
                        + str(int(i['price_number'])*int(i['amount'])) + "\n")
            order_list += order
        print(name, phone_number, address, delivery, price, order_list)
        Delivery.objects.create(name=name, number_phone=phone_number,address= address,
                             price=str(price), delivery=delivery, order_list=order_list)
        # send_mail("Bạn đã nhận được một đơn đặt hàng",
        #           "Người đặt: {}, số điện thoại: {}, đơn hàng: {}".format(name,phone_number,order_list),
        #           "nhokproxmenone@gmail.com",
        #           ["healwayhappy@gmail.com"]
        #           )
        update_waff(request)
        return redirect("success")
    else:
        return render(request, "content/cartboard.html", {"titles": titles})

def update_waff(request):
    click_id = request.COOKIES.get('click_id')
    commission = request.COOKIES.get('commission')
    lead_amount = request.COOKIES.get('lead_amount')
    pub_id = request.COOKIES.get('pub_id')
    if click_id:
        update_url = f"https://wwaff.com/affiliate/tracklinks/{click_id}"
        headers ={
            "Authorization": WAFF_TOKEN
        }
        data = {
            "flead": 1,
            "amount": float(commission),
            "amount2": float(lead_amount)
        }
        response = requests.put(url=update_url, data=data, headers=headers)
        print("Status update track link:", response.status_code)
        print("Body response update track link: ", response.text)
    else:
        print("Click ID doesn't exsit. Update later!")

def success_post(request):

    return render(request, "content/success.html")

def search(request):
    titles = filter_titles()

    if request.method == "GET":
        key_search = remove_accents(request.GET['search']).lower()
        products = [product for product in Product.objects.all() if key_search in product.name_remove_accents.lower()]
        print(products)
        return render(request, "content/search.html", { "products": products, "titles":titles ,
                                                         "key_search": request.GET["search"] })

def detail(request, pk, page):
    # Filter titles
    titles = filter_titles()
    # End filter

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

