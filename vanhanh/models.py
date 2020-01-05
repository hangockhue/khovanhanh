from django.db import models
from datetime import datetime
# Create your models here.

class Grouptype(models.Model):
    name = models.CharField("Loại chung", max_length=50)
    highlight = models.BooleanField("Hiển thị title", default=True)
    def __str__(self):
        return remove_accents(self.name)
    @property
    def name_filter(self):
        return remove_accents(self.name)
    class Meta:
        verbose_name = 'Grouptype'
        verbose_name_plural = 'Nhóm sản phẩm'

class Typeproduct(models.Model):
    name = models.CharField("Loại sản phẩm", max_length=50)
    highlight = models.BooleanField("Nổi bật tại trang chủ",default=False)
    group_type = models.ForeignKey(Grouptype, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Typeproduct'
        verbose_name_plural = 'Loại sản phẩm'

class Product(models.Model):
    name = models.CharField("Tên", max_length=50)
    image = models.ImageField("Image", null=True, default='4.jpg')
    description = models.TextField("Mô tả", null=True, blank=True)
    price = models.IntegerField("Giá", default=150000)
    sale_off = models.IntegerField("Giá giảm", null=True, blank=True)
    wholesale = models.CharField("Giá bán sĩ", null=True, max_length=50, default="150k/cái")
    type = models.ForeignKey(Typeproduct, on_delete=models.CASCADE)
    brands = models.CharField("Thương hiệu", max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            this = Product.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except: pass
        super(Product, self).save(*args, **kwargs)
    @property
    def url(self):
        return remove_accents(self.name).replace(" ","-")
    @property
    def price_string(self):
        return str(self.price)[:-3] + "." + str(self.price)[-3:]
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Sản phẩm'
    def ___str__(self):
        return self.name
    @property
    def name_remove_accents(self):
        return remove_accents(self.name)

class Nofication(models.Model):
    email = models.EmailField("Email khách hàng")
    class Meta:
        verbose_name = "Nofication"
        verbose_name_plural = "Email khách hàng"

class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    delivery = models.CharField("Tên đơn hàng", max_length=50, null=True)
    name = models.CharField("Tên khách hàng", max_length=50)
    number_phone = models.CharField("Số điện thoại", max_length=15)
    price = models.IntegerField("Giá đơn hàng", null=True)
    order_list = models.TextField("Danh sách đặt hàng")
    description = models.TextField("Ghi chú")
    check_order = models.BooleanField(default=False)
    person_check = models.CharField("Người check", max_length=20, unique=False)

    def __str__(self):
        return self.delivery

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Đơn hàng'

class Done_Delivery(models.Model):
    name = models.ForeignKey(Order, on_delete=models.CASCADE)
    # order_list = models.TextField("Danh sách đơn hàng", default=Order.objects.filter(delivery=name).order_list)
    date_done = models.DateField("Ngày giao", null=True)
    # price = models.CharField("Giá đơn hàng", default=Order.objects.filter(delivery=name).price)
    class Meta:
        verbose_name = 'Done_Delivery'
        verbose_name_plural = 'Đơn hàng đã hoàn thành'
s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
def remove_accents(input_str):
    s = ''
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s
# class Sale_Product(models.Model):
#     name = models.CharField("Tên")
#
