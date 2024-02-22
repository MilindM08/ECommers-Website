from django.shortcuts import render,redirect,HttpResponse
from.models import Product,CartItem,Order
from.forms import CreateUserForm,AddProduct
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
import random
import razorpay
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def index(request):
    products=Product.objects.all()
    c={}
    c['products']= products
    return render(request,'index.html',c)


def productDetails(request,pid):
    products=Product.objects.get(product_id=pid)
    c={}
    c['products']= products
    return render(request,'productDetails.html',c)


def viewcart(request):
    if  request.user.is_authenticated:
        cart=CartItem.objects.filter( user = request.user)
    else:
        cart=CartItem.objects.filter( user = None)   
        messages.warning(request,"Login To add to Cart")
    print(cart)
    c={}
    c['item']=cart
    total_price=0
    for x in cart:
        print(x.product.price,x.quantity)
        total_price += (x.product.price*x.quantity)
        print(total_price)
    c['total']=total_price 
    length=len(cart)
    c['length']=length   
    return render(request,'cart.html',c)


def addcart(request,pid):
    products= Product.objects.get(product_id=pid)
    user = request.user if request.user.is_authenticated else None
    if user:
        cart,created=CartItem.objects.get_or_create(product=products,user=user)
    else:
        return redirect("/login")
    print(cart.quantity,created)
    
    if not created:
        cart.quantity +=1
    else:
        cart.quantity =1
    cart.save()    
    return redirect('/viewcart')    


def removecart(request,pid):
    products=Product.objects.get(product_id=pid)
    cart=CartItem.objects.filter(product=products,user=request.user)
    cart.delete()
    return redirect("/viewcart")

from django.db.models import Q
def search(request):
    query=request.POST['q']
    print(f" Query is{query}")
    if not query:
        result=Product.objects.all()
    else:    
        result=Product.objects.filter(
            Q(product_name__icontains=query)|
            Q(category__icontains=query)|
            Q(price__icontains=query)
        )
    return render(request,'search.html',{'result':result,'query':query})    


def range(request):
    if request.method== "GET":
        return redirect("/")
    else:
        min = request.POST['min']
        max = request.POST['max']
        #using Custom Manager
        if min !="" and max != "" and min is not None and max is not None:
          queryset = Product.prod.get_price_range(min,max)
          # uisng Degault MAnager
          # queryset = Product.objects.filter(price__range = (min,max))
          c={}
          c['products']= queryset
          return render(request,'index.html',c)
        else:
            return redirect("/")



def watchList(request):
    if request.method== "GET":
        queryset = Product.prod.watch_list()
    
        # uisng Degault MAnager
        # queryset = Product.objects.filter(price__range = (min,max))
        c={}
        c['products']= queryset
        return render(request,'index.html',c)    


def laptopList(request):
    if request.method== "GET":
        queryset = Product.prod.laptop_list()
    
        # uisng Degault MAnager
        # queryset = Product.objects.filter(price__range = (min,max))
        c={}
        c['products']= queryset
        return render(request,'index.html',c)    



def mobileList(request):
    if request.method== "GET":
        queryset = Product.prod.mobile_list()
    
        # uisng Degault MAnager
        # queryset = Product.objects.filter(price__range = (min,max))
        c={}
        c['products']= queryset
        return render(request,'index.html',c)  


def priceOrder(request):
    queryset=Product.objects.all().order_by('price')
    c={'products':queryset}
    return render(request,'index.html',c)


def descpriceOrder(request):
    queryset=Product.objects.all().order_by('-price')
    c={'products':queryset}
    return render(request,'index.html',c)


def updateqty(request,uval,pid):
    products=Product.objects.get(product_id=pid)
    a=CartItem.objects.filter(product=products)
    print(a)
    print(a[0])
    print(a[0].quantity)
    if uval ==1:
        temp =a[0].quantity + 1
        a.update(quantity=temp)
    else:
        temp =a[0].quantity - 1
        a.update(quantity=temp)   
    return redirect("viewcart")

def vieworder(request):
    cart=CartItem.objects.filter(user=request.user)
    print(cart)
    """oid=random.randrange(1000,9999)
    for x in cart:
        Order.objects.create(order_id=oid,product_id=x.product.product_id,quantity=x.quantity,user=request.user)
        #x.delete()
    orders=Order.objects.filter(user=request.user,is_completed=False)"""
    c={}
    c['item']=cart
    total_price=0
    for x in cart:
        #print(x.product.price,x.quantity)
        total_price += (x.product.price*x.quantity)
        #print(total_price)
    c['total']=total_price 
    length=len(cart)
    c['length']=length
    return render(request,"vieworder.html",c)


def register_user(request):
    form= CreateUserForm() 
    if request.method == "POST":
        form= CreateUserForm(request.POST)
        if form.is_valid(): #checking if data is valid
            form.save() # saving into the db
            print("USer created successfully")
            messages.success(request,("user created Successfully"))
            return redirect("/")
        
        else:
            print("Error")
            messages.error(request,("""Your password canâ€™t be too similar to your other personal information.
                                   Your password must contain at least 8 characters.
                                   Your password canâ€™t be a commonly used password.
                                   Your password canâ€™t be entirely numeric."""))
    c={'form':form}
    return render(request,"register.html",c)        




def login_user(request):
    
    if request.method=="POST":
        username=request.POST['username']
        password= request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            print("User Logged in Successfully")
            messages.success(request,("user login created Successfully"))
            return redirect("/")
        else:
            messages.error(request,("There was an error ,Try Again !!"))
            return redirect("login_user/")
    else:
        return render(request,"login.html")    


def logout_user(request):
    logout(request)
    messages.success(request,("Logged Out Successfully"))
    return redirect("/")


def makePayment(request):
    c=CartItem.objects.filter(user=request.user)
    oid=random.randrange(1000,9999)
    for x in c:
        Order.objects.create(order_id=oid,product_id=x.product.product_id,quantity=x.quantity,user=request.user)
        #x.delete()
    orders=Order.objects.filter(user=request.user,is_completed=False)
    total_price=0
    for x in orders:
        total_price+=(x.product.price * x.quantity)
        oid=x.order_id
    print(total_price)
    orderdetails=Order.objects.filter(user=request.user,is_completed=False)
    order_details=[
        {'product_name':order.product.product_name,'quantity':order.quantity,'price':order.product.price}
        for order in orderdetails
    ]    
    client = razorpay.Client(auth=("rzp_test_NrRhkRo3jmQAld", "bRhdIMqipkByzTXcIkfMc9bW"))
    data={"amount": total_price * 100,
          "currency": "INR",
          "receipt": "oid"}
    payment=client.order.create(data = data)
    context={}
    context['data']=payment
    context['amount']=payment['amount']
    c=CartItem.objects.filter(user=request.user)
    c.delete()
    orders.update(is_completed=True)
    sendUserMail(request,orderdetails,request.user.email,total_price)
    return render(request,"payment.html",context)
    


def myOrders(request):
    orders=Order.objects.filter(user=request.user)    
    context={}
    context['item']=orders
    return render(request,'myOrders.html',context)



def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def insertProduct(request):

    
    if request.user.is_authenticated:
        user =request.user
        if request.method=='GET':
            form =AddProduct()
            return render(request,'insertProd.html',{'form':form,"username":user})
        else:
            form =AddProduct (request.POST,request.FILES or None)
            if form.is_valid():
                form.save()
                return redirect("/")
            else:
                return render(request,'insertProd.html',{'form':form,"username":user})   
    else:
        return redirect("/login")     
    
    
    
    
from django.template.loader import render_to_string    
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

def sendUserMail(request,od,recipient_email,tp):
    email_body =render_to_string('order_placed.html',
       {'order_details':od,'total_price':tp})
    """ send_mail(
    "Order placed successfully",
    "Order Details are:",
    "milindmayekar099@gmail.com",
    ["to@example.com"],
    fail_silently=False,
    )"""  
    message=EmailMultiAlternatives(
    subject= "Order placed successfully",
    body=email_body,
    from_email=None,
    to=[recipient_email]

)

    message.attach_alternative(email_body,"text/html")
    message.send()
    return HttpResponse("Mail sent successfully")