from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from .models import Item,Comment,Cart
from .forms import LoginForm, RegisterForm ,CommentForm
from django.contrib.auth.models import User
from django.shortcuts import render

def rate(itemid):
    commentsItem = Comment.objects.filter(itemId=itemid)
    #values btrg3 list of Query set el col Rate bs
    rates_item=commentsItem.values('Rate')
    if len(rates_item) > 0:
        sum=0
        avg=0
        for rateitem in rates_item:
            if rateitem is not None:
                sum=sum+rateitem['Rate']
        avg = sum / len(rates_item)
        return avg
    else :
        return 0


def index(request):
    item_all=Item.objects.all()
    context={'items':item_all}
        # if request.user.is_authenicated():
    #    context['user']=request.user.username
    return render(request,'products/home.html',context)

def kitchen(request):
    item_all=Item.objects.filter(ItemCategory=1)
    #filter btrg3li list lkn get btrg3li wa7d bs
    return render(request,'products/category.html',{'items':item_all})

def hold(request):
    item_all=Item.objects.filter(ItemCategory=3)
    #filter btrg3li list lkn get btrg3li wa7d bs
    return render(request,'products/category.html',{'items':item_all})

def care(request):
    item_all=Item.objects.filter(ItemCategory=2)
    #filter btrg3li list lkn get btrg3li wa7d bs
    return render(request,'products/category.html',{'items':item_all})


def single_page(request,item_id):
    item=Item.objects.get(pk=item_id)
    form=CommentForm(request.POST or None)
    if form.is_valid():
        comment=form.save()
        if not request.user.is_authenticated :
            return redirect("products:login")
        comment.username=request.user.username
        comment.itemId=item_id
        comment.stars='x'*comment.Rate
        comment.graystars='x'*(5-comment.Rate)
        comment.save()
    comments=Comment.objects.filter(itemId=item_id)
    item.ItemRate = round(rate(item.id),2)
    item.stars = 'x' * int(item.ItemRate)
    item.graystars = 'x' * (5 - int(item.ItemRate))
    item.save()
    return render(request,'products/single.html',{'item':item,'form':form,'comments':comments})

#       ^
 #   < -__- >"
#   <--|_|-->
#       |
#     </ \>

def login_user(request):
    form=LoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("products:index")
    return render(request,"products/login_form.html",{'form':form})


User=get_user_model()

def register_user(request):
    form=RegisterForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get('username')
        email=form.cleaned_data.get("email")
        password=form.cleaned_data.get('password')
        new_user=User.objects.create_user(username,email,password)
        cart=Cart.objects.create()
        cart.UserId=new_user.id
        cart.save()
        return redirect("products:login")
    return render(request,'products/registration_form.html',{'form':form})

def logout_user(request):
    if User.is_authenticated:
        logout(request)
    return redirect("products:index")



def add_cart(request,item_id):
    if not request.user.is_authenticated:
        return redirect("products:login")
    item=Item.objects.get(pk=item_id)
    cart=Cart.objects.get(UserId=request.user.id)
    cart.ItemsId=str(cart.ItemsId)+" "+str(item.id)
    cart.TotalPay+=float(item.ItemPrice)
    cart.save()
    return redirect("products:index")

def remove_cart(request,item_id):
    item=Item.objects.get(pk=item_id)
    item_price=item.ItemPrice
    cart=Cart.objects.get(UserId=User.pk)
    cart.ItemsId.remove(item_id)
    cart.TotalPay-=item_price
    cart.save()
    return redirect("products:index")




def contact(request):
    return render(request,'products/contact.html')
