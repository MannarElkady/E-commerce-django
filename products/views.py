from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from .models import Item,Comment,Cart
from .forms import LoginForm, RegisterForm ,CommentForm
from django.contrib.auth.models import User
from django.shortcuts import render


#rate Function to calculate average Rating of all rates for specific item Using Django Functions for DB manipulation    
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

#rate Function to calculate average Rating of all rates for specific item Using DB SQL commands for DB manipulation    
def rate(itemid):
    commentsItem = Comment.objects.raw('''Select * From products_comment WHERE products_comment.itemId = %s ''', [itemid])
    rates_item = []
    for item in commentsItem:
        rates_item.append(item.Rate)
    if len(rates_item) > 0:
        sum = 0
        avg = 0
        for rateitem in rates_item:
            if rateitem is not None:
                sum = sum + rateitem
        avg = sum / len(rates_item)
        return avg
    else:
        return 0

def index(request):
    item_all=Item.objects.all()
    context={'items':item_all}
        # if request.user.is_authenicated():
    #    context['user']=request.user.username
    return render(request,'products/home.html',context)

def kitchen(request):
    item_all=Item.objects.filter(ItemCategory=1)
    
    #Calling all the items for specific category using DB
    #item_all = Item.objects.raw('''Select * from products_item WHERE ItemCategory_id=1''')
    
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

#Calling An Item Single page with django functions for DB manipulation
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


#Calling An Item Single page with SQL commands for DB
def single_page(request, item_id):
    item = Item.objects.get(pk=item_id)
    c = connection.cursor()
    itemQue = c.execute(''' Select * From products_item where id = %s   ''', [item_id])
    itemQue = list(itemQue)[0]
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        if not request.user.is_authenticated:
            return redirect("products:login")
        # insert comment into DB with SQL
        stars = 'x' * comment.Rate
        greyStars = 'x' * (5 - comment.Rate)
        c.execute(
            '''INSERT INTO products_comment (Review, Rate, itemId, username, stars, graystars) VALUES (%s,%s,%s,%s,%s,%s)''',
            [comment.Review, comment.Rate, item_id, request.user.username, stars, greyStars])
        # Update Product Rate
        c.execute(''' UPDATE products_item SET ItemRate = %s , stars = %s , graystars = %s WHERE products_item.id = %s ''',
                  [round(rate(item_id), 2),'x' * int(itemQue[4]),'x' * (5 - int(itemQue[4])),item_id])

    comments = Comment.objects.filter(itemId=item_id)
    return render(request, 'products/single.html', {'item': item, 'form': form, 'comments': comments})

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


# Add to cart Function (add_cart) Using django Functions to manipulate data from DB 
# Note this function had written before adding HAVE Model (table) So use this function without Have model in models
def add_cart(request,item_id):
    if not request.user.is_authenticated:
        return redirect("products:login")
    item=Item.objects.get(pk=item_id)
    cart=Cart.objects.get(UserId=request.user.id)
    cart.ItemsId=str(cart.ItemsId)+" "+str(item.id)
    cart.TotalPay+=float(item.ItemPrice)
    cart.save()
    return redirect("products:index")

# Add to cart Function (add_cart) Using direct sql commands from DB for DB manipulation
# Note this function had written after adding HAVE Model (table) as (A table generated from Many to Many relationship between
# Item and Cart Models So use this function with hHave Model
def add_cart(request, item_id):
    c=connection.cursor()
    if not request.user.is_authenticated:
        return redirect("products:login")
    #GET ITEM FROM DB
    item = c.execute('''SELECT * FROM products_item WHERE products_item.id= %s ''',[item_id])
    item=list(item)[0]
    print(item)
    #Get Cart Data from DB
    cart = c.execute('''SELECT * FROM products_cart WHERE products_cart.userId_id=%s''',[request.user.id])
    cart=list(cart)[0]
    #Check if itemId with same CartId alrwady exists
    exist=c.execute('''SELECT *  FROM products_have WHERE products_have.itemId_id = %s 
    AND products_have.cartId_id = %s''',[item_id,cart[0]])
    exist=list(exist)
    #if exists just add number of this item in db to avoid redundancy
    if len(exist) > 0:
        c.execute('''UPDATE products_have SET itemNumber = itemNumber+1
        WHERE products_have.itemId_id=%s AND products_have.cartId_id= %s ''', [item_id,cart[0]])
    #if not exist insert new raw with this item data for the Have table of the user
    else:
        c.execute('''INSERT INTO products_have (cartId_id,itemId_id,itemNumber) 
        VALUES (%s,%s,%s)''',[cart[0],item_id,1])
    c.execute(''' UPDATE products_cart SET totalPay = totalPay + %s  
    WHERE products_cart.id = %s ''',[item[2],cart[0]])
    print(item[2])
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
