from django.shortcuts import render,HttpResponseRedirect,reverse,redirect
from django.http import JsonResponse
from .models import *
from random import randint
from .utils import *


from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum

from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def IndexPage(request):
    return render(request,"app/index.html")

def LoginPage(request):
    return render(request,"app/login.html")

def LoginChefPage(request):

    return render(request,"app/loginchef.html")


def SingupPage(request):
    return render(request,"app/signup.html")


def SingupChefPage(request):
    return render(request,"app/signupchef.html")


def Showpage(request):
    return render(request,"app/show.html")

def ChefEditProfilePage(request):
    return render(request,"app/chef/edit-profile.html")

def ChefProduct_add(request):
    return render(request,"app/chef/product-add.html")

def CustomerShop_page(request):
    return render(request,"app/shop-page.html")

def Product_Page(request):
    return render(request,"app/chef/product.html")



def CatPage(request):
    return render(request,"app/chef/catpage.html")

def Insertdata(request):
        try:
            if request.POST['role']=="Customer":

               role = request.POST['role']
               email = request.POST['email']
               password = request.POST['pass']
               cpassword = request.POST['cpass']
               fname = request.POST['fname']
               lname = request.POST['lname']
               contact = request.POST['contact']
               
               
               

               user = User.objects.filter(Email=email)
               if user:
                    message = "Email  does not exist"
                    return render(request,"app/signup.html",{'msg':message})
               else:
                    if password==cpassword:
                        otp = randint(10000,99999)
                        newuser = User.objects.create(Email=email,Password=password,Otp=otp,Role=role)
                        newcust = Customer.objects.create(user_id=newuser,Firstname=fname,Lastname=lname,Contact=contact)
                        email_subject = "food Finder : Customer Verification"
                        sendmail(email_subject,'mail_templates',email,{'name':fname,'otp':otp})
                             
                        return render(request,"app/otpverify.html")
                    else:
                        message = "Password and confirm password does not match"
                        return render(request,"app/signup.html",{'msg':message})
            else:
                if request.POST['role']=="Chef":

                   role = request.POST['role']
                   email = request.POST['email']
                   password = request.POST['pass']
                   cpassword = request.POST['cpass']
                   fname = request.POST['fname']
                   lname = request.POST['lname']
                   contact = request.POST['contact']
                   
                   
               

                   user = User.objects.filter(Email=email)
                   if user:
                        message = "Email  does not exist"
                        return render(request,"app/index.html",{'msg':message})
                   else:
                        if password==cpassword:
                            otp = randint(10000,99999)
                            newuser = User.objects.create(Email=email,Password=password,Otp=otp,Role=role)
                            newchef = Chef.objects.create(user_id=newuser,Firstname=fname,Lastname=lname,Contact=contact)
                            email_subject = "food Finder : Chef Verification"
                            sendmail(email_subject, 'mail_templates', email, {'name': fname, 'otp': otp,})
                            return HttpResponseRedirect(reverse('loginchef'))
                        else:
                            message = "Password and confirm password does not match"
                            return render(request,"app/index.html",{'msg':message})
               

        except Exception as e:
                    print("registration exception----->",e)




def VerifyOtp(request):
    print("------------1--------------")
    try:
        email=request.POST['email']
        eotp=int(request.POST['eotp'])
        print("Eotp--------------->",eotp)
        user = User.objects.get(Email=email)
        if user.Otp==eotp and user.Role =="Customer":
            message = "otp verified successfully"
            return render(request,"app/login.html",{'msg':message})
    except Exception as e:
        print("OTP Verify Exception-------------->",e)


def LoginUser(request):
    try:
        if request.POST['role']=="Customer":
                print("==========1==========")
                email = request.POST['email']
                password = request.POST['password']

                user = User.objects.get(Email=email)
                if user:
                    print("=======2=======")
                    try:
                        if user.Password==password and user.Role=="Customer":
                            print("=======3=======")
                            cust = Customer.objects.filter(user_id=user)
                            request.session['Firstname'] = cust[0].Firstname
                            request.session['Email'] = user.Email
                            request.session['Role'] = user.Role
                            request.session['id'] = user.id
                            return render(request,"app/index-2.html")
                            print("==========4============")
                        else:
                            message = "Password Does not match"
                            return render(request,"app/login.html",{'msg':message})
                    except Exception as e4:
                        print("Customer Login Exception----------->",e4)
                    
                else:
                    message = " User Does not match"
                    return render(request,"app/login.html",{'msg':message})
        else:
            if request.POST['role']=="Chef":
                print("=========5=========")
                email = request.POST['email']
                password = request.POST['password']

                user = User.objects.get(Email=email)
                if user:
                    print("========6========")
                    try:
                        if user.Password==password and user.Role=="Chef":
                            print("==========7========")
                            chef = Chef.objects.filter(user_id=user)
                            request.session['Firstname'] = chef[0].Firstname
                            request.session['Lastname'] = chef[0].Lastname
                            request.session['Email'] = user.Email
                            request.session['Role'] = user.Role
                            request.session['id'] = user.id
                            odata=Transaction.objects.all()
                            l=len(odata)
                            cdata=Customer.objects.all()
                            l1=len(cdata)
                            pdata=Product.objects.all()
                            l2=len(pdata)
                            
                            return render(request,"app/chef/index.html",{'l':l,'l1':l1,'l2':l2})

                            print("=============8===========")
                        else:
                            message = "Password Does not match"
                            return render(request,"app/login.html",{'msg':message})
                    except Exception as e5:
                        print("Exception Chef------------->",e5)


                        
                    
                else:
                    message = " User Does not match"
                    return render(request,"app/login.html",{'msg':message})

            else:
                print("no user found")
    except Exception as e3:
        print("Login Exception ------->",e3)



def DisplayData(request,pk):
    all_data = Customer.objects.get(pk=pk)
    return render(request,"app/show.html",{'key1':all_data})


def EditPage(request,pk):
    udata = User.objects.get(id=pk)
    if udata.Role=="Customer":
        cust = Customer.objects.get(user_id=udata)
        return render(request,"app/customeredit.html",{'key1':cust})

def customerhome(request):
    return render(request,"app/index-2.html")

def feedback_submit(request, pk):
    if request.method == 'POST':
        user = User.objects.get(pk=request.session['id'])
        customer = Customer.objects.get(user_id=user)
        product = Product.objects.get(pk=pk)
        rating = request.POST['rating']
        description = request.POST['description']
        new = Feedback.objects.create(Customer=customer,Product=product,Rating=rating,Description=description)
        msg="Your Feedback saved succesfully"
        return render(request,"app/shop-single.html",{'key4':product,'msg':msg})
       


       
def ChefAlldata(request,pk):
    if 'Email' in request.session and 'Role' in request.session:
        if request.session['Role'] == "Chef":
            chef = Chef.objects.get(pk=pk)
            print("Chef--------------->",chef)
            return render(request,"app/chef/edit-profile.html",{'key2':chef})



def UpdateData(request,pk):
    if request.session['Role'] == "Customer":
        udata = Customer.objects.get(pk=pk)
        udata.Firstname = request.POST['fname']
        udata.Lastname = request.POST['lname']
        udata.Email = request.POST['email']
        udata.Contact = request.POST['contact']
        udata.City = request.POST['city']
        udata.State = request.POST['state']
        udata.Address = request.POST['address']
        
        udata.save()
        return HttpResponseRedirect(reverse('edit'))

    else:
        if request.session['Role'] == "Chef":
            cdata = Chef.objects.get(pk=pk)
            cdata.Firstname = request.POST['fname']
            cdata.Lastname = request.POST['lname']
            cdata.Email = request.POST['email']
            cdata.Contact = request.POST['contact']
            cdata.City = request.POST['city']
            cdata.State = request.POST['state']
            cdata.Address = request.POST['address']
            cdata.Ability = request.POST['Ability']
            cdata.Gender = request.POST['gender']

            cdata.save()
            return HttpResponseRedirect(reverse('edit'))

def Addproduct(request,pk):
    udata = User.objects.get(id=pk)
    if udata.Role == "Chef":

        chef_id = Chef.objects.get(user_id=udata)
        print("Chef_id-------------->",chef_id)
        productname = request.POST['Productname']
        Expirydate = request.POST['Expirydate']
        Mfgdate = request.POST['Mfgdate']
        catid = request.POST['category']
        cid = Category.objects.get(id=catid)
        print("Category------------------>",Category)
        print("Cat_Id---------------->",cid)
        Price = request.POST['Price']
        Discount = request.POST['discount']
        ProductDescription = request.POST['ProductDescription']
        Detail = request.POST['Detail']
        Integrates=request.POST['Integrates']
        Status = request.POST['Status']
        img = request.FILES['Image']
        Keyword = request.POST['Keyword']

        newproduct = Product.objects.create(chef_id=chef_id,cat_id=cid,Productname=productname,Expirydate=Expirydate,Mfgdate=Mfgdate,Price=Price,discount=Discount,ProductDescription=ProductDescription,Detail=Detail,Status=Status,Image=img,Keywords=Keyword,Integrates=Integrates)
        message = "Product Add Success"
        return render(request,"app/chef/product-add.html",{'msg':message})



def ShowProduct(request):
    print("--------------ShowProduct---------------")
    all_pro = Product.objects.all()
   
    return render(request,"app/shop-page.html",{'key3':all_pro})
   


def ProductDescription(request,pk):
    pro = Product.objects.get(pk=pk)
    print("Product----------------------->",pro)
    return render(request,"app/shop-single.html",{'key4':pro})

def Chefdetail(request,pk):
   # udata=User.objects.get(id=pk)
    cdata=Chef.objects.get(id=pk)
    print("==========cdata",pk)
    return render(request,"app/about.html",{'cdata':cdata})




def ShopSinglePage(request):
    return render(request,"app/shop-single.html")


def ChefShowProduct_Page(request,pk):
    print("--------------Before Update ShowProductPage---------------",pk)
    pdata = User.objects.get(id=pk)
    print("======================After Update Show Product Id=======",pdata)
    if pdata.Role == "Chef":
        page_id = Chef.objects.get(user_id=pdata)
        pro = Product.objects.all().filter(chef_id=page_id)
        return render(request,"app/chef/product.html",{'key5':pro})



def EditProduct(request,pk):
    pdata = Product.objects.get(pk=pk)
    return render(request,"app/chef/productEdit.html",{'key6':pdata})
    


def UpdateProduct(request,pk):
    pdata = Product.objects.get(pk=pk)
    print("============PDATA=================",pdata)
    pdata.Productname = request.POST['Productname']
    pdata.ProductDescription = request.POST['ProductDescription']
    pdata.Price = request.POST['Price']
    pdata.Expirydate = request.POST['Expirydate']
    pdata.Mfgdate = request.POST['Mfgdate']
    pdata.Detail = request.POST['Detail']
    pdata.Status = request.POST['Status']
    pdata.Keywords = request.POST['Keyword']
    pdata.save()
    udata = request.session['id']
    print("===========Product UDATA=================",udata)
    url = f"/chefshowproductpage/{udata}"
    print("=================URL================",url)
    return redirect(url)


def DeleteProduct(request,pk):
    ddata = Product.objects.get(pk=pk)
    ddata.delete()
    udata = request.session['id']
    print("===========Product UDATA=================",udata)
    url = f"/chefshowproductpage/{udata}"
    print("=================URL================",url)
    return redirect(url)


def LogoutChef(request):
    del request.session['id']
    del request.session['Firstname']
    del request.session['Email']
    del request.session['Role']
    return HttpResponseRedirect(reverse('index'))

def LogoutCustomer(request):
    del request.session['id']
    del request.session['Firstname']
    del request.session['Email']
    del request.session['Role']
    return HttpResponseRedirect(reverse('index'))



def Addtocart(request,pk):
    udata = User.objects.get(id=pk)
    if udata.Role=="Customer":
        cust = Customer.objects.get(user_id=udata)
        cid = request.POST['chefid']
        chefid = Chef.objects.get(id=cid)
        pid = request.POST['proid']
        proid = Product.objects.get(id=pid)
        price = int(request.POST['pprice'])
        qty = int(request.POST['qty'])
        proname = request.POST['pname']
        total = price * qty
        newpro = Shopping_cart.objects.create(Cust_id=cust,pro_id=proid,Quantity=qty,Productname=proname,Price=price,Total=total)
       
        url = f"/cartpro/{pk}"
        return redirect(url)





def CartProduct(request,pk):
    udata = User.objects.get(id=pk)
    sub_total=0
    if udata.Role=="Customer":
        cust = Customer.objects.get(user_id=udata)
        c_pro = Shopping_cart.objects.all().filter(Cust_id=cust)
        for t in c_pro:
            sub_total += t.Total
        print(sub_total)
        
        return render(request,"app/cart-page.html",{'key9':c_pro,'sub_total':sub_total})
    else:
        print("============ERROR===========")


def Proceedtocheckout(request,pk):
    udata = User.objects.get(id=pk)
    sub_total = 0
    if udata.Role=="Customer":
        cdata = Customer.objects.get(user_id=udata)
        all_data1=Shopping_cart.objects.all().filter(Cust_id=cdata)
        for t in all_data1:
            sub_total += t.Total
        return render(request,"app/checkout.html",{'keyp':all_data1,'keyc':cdata,'sub_total':sub_total})



def AddCaategory(request,pk):
    udata = User.objects.get(id=pk)
    if udata.Role=="Chef":
        cid = Chef.objects.get(user_id=udata)
        catname = request.POST['catname']
        catimg = request.FILES['catimg']
        newcat = Category.objects.create(chef_id=cid,Productname=catname,Image=catimg)
        message = "Category Added SuccessFully"
        return render(request,"app/chef/catpage.html",{'msg':message})
    else:
        print("*********************ERROR while adding Category*************")
        message = "User Doesnot matching the Role"
        return render(request,"app/chef/catpage.html",{'msg':message})



def ShowCatPro(request,pk):
    udata = User.objects.get(id=pk)
    if udata.Role=="Chef":
        cid = Chef.objects.get(user_id=udata)
        all_cat = Category.objects.all().filter(chef_id=cid)
        return render(request,"app/chef/product-add.html",{'all_cat':all_cat})



def MenuCard(request):
    all_cat = Category.objects.all()
    return render(request,"app/menu-card-3.html",{'all_cat':all_cat})

def OpenproductsbyCategory(request,pk):
    pdata=Product.objects.all().filter(cat_id=pk)
    return render(request,"app/shop-page.html",{'key3':pdata})

def allorder(request):
    odata=Transaction.objects.all()
    return render(request,"app/chef/product-order.html",{'key4':odata})







############################################# Paytm Block #################################################

def initiate_payment(request):
    try:
        udata = User.objects.get(Email=request.session['Email'])
        amount = int(request.POST['sub_total'])
        #user = authenticate(request, username=username, password=password)
    except Exception as err:
        print(err)
        return render(request, 'app/checkout.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=udata, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.Email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'app/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'app/callback.html', context=received_data)
        return render(request, 'app/callback.html', context=received_data)


################################################## ADMIN PROCESS###########################################

def Openadminindexpage(request):
    return render(request,"app/admin/index.html")

def LoginadminPage(request):
    return render(request,"app/admin/login.html")

def AdminLogin(request):
    uname = request.POST['username']
    password = request.POST['password']

    if uname=="admin" and password=="admin":
        request.session['username'] = uname
        request.session['password'] = password

        return render(request,"app/admin/index.html")
    else:
        message = "Username or Password doesnot match"
        return render(request,"app/admin/login.html",{'msg':message})



def AdminUserTablePage(request):
    all_chef = Chef.objects.all()
    return render(request,"app/admin/tables.html",{'key7':all_chef})



def AdminChefEditPage(request,pk):
    udata = User.objects.get(id=pk)
    if udata.Role=="Chef":
        c_id = Chef.objects.get(user_id=udata)
        return render(request,"app/admin/admineditpage.html",{'udata':udata,'cid':c_id})

def AdminUpdatePage(request,pk):
    adata = User.objects.get(pk=pk)
    adata.is_verified = request.POST['is_verified']
    adata.is_active = request.POST['is_active']
    print("-----------------ADATA",adata)
    adata.save()
    return HttpResponseRedirect(reverse('admintablepage'))

def AdminDeletePage(request,pk):
    rdata = User.objects.get(pk=pk)
    rdata.delete()
    return HttpResponseRedirect(reverse('admintablepage'))









