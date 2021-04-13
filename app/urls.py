from django.urls import path,include
from . import views
urlpatterns = [

    # Page Url
    path("",views.IndexPage,name="index"),
    path("loginpage/",views.LoginPage,name="loginpage"),
    path("catpage/",views.CatPage,name="catpage"),
    path("signuppage/",views.SingupPage,name="signuppage"),
    path("signuppagechef/",views.SingupChefPage,name="signupchefpage"),
    path("insert/",views.Insertdata,name="insert"),
    path("login/",views.LoginUser,name="login"),
    path("loginchef/",views.LoginChefPage,name="loginchef"),
    path("show/",views.Showpage,name="show"),
    path("welcomeback/",views.customerhome,name="welcomeback"),
    path("display/<int:pk>",views.DisplayData,name="display"),
    path("edit/<int:pk>",views.EditPage,name="edit"),
    path("update/<int:pk>",views.UpdateData,name="update"),
    path("chefedit/<int:pk>",views.ChefAlldata,name="chefedit"),
    path("chefeditprofile/",views.ChefEditProfilePage,name="chefeditprofile"),
    path("ChefProductadd/",views.ChefProduct_add,name="ChefProductadd"),
    path("allorders/",views.allorder,name="allorders"),
    path("add/<int:pk>",views.Addproduct,name="add"),
    path("shoppage/",views.CustomerShop_page,name="shoppage"),
    path("showallproduct/",views.ShowProduct,name="showproduct"),
    path("showallproductbycategory/<int:pk>",views.OpenproductsbyCategory,name="productbycategory"),
    path("productdes/<int:pk>",views.ProductDescription,name="productdes"),
    path("shopsinglepage/",views.ShopSinglePage,name="shopsinglepage"),
    path("chefproductpage/",views.Product_Page,name="chefproductpage"),
    path("chefshowproductpage/<int:pk>",views.ChefShowProduct_Page,name="chefshowproductpage"),
    path("editproduct/<int:pk>",views.EditProduct,name="editproduct"),
    path("updateproduct/<int:pk>",views.UpdateProduct,name="updateproduct"),
    path("deleteproduct/<int:pk>",views.DeleteProduct,name="deleteproduct"),
    path("logoutchef/",views.LogoutChef,name="logoutchef"),
    path("logoutcustomer/",views.LogoutCustomer,name="logoutcustomer"),
    path("adminindexpage/",views.Openadminindexpage,name="openadminindexpage"),
    path("loginadmin/",views.LoginadminPage,name="loginadmin"),
    path("adminlogin/",views.AdminLogin,name="adminlogin"),
    path("admintablepage/",views.AdminUserTablePage,name="admintablepage"),
    path("adminchefeditpage/<int:pk>",views.AdminChefEditPage,name="adminchefeditpage"),
    path("adminupdate/<int:pk>",views.AdminUpdatePage,name="adminupdate"),
    path("admindelete/<int:pk>",views.AdminDeletePage,name="admindelete"),
    path("verifyotp/",views.VerifyOtp,name="verifyotp"),
    path("addtocart/<int:pk>",views.Addtocart,name="addtocart"),
    path("cartpro/<int:pk>",views.CartProduct,name="cartpro"),
    path("addcat/<int:pk>",views.AddCaategory,name="addcat"),
    path("showcatpro/<int:pk>",views.ShowCatPro,name="showcatpro"),
    path("menupage/",views.MenuCard,name="menupage"),
######################################################## Paytm URLS #########################3
    path("checkout/<int:pk>",views.Proceedtocheckout,name="checkout"),
    path('pay/',views.initiate_payment, name='pay'),
    path('callback/', views.callback, name='callback'),
    
    path('chefdata/<int:pk>',views.Chefdetail,name='chefdata'),
    path('feedback/<int:pk>',views.feedback_submit,name='feedback'),
    
    
]



