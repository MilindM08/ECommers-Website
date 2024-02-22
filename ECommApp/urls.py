from.import views
from django.urls import path


urlpatterns = [
   
    path('', views.index, name='index'),
    path('productDetails/<int:pid>', views.productDetails, name='productDetails'),
    path('viewcart/', views.viewcart, name='viewcart'),
    path('addcart/<int:pid>', views.addcart, name='addcart'),
    path('removecart/<int:pid>', views.removecart, name='removecart'),
    path('search/', views.search, name='search'),
    path('range/', views.range, name='range'),
    path('watchList/', views.watchList, name='watchList'),
    path('laptopList/', views.laptopList, name='laptopList'),
    path('mobileList/', views.mobileList, name='mobileList'),
    path('priceOrder/', views.priceOrder, name='priceOrder'),
    path('descpriceOrder/', views.descpriceOrder, name='descpriceOrder'),
    path('updateqty/<int:uval>/<int:pid>', views.updateqty, name='updateqty'),
    path('vieworder/', views.vieworder, name='vieworder'),
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('makePayment/', views.makePayment, name='makePayment'),
    path('myOrders/', views.myOrders, name='myOrders'),
    path('insertProduct/', views.insertProduct, name='insertProduct'),
   # path('send_mail/', views.send_mail, name='send_mail') 
    
]