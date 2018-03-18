from django.conf.urls import url
from .import views
app_name="products"
urlpatterns=[

    url(r'^$',views.index,name='index'),
    url(r'^kitchen/$', views.kitchen, name='kitchen'),
    url(r'^hold/$', views.hold, name='hold'),
    url(r'^care/$', views.care, name='care'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^single/(?P<item_id>\w+)$', views.single_page, name='single'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^add/(?P<item_id>\w+)$', views.add_cart, name='add'),
    url(r'^remove/(?P<item_id>\w+)$', views.remove_cart, name='remove'),

]