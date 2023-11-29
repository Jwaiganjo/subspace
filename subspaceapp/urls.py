from django.contrib import admin
from django.urls import path
from subspaceapp import views

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', views.index, name = 'index'),
  path('about', views.about, name = 'about'),
  path('inner', views.inner, name = 'inner-page'),
  path('subscription', views.subscription, name = 'subscription'),
  path('contact', views.contact, name = 'contact'),
  path('register', views.register, name = 'register'),
  path('login', views.login, name = 'login'),
  path('add/', views.add, name='add'),
  path('renewal', views.renewal, name='renewal'),
  path('delete/<int:id>', views.delete),
  path('edit/<int:id>', views.edit),
  path('update/<int:id>',views.update),
  path('pay/', views.pay, name='pay'),
  path('token/', views.token, name='token'),
  path('stk/', views.stk, name='stk'),
]
