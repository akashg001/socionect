"""socionect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import notifications.urls
from django.contrib import admin
from django.urls import path,include
from home import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.dashboard,name="home"),
    path('handlelogin/',views.handlelogin,name='handlelogin'),
    path('register/',views.register,name="register"),
    path('signup/',views.signup,name="signup"),
    path('handleSignup/',views.handleSignup,name="handleSignup"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('handlelogout/',views.handlelogout,name="handlelogout"),
    path('likepost/<id>',views.likepost,name="likepost"),
    path('post_picture/',views.post_picture,name="post_picture"),
    path('direct/<username>', views.Directs, name="directs"),
    path('search/',views.search,name="search"),
    path('notifications/',views.notifications,name='notifications'),
    path('send/', views.SendDirect, name="send-directs"),
    path('new/<username>', views.NewConversation, name="conversation"),
    path('inbox/',views.inbox,name="inbox"),
    path('profile/<id>',views.profile,name="profile"),
    path('follow/<id>',views.follow,name="follow"),
    path('explore/',views.explore,name="explore"),
    path('commenting/<pk>',views.commenting,name="commenting"),
    path('show/<id>',views.show,name="show"),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

