from django.conf.urls import patterns,include,url
from . import views
from django.conf.urls.static import static
urlpatterns = [
    url(r'^$',views.pressrelease_short, name='pressrelease_short'),
    url(r'^signup/$', views.register, name='sign_up'),
    url(r'^article/new/$', views.upload, name='talk_new'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^register_edit/(?P<pk>\d+)/edit/$', views.user_edit, name='register_edit'),
    url(r'^articles/list/$', views.talks_list, name='talks_list'),
    url(r'^articles/(?P<pk>\d+)/part/$', views.talk_part, name='talk_part'), 
    url(r'^articles/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^like/(?P<pk>\d+)/$', views.like, name='like'),
    url(r'^dislike/(?P<pk>\d+)/$', views.dislike, name='dislike'),
    url(r'^googlenews/$', views.news, name='news'),   
    url(r'^books/$', views.books, name='books'),
    url(r'^clothing/$', views.clothing, name='clothing'),
    url(r'^ereader/$', views.ereader, name='ereader'),
]

