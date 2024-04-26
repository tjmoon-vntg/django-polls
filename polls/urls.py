from django.urls import include, path

# from django.conf.urls import url
# from rest_framework.urlpatterns import format_suffix_patterns

from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api',views.ApiIndexView)

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path('api/', views.ApiIndexView.as_view()),
    path('',include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # url(r'^api/questions/',views.questionList.as_view()),
    # url(r'^api/choices/',views.choiceList.as_view()),
]
