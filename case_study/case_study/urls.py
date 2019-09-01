"""case_study URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from app.views import FundViewSet, CommitViewSet, CallViewSet, FundInvestViewSet, DashboardViewSet, CalculateViewSet

fund_list = FundViewSet.as_view({'get': 'list','post':'create'})
fund_detail = FundViewSet.as_view({'get': 'retrieve','put':'update'})

commit_list = CommitViewSet.as_view({'get': 'list','post':'create'})
commit_detail = CommitViewSet.as_view({'get': 'retrieve'})

call_list = CallViewSet.as_view({'get': 'list','post':'create'})
call_detail = CallViewSet.as_view({'get': 'retrieve'})

fundinvest_list = FundInvestViewSet.as_view({'get': 'list','post':'create'})
fundinvest_detail = FundInvestViewSet.as_view({'get': 'retrieve'})

summary_list = DashboardViewSet.as_view({'get': 'list'})

calculateSummary_list = CalculateViewSet.as_view({'get': 'list'})
# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'funds', FundViewSet, basename='fund')
router.register(r'commits', CommitViewSet, basename='commit')
router.register(r'calls', CallViewSet, basename='call')
router.register(r'invests', FundInvestViewSet, basename='invest')
router.register(r'summary', DashboardViewSet, basename='summary')
router.register(r'calculate', CalculateViewSet, basename='calculate')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
