from django.urls import path

from delivery import views
from delivery.views import *

urlpatterns = [
    path('createUser/', createUsersViewSet.as_view(), name='createUsersViewSet'),
    path('loginUser/', loginUsersViewSet.as_view(), name='loginUsersViewSet'),
    path('login/', login_user, name='login_user'),
    path('products/', get_product_info, name='get_product_info'),
    path('info-sectors/', get_info_sector_info, name='get_info_sector_info'),
    path('history/', HistoryView.as_view(), name='history_view'),
    path('filter_history/', filter_history, name='filter_products'),
     
]
 