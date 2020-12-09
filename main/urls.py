from django.urls import path

from .views import *

app_name = 'main'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('documentation', faq_page, name='faq'),
    path('support', support_page, name='support'),
    path('create-unit', create_unit_form, name='create-unit'),
    path('list-unit', list_unit, name='list-unit'),
    path('delete/<int:obj_id>', unit_delete, name='unit-delete'),
    path('update/<int:pk>', unit_update, name='unit-update'),
    path('launch-unit', launch_unit, name='launch-unit'),
    path('launch-unit-refresh', launch_refresh, name='launch-refresh'),
    path('add-task', launch_unit_form, name='add-task'),
    path('task-update/<int:pk>', launch_unit_update, name='task-update'),
    path('collected-unit-data', collected_data, name='collected-unit-data'),
    path('collected-unit-data-show/<int:pk>', collected_data_show, name='data-show'),
]
