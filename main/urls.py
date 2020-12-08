from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('documentation', faq_page, name='faq'),
    path('support', support_page, name='support'),
    path('create-unit', create_unit_form, name='create-unit'),
    # path('create-unit-code', create_unit_code_form, name='create-unit-code'),
    path('list-unit', list_unit, name='list-unit'),
    path('delete/<int:obj_id>', unit_delete, name='unit-delete'),
    path('update/<int:pk>', unit_update, name='unit-update'),
    # path('list-unit-code', list_unit_code, name='list-unit-code'),
    path('launch-unit', launch_unit, name='launch-unit'),
    path('collected-unit-data', collected_data, name='collected-unit-data'),
    path('add_task', run_bot)
]
