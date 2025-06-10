from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('',views.user_page, name='user_page'),


    path('register/', views.register_view, name='register_view'),


    #USER
    path('/user_page', views.user_page, name='user_page'),
    path('add_materiel/', views.add_materiel, name='add_materiel'),
    path('edit_view/<int:id>/',views.edit_view, name='edit_view'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('recherche/', views.recherche, name='recherche'),
    path('voir_plus/<int:id>/',views.voir_plus, name='voir_plus'),



    # #ADMIN
    path('admin_page/', views.admin_page, name='admin_page'),
    path('delete_admin/<int:id>/', views.delete_admin, name='delete_admin'),
    path('add_admin_materiel/', views.add_admin_materiel,name='add_admin_materiel'),
    path('edit_view_admin/<int:id>/', views.edit_view_admin, name='edit_view_admin'),
    path('recherche_admin/', views.recherche_admin, name='recherche_admin'),
    path('voir_plus_admin/<int:id>/', views.voir_plus_admin, name='voir_plus_admin'),
    path('add_user/', views.add_user, name='add_user'),

    path('to_block/<int:id>/', views.to_block, name='to_block'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('export/', views.export, name='export'),



     # URL pour afficher le formulaire de changement de mot de passe
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    
    # URL redirigée après succès du changement
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

]




    

    
    


