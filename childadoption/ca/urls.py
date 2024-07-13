from django.urls import path
from ca import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.HomeView.as_view(),name="home"),
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login',views.LoginView.as_view(),name="login"),
    path('logout',views.LogoutView.as_view(),name="logout"),
    # path('sponser/',views.SponserView.as_view(),name="sponser"),
    path('donate/',views.DonationView.as_view(),name="donate"),
    path('privacy/',views.PrivacyView.as_view(),name="privacy"),
    path('adoption/',views.AdoptionRequestView.as_view(),name="adoptionform"),
    path('donatepay/',views.DonatePayment.as_view(),name="donatepay"),
    path('profileedit/<int:pk>/',views.UserProfileEdit.as_view(),name="profileedit"),
    path('profile/<int:pk>/',views.UserProfile.as_view(),name="profile"),
    path('message/',views.MessageView.as_view(),name="messages"),
    path('childconfirm/<int:pk>/',views.SelectChild.as_view(), name='childconfirm'),
    path('save_model/', views.SaveModelView.as_view(), name='save_model'),
    path('sponsor/', views.SponsorChildView.as_view(), name='sponsor_child'),
    path('successsponcer/', views.success_sponcer.as_view(), name='sponsor_success'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)