from django.urls import path

from myapp import views

urlpatterns = [
    path('login/',views.login),
    path('login_post/',views.login_post),

    path('home/',views.home),
    path('admin_change_password/',views.admin_change_password),
    path('admin_change_password_post/',views.admin_change_password_post),
    path('logout/',views.logout),
    path('view_user/',views.view_user),
    path('view_user_post/',views.view_user_post),
    path('view_complaint/', views.view_complaint),
    path('view_complaint_post/', views.view_complaint_post),
    path('view_feedback/', views.view_feedback),
    path('view_feedback_post/', views.view_feedback_post),
    path('view_manufacture/', views.view_manufacture),
    path('view_manufacture_post/', views.view_manufacture_post),
    path('aproving_manufacture/<id>', views.aproving_manufacture),
    path('reject_Manufacture/<id>', views.reject_Manufacture),
    path('view_aproved_manufacture/', views.view_aproved_manufacture),
    path('view_aproved_manufacture_post/', views.view_aproved_manufacture_post),
    path('view_reject_manufacture/', views.view_reject_manufacture),
    path('view_reject_manufacture_post/', views.view_reject_manufacture_post),
    path('send_reply/<id>', views.send_reply),
    path('send_reply_post/', views.send_reply_post),

    # manufacture
    path('manufacture/', views.manufacture),
    path('manufacture_post/', views.manufacture_post),
    path('manufacture_home/', views.manufacture_home),
    path('manufacture_profile/', views.manufacture_profile),
    path('edit_manu/<id>', views.edit_manu),
    path('edit_manu_post/', views.edit_manu_post),
    path('manu_change_password/', views.manu_change_password),
    path('manu_change_password_post/', views.manu_change_password_post),
    path('category/', views.category),
    path('category_post/', views.category_post),
    path('view_category/', views.view_category),
    path('view_category_post/', views.view_category_post),
    path('edit_category/<id>', views.edit_category),
    path('edit_category_post/', views.edit_category_post),
    path('delete_category/<id>', views.delete_category),
    path('add_product/', views.add_product),
    path('add_product_post/', views.add_product_post),
    path('view_product/', views.view_product),
    path('view_product_post/', views.view_product_post),
    path('delete_product/<id>', views.delete_product),
    path('edit_product/<id>', views.edit_product),
    path('edit_product_post/', views.edit_product_post),

    path('user/', views.user),
    path('user_post/', views.user_post),
    path('user_home/', views.user_home),
    path('user_change_password/', views.user_change_password),
    path('user_profile/', views.user_profile),
    path('edit_profile/<id>', views.edit_profile),
    path('edit_profile_post/', views.edit_profile_post),
    path('send_complaint_post/', views.send_complaint_post),
    path('send_complaint/', views.send_complaint),
    path('userview_complaint/', views.userview_complaint),
    path('userview_complaint_post/', views.userview_complaint_post),
    path('send_feedback_post/', views.send_feedback_post),
    path('sendreviewrating/', views.sendfeedbackrating),
    path('sendreviewrating_post/', views.send_feedback_post),






    path('login2/', views.login2),
    path('user_post_new/', views.user_post_new),
    path('user_profile_new/', views.user_profile_new),
    path('edit_userprofile/', views.edit_userprofile),
    path('user_view_complaints/', views.user_view_complaints),
    path('user_complaint_post/', views.user_complaint_post),
    path('user_changepassword/', views.user_changepassword),
    path('user_feedback_post/', views.user_feedback_post),


#     phishing

    path('detect/',views.detect),
    # path('detect_result/',views.detect_result),
]
