from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_multipart),
    path('register/team/<str:team_id>', views.register_team_payment),
    path('register/member/ktm/<str:member_id>', views.register_member_ktm),
    path('register/member/aktif/<str:member_id>', views.register_member_active),
    path('register/member/3x4/<str:member_id>', views.register_member_3x4),
    path('register/member/instagram/<str:member_id>', views.register_member_follow_instagram),
    path('register/member/twibbon/<str:member_id>',
         views.register_member_twibbon),
    path('uploads/<str:team_name>/<str:filename>', views.get_uploads),
    # path('upload_drive', views.upload_to_google_drive)
]
