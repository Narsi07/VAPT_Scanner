# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import path

from user_management import views

app_name = "users"

urlpatterns = [
    # Your URLs...
    path("list_user/", views.UsersList.as_view(), name="list_user"),
    path("edit_user/<str:uu_id>/", views.UsersEdit.as_view(), name="edit_user"),
    path("add_user/", views.UsersAdd.as_view(), name="add_user"),
    path("profile/", views.Profile.as_view(), name="profile"),
    path("roles/", views.Roles.as_view()),
    path("roles/<str:uu_id>/", views.Roles.as_view()),
    path("list_org/", views.OrganizationDetail.as_view(), name="list_org"),
    path("edit_org/<str:uu_id>/", views.OrgEdit.as_view(), name="edit_org"),
    path("add_org/", views.OrgAdd.as_view(), name="add_org"),
]
