# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import include, path

from jiraticketing import views

app_name = "jiraticketing"

urlpatterns = [
    path("jira_setting/", views.JiraSetting.as_view(), name="jira_setting"),
    path(
        "submit_jira_ticket/",
        views.CreateJiraTicket.as_view(),
        name="submit_jira_ticket",
    ),
    path(
        "link_jira_ticket/",
        views.LinkJiraTicket.as_view(),
        name="link_jira_ticket",
    ),
]
