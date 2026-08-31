from django.urls import path

from .views import (
    HealthCheckView,
    JobSearchView,
    JobExtractView,
    GenerateEmailView,
    ContactFinderView
)


urlpatterns = [

    path(
        'health/',
        HealthCheckView.as_view(),
        name='health'
    ),

    path(
        'search/',
        JobSearchView.as_view(),
        name='job-search'
    ),

    path(
        'extract/',
        JobExtractView.as_view(),
        name='job-extract'
    ),

    path(
        'generate-email/',
        GenerateEmailView.as_view(),
        name='generate-email'
    ),

    path(
        'contact/',
        ContactFinderView.as_view(),
        name='contact'
    ),
]