from django.urls import path, re_path

from catalog.views import CatalogView, ActualCatalogView, ElementView, ValidateElementView, ElementCurrentVersionView

app_name = 'catalog'


urlpatterns = [
   path('catalogs/get-all/', CatalogView.as_view()),
   path('catalogs/get-actual/', ActualCatalogView.as_view()),
   path('elements/get-by-current-version/', ElementCurrentVersionView.as_view()),
   path('elements/validate/', ValidateElementView.as_view()),
   path('elements/get-by-version/', ElementView.as_view()),
]
