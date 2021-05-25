import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Catalog, Element
from catalog.serializers import CatalogSerializer, ElementSerializer


class CatalogView(APIView, LimitOffsetPagination):
    """
    Получение списка справочников
    """

    # Настройка отображения Swagger
    limit_param = openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                    description='Количество элементов на странице', default=10)

    @swagger_auto_schema(
        tags=['Получение списка справочников'],
        operation_id='All catalogs',
        operation_description='Получение списка справочников',
        responses={
            '200': 'OK',
            '400': 'Bad request'
        },
        manual_parameters=[limit_param]
    )


    def get(self, request):
        try:
            queryset = Catalog.objects.all()
            result = self.paginate_queryset(queryset, request)
            serializer = CatalogSerializer(result, many=True)
            return self.get_paginated_response(serializer.data)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ActualCatalogView(APIView, LimitOffsetPagination):
    """
    Получение списка справочников, актуальных на указанную дату
    """
    # Настройка отображения Swagger
    limit_param = openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                    description='Количество элементов на странице', default=10)
    date_param = openapi.Parameter('date', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                                   description='Дата для проверки актуальности', default=str(datetime.date.today()))

    @swagger_auto_schema(
        tags=['Получение списка справочников'],
        operation_id='Actual catalogs',
        operation_description='Получение списка справочников, актуальных на указанную дату',
        responses={
            '200': 'OK',
            '400': 'Bad request'
        },
        manual_parameters=[limit_param, date_param]
    )
    def get(self, request):
        try:
            queryset = Catalog.objects.filter(date__lte=request.query_params.get('date'))
            result = self.paginate_queryset(queryset, request)
            serializer = CatalogSerializer(result, many=True)
            return self.get_paginated_response(serializer.data)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ElementCurrentVersionView(APIView, LimitOffsetPagination):
    """
    Получение элементов заданного справочника текущей версии
    """
    # Настройка отображения Swagger
    limit_param = openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                    description='Количество элементов на странице', default=10)
    date_param = openapi.Parameter('date', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                                   description='Дата для проверки текущей версии', default=str(datetime.date.today()))
    id_param = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                 description='Id справочника для проверки', default=1)

    @swagger_auto_schema(
        tags=['Получение элементов справочника'],
        operation_id='Current version catalogs',
        operation_description='Получение элементов заданного справочника текущей версии',
        responses={
            '200': 'OK',
            '400': 'Bad request'
        },
        manual_parameters=[limit_param, date_param, id_param]
    )
    def get(self, request):
        try:
            queryset = Element.objects.filter(catalog_id__date__lte=request.query_params.get('date'),
                                              catalog_id=request.query_params.get('id'))
            result = self.paginate_queryset(queryset, request)
            serializer = ElementSerializer(result, many=True)
            return self.get_paginated_response(serializer.data)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ValidateElementView(APIView):
    """
    Валидация элементов заданного справочника текущей версии
    и валидация элемента заданного справочника по указанной версии
    """

    # Настройки Swagger
    @swagger_auto_schema(
        tags=['Валидация элементов'],
        operation_id='Validation',
        operation_description='Валидация элементов справочника',
        responses={
            '200': 'OK',
            '400': 'Bad request'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'catalog_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                             description='Идентификатор справочника(Catalog ID)', default=1),
                'element_code': openapi.Schema(type=openapi.TYPE_STRING,
                                               description='код элемента (тип: строка, не может быть пустой)',
                                               default='Example element code'),
                'element_value': openapi.Schema(type=openapi.TYPE_STRING,
                                                description='значение элемента (тип: строка, не может быть пустой)',
                                                default='Example element value'),

            }
        )
    )
    def post(self, request):
        serializer = ElementSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'All fields are valid': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElementView(APIView, LimitOffsetPagination):
    """
    Получение элементов заданного справочника указанной версии
    """
    # Настройка отображения Swagger
    limit_param = openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                    description='Количество элементов на странице', default=10)
    version_param = openapi.Parameter('version', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                                      description='Версия для проверки', default="1.0")
    id_param = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                 description='Id справочника для проверки', default=1)

    @swagger_auto_schema(
        tags=['Получение элементов справочника'],
        operation_id='Get catalogs by version',
        operation_description='Получение элементов заданного справочника указанной версии',
        responses={
            '200': 'OK',
            '400': 'Bad request'
        },
        manual_parameters=[limit_param, version_param, id_param]
    )
    def get(self, request):
        try:
            queryset = Element.objects.filter(catalog_id__version=request.query_params.get('version'),
                                              catalog_id=request.query_params.get('id'))
            result = self.paginate_queryset(queryset, request)
            serializer = ElementSerializer(result, many=True)
            return self.get_paginated_response(serializer.data)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
