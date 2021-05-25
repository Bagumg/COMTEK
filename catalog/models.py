from datetime import date

from django.db import models


class Catalog(models.Model):
    """
    Сущность "Справочник" содержит следующие атрибуты:

    - идентификатор справочника (глобальный и не зависит от версии)
    - наименование
    - короткое наименование
    - описание
    - версия (тип: строка,  не может быть пустой, уникальная в пределах одного справочника)
    - дата начала действия справочника этой версии
    """
    name = models.CharField(max_length=64, verbose_name='наименование')
    slug = models.SlugField(max_length=16, verbose_name='короткое наименование')
    description = models.TextField(verbose_name='описание')
    version = models.CharField(max_length=32, unique=True, blank=False, null=False, verbose_name='версия')
    date = models.DateField(auto_created=True, default=date.today, verbose_name='дата начала', editable=True)

    class Meta:
        verbose_name = 'справочник'
        verbose_name_plural = 'справочники'

    def __str__(self):
        return self.name


class Element(models.Model):
    """
    Сущность "Элемент справочника"

    - идентификатор
    - родительский идентификатор
    - код элемента (тип: строка, не может быть пустой)
    - значение элемента (тип: строка, не может быть пустой)
    """
    catalog_id = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='catalog_id',
                                   verbose_name='родительский идентификатор')
    element_code = models.CharField(max_length=16, blank=False, null=False, verbose_name='код элемента')
    element_value = models.CharField(max_length=32, blank=False, null=False, verbose_name='значение элемента')

    class Meta:
        verbose_name = 'элемент справочника'
        verbose_name_plural = 'элементы справочника'
