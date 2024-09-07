from django.contrib import admin
from .models import *

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('TCUSERNAME', 'TCEMAIL', 'TCGENDER')
    search_fields = ('TCUSERNAME', 'TCEMAIL')
    list_filter = ('TCGENDER',)

@admin.register(InfoSector)
class InfoSectorAdmin(admin.ModelAdmin):
    list_display = ('sectorId', 'name', 'isMain', 'address', 'phone', 'createdDate')
    search_fields = ('sectorId', 'name')
    list_filter = ('isMain',)

@admin.register(InfoProduct)
class InfoProductAdmin(admin.ModelAdmin):
    list_display = ('itemCode', 'itemName', 'itemBillName', 'itemPrice', 'isActive', 'createdDate')
    search_fields = ('itemCode', 'itemName')
    list_filter = ('isActive',)

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('UserPk', 'infoOutSector', 'infoToSector', 'totalPrice', 'description', 'isIncome', 'createdDate')
    search_fields = ('UserPk__TCUSERNAME', 'infoOutSector__name', 'infoToSector__name', 'description')
    list_filter = ('isIncome', 'createdDate')

@admin.register(HistoryProduct)
class HistoryProductAdmin(admin.ModelAdmin):
    list_display = ('history', 'product', 'quantity')
    search_fields = ('history__UserPk__TCUSERNAME', 'product__itemName')
