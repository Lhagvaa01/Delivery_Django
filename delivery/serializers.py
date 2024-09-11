from rest_framework import serializers
from .models import *
from collections import OrderedDict

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['pk', 'TCUSERNAME', 'TCEMAIL', 'TCGENDER']

class InfoSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoSector
        fields = ['pk', 'sectorId', 'name', 'isMain', 'address', 'phone', 'createdDate']

class InfoProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoProduct
        fields = ['pk', 'itemCode', 'itemName', 'itemBillName', 'itemPrice', 'isActive', 'createdDate']


class HistoryProductSerializer(serializers.ModelSerializer):
    product = InfoProductSerializer(read_only=True)

    class Meta:
        model = HistoryProduct
        fields = ['pk', 'product', 'quantity']


class HistorySerializer(serializers.ModelSerializer):
    UserPk = serializers.StringRelatedField()  # Display the username for UserPk
    infoOutSector = serializers.StringRelatedField()  # Display the sector name for infoOutSector
    infoToSector = serializers.StringRelatedField()  # Display the sector name for infoToSector
    history_products = HistoryProductSerializer(source='historyproduct_set', many=True, read_only=True)

    class Meta:
        model = History
        fields = ['pk', 'UserPk', 'infoOutSector', 'infoToSector', 'totalPrice', 'description', 'isIncome', 'createdDate', 'history_products']

    def create(self, validated_data):
        history_products_data = validated_data.pop('history_products', [])
        history = History.objects.create(**validated_data)

        for history_product_data in history_products_data:
            HistoryProduct.objects.create(history=history, **history_product_data)

        return history


class HistoryAddProductSerializer(serializers.ModelSerializer):
    # product = InfoProductSerializer(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=InfoProduct.objects.all())
    class Meta:
        model = HistoryProduct
        fields = ['product', 'quantity']


class HistoryAddSerializer(serializers.ModelSerializer):
    history_products = HistoryAddProductSerializer(source='historyproduct_set', many=True)

    class Meta:
        model = History
        fields = ['UserPk', 'infoOutSector', 'infoToSector', 'totalPrice', 'description', 'isIncome',
                  'history_products']

    def create(self, validated_data):
        history_products_data = validated_data.pop('historyproduct_set')
        history = History.objects.create(**validated_data)

        for history_product_data in history_products_data:
            HistoryProduct.objects.create(history=history, **history_product_data)

        return history

