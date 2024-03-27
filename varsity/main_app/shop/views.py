from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from main_app.models import ShopProduct
from main_app.serializers import ShopSerializers

class CreateProductView(ModelViewSet):
   queryset = ShopProduct.objects.all()
   serializer_class = ShopSerializers