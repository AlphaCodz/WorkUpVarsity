from courses.models import Ebook, MyEbooks
from courses.serializers import EbookSerializer, BuyEbookSerializer
from rest_framework.viewsets import ModelViewSet


class CreateEbook(ModelViewSet):
   queryset = Ebook.objects.all()
   serializer_class = EbookSerializer


class BuyEbookView(ModelViewSet):
   queryset = MyEbooks.objects.select_related("user", "ebook")
   serializer_class = BuyEbookSerializer