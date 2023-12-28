from courses.models import Ebook
from courses.serializers import EbookSerializer
from rest_framework.viewsets import ModelViewSet

class CreateEbook(ModelViewSet):
   queryset = Ebook.objects.all()
   serializer_class = EbookSerializer