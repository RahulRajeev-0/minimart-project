# views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer


# views 
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    
    def get_queryset(self):
        return Category.objects.filter(is_active=True)

    # Soft delete 
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'detail': 'Category soft-deleted'}, 
                        status=status.HTTP_204_NO_CONTENT)
