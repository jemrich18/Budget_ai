from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer, ExpenseListSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.ai_services.services import ExpenseQueryService


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for expenses
    """
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'date']
    search_fields = ['description', 'notes']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']
    
    def get_queryset(self):
        # Only return expenses for the current user
        return Expense.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        # Use lighter serializer for list views
        if self.action == 'list':
            return ExpenseListSerializer
        return ExpenseSerializer
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def query_expenses(request):
    """
    Natural language query endpoint
    """
    query = request.data.get('query', '')
    
    if not query:
        return Response({'error': 'Query is required'}, status=400)
    
    try:
        service = ExpenseQueryService()
        response_text = service.query_expenses(request.user, query)
        return Response({'query': query, 'response': response_text})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
