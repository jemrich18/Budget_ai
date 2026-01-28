from rest_framework import serializers
from .models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    ai_suggested_category_name = serializers.CharField(source='ai_suggested_category.name', read_only=True)
    
    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'category', 'category_name', 
            'description', 'notes', 'date', 
            'created_at', 'updated_at',
            'ai_suggested_category', 'ai_suggested_category_name', 'ai_confidence'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'ai_suggested_category', 'ai_confidence']
    
    def create(self, validated_data):
        from apps.ai_services.services import ExpenseCategorizationService
        
        # Automatically assign the current user
        validated_data['user'] = self.context['request'].user
        
        # Get AI suggestion if no category provided
        if not validated_data.get('category'):
            try:
                ai_service = ExpenseCategorizationService()
                suggested_category_name, confidence = ai_service.categorize_expense(
                    description=validated_data.get('description', ''),
                    notes=validated_data.get('notes', ''),
                    amount=validated_data.get('amount')
                )
                
                # Try to find the category
                if suggested_category_name:
                    try:
                        suggested_category = Category.objects.get(name=suggested_category_name)
                        validated_data['ai_suggested_category'] = suggested_category
                        validated_data['ai_confidence'] = confidence
                        # Auto-assign if confidence is high
                        if confidence > 0.8:
                            validated_data['category'] = suggested_category
                    except Category.DoesNotExist:
                        pass
            except Exception as e:
                print(f"AI categorization failed: {e}")
        
        return super().create(validated_data)


class ExpenseListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'category_name', 'description', 'date']