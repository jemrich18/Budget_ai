import os
from anthropic import Anthropic
from apps.expenses.models import Category
from django.conf import settings
from pathlib import Path
from dotenv import load_dotenv


class ExpenseCategorizationService:
    """Service for AI-powered expense categorization"""
    
    def __init__(self):
        # Load environment variables
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        load_dotenv(BASE_DIR.parent / '.env')
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = Anthropic(api_key=api_key)
    
    def categorize_expense(self, description, notes="", amount=None):
        """
        Use Claude to suggest a category for an expense
        
        Returns: (category_name, confidence_score)
        """
        # Get available categories
        categories = Category.objects.all().values_list('name', flat=True)
        categories_list = ", ".join(categories)
        
        # Build the prompt
        prompt = f"""You are an expense categorization assistant. Given an expense description, suggest the most appropriate category.

Available categories: {categories_list}

Expense description: {description}
{f"Additional notes: {notes}" if notes else ""}
{f"Amount: ${amount}" if amount else ""}

Respond with ONLY the category name from the available categories list. If none fit well, respond with "Uncategorized"."""

        try:
            # Call Claude API
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=100,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract the suggested category
            suggested_category = message.content[0].text.strip()
            
            # Calculate confidence (simplified - you could make this more sophisticated)
            confidence = 0.85 if suggested_category in categories else 0.5
            
            return suggested_category, confidence
            
        except Exception as e:
            print(f"Error categorizing expense: {e}")
            return None, 0.0
        
class ExpenseQueryService:
    """Service for natural language queries about expenses"""
    
    def __init__(self):
        # Load environment variables
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        load_dotenv(BASE_DIR.parent / '.env')
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = Anthropic(api_key=api_key)
    
    def query_expenses(self, user, query):
        """
        Answer natural language questions about user's expenses
        
        Returns: AI-generated response
        """
        from apps.expenses.models import Expense
        
        # Get user's expenses
        expenses = Expense.objects.filter(user=user).select_related('category')
        
        # Build expense summary
        expense_data = []
        for expense in expenses:
            expense_data.append({
                'description': expense.description,
                'amount': float(expense.amount),
                'category': expense.category.name if expense.category else 'Uncategorized',
                'date': str(expense.date),
                'notes': expense.notes
            })
        
        # Build the prompt
        prompt = f"""You are a financial assistant helping a user understand their expenses. 

Here is their expense data:
{expense_data}

User question: {query}

Provide a helpful, concise answer based on the expense data. Include specific numbers and insights when relevant."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"