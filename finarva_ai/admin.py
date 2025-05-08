from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.contrib.auth.models import User, Group
from django.db.models import Count, Sum
from dashboard.models import SalesPerformance, CustomerLead, AIInsight, PerformanceGoal
from accounts.models import UserProfile, Skill, LearningProgress
from ai_assistant.models import Conversation, Message, AIResponse, LearningContent, SalesTemplate
from django.utils import timezone
from datetime import timedelta
from django.contrib.sites.models import Site

# Import all admin classes
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.sites.admin import SiteAdmin
from dashboard.admin import SalesPerformanceAdmin, CustomerLeadAdmin, AIInsightAdmin, PerformanceGoalAdmin
from ai_assistant.admin import ConversationAdmin, MessageAdmin, AIResponseAdmin, LearningContentAdmin, \
    SalesTemplateAdmin


class FinArvaAdminSite(AdminSite):
    """
    Standard admin site with enhanced dashboard
    """
    site_header = 'FinArva AI Administration'
    site_title = 'FinArva AI Admin'
    index_title = 'Administration Portal'

    def index(self, request, extra_context=None):
        """Enhanced admin dashboard with stats"""
        # Get date range for stats
        today = timezone.now().date()
        start_date = today - timedelta(days=30)

        # Calculate various stats
        total_users = User.objects.count()
        active_users = User.objects.filter(last_login__gte=start_date).count()

        total_sales = SalesPerformance.objects.filter(date__gte=start_date).count()
        total_sales_amount = SalesPerformance.objects.filter(date__gte=start_date).aggregate(sum=Sum('amount'))[
                                 'sum'] or 0
        total_commission = SalesPerformance.objects.filter(date__gte=start_date).aggregate(sum=Sum('commission'))[
                               'sum'] or 0

        product_distribution = SalesPerformance.objects.filter(date__gte=start_date).values(
            'product_category').annotate(count=Count('id')).order_by('-count')

        total_leads = CustomerLead.objects.count()
        new_leads = CustomerLead.objects.filter(status='new').count()
        contacted_leads = CustomerLead.objects.filter(status='contacted').count()
        interested_leads = CustomerLead.objects.filter(status='interested').count()
        converted_leads = CustomerLead.objects.filter(status='converted').count()

        total_insights = AIInsight.objects.count()
        total_responses = AIResponse.objects.count()

        recent_sales = SalesPerformance.objects.all().order_by('-date')[:10]
        recent_leads = CustomerLead.objects.all().order_by('-created_at')[:10]

        context = {
            'title': 'FinArva AI Admin Dashboard',
            'total_users': total_users,
            'active_users': active_users,
            'total_sales': total_sales,
            'total_sales_amount': total_sales_amount,
            'total_commission': total_commission,
            'product_distribution': product_distribution,
            'total_leads': total_leads,
            'new_leads': new_leads,
            'contacted_leads': contacted_leads,
            'interested_leads': interested_leads,
            'converted_leads': converted_leads,
            'total_insights': total_insights,
            'total_responses': total_responses,
            'recent_sales': recent_sales,
            'recent_leads': recent_leads,
            'start_date': start_date,
            'today': today
        }

        if extra_context:
            context.update(extra_context)

        return super().index(request, context)


# Create the admin site instance
admin_site = FinArvaAdminSite(name='admin')

# Register models with the admin site
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(Site, SiteAdmin)
admin_site.register(UserProfile)
admin_site.register(Skill)
admin_site.register(LearningProgress)
admin_site.register(SalesPerformance, SalesPerformanceAdmin)
admin_site.register(CustomerLead, CustomerLeadAdmin)
admin_site.register(AIInsight, AIInsightAdmin)
admin_site.register(PerformanceGoal, PerformanceGoalAdmin)
admin_site.register(Conversation, ConversationAdmin)
admin_site.register(Message, MessageAdmin)
admin_site.register(AIResponse, AIResponseAdmin)
admin_site.register(LearningContent, LearningContentAdmin)
admin_site.register(SalesTemplate, SalesTemplateAdmin)