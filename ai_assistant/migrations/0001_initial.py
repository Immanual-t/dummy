# Generated by Django 5.2 on 2025-05-05 10:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AIResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(choices=[('copilot', 'Sales Co-Pilot'), ('learning', 'Learning Content'), ('lead', 'Lead Suggestion'), ('message', 'Customer Message')], max_length=20)),
                ('prompt', models.TextField()),
                ('response', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ai_responses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_type', models.CharField(choices=[('new', 'New Customer'), ('existing', 'Existing Customer'), ('referred', 'Referred Customer')], max_length=20)),
                ('product_type', models.CharField(choices=[('insurance', 'Insurance'), ('credit_card', 'Credit Card'), ('loan', 'Loan'), ('savings', 'Savings Account'), ('demat', 'Demat Account'), ('investment', 'Investment')], max_length=20)),
                ('title', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LearningContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(choices=[('insurance', 'Insurance'), ('credit_card', 'Credit Card'), ('loan', 'Loan'), ('savings', 'Savings Account'), ('demat', 'Demat Account'), ('investment', 'Investment')], max_length=20)),
                ('topic', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('summary', models.TextField()),
                ('difficulty_level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learning_content', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('user', 'User'), ('assistant', 'Assistant'), ('system', 'System')], max_length=10)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='ai_assistant.conversation')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='SalesTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(choices=[('insurance', 'Insurance'), ('credit_card', 'Credit Card'), ('loan', 'Loan'), ('savings', 'Savings Account'), ('demat', 'Demat Account'), ('investment', 'Investment')], max_length=20)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('template_type', models.CharField(choices=[('pitch', 'Sales Pitch'), ('objection', 'Objection Handling'), ('followup', 'Follow-up Message'), ('closing', 'Closing Script')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_templates', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
