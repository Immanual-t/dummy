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
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('partner_id', models.CharField(blank=True, max_length=10, null=True)),
                ('partner_since', models.DateField(blank=True, null=True)),
                ('monthly_target', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('experience_level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'), ('expert', 'Expert')], default='beginner', max_length=20)),
                ('preferred_products', models.JSONField(blank=True, default=list)),
                ('notification_preferences', models.JSONField(blank=True, default=dict)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LearningProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_name', models.CharField(max_length=100)),
                ('completion_percentage', models.IntegerField(default=0)),
                ('last_activity', models.DateTimeField(auto_now=True)),
                ('completed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learning_progress', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'module_name')},
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(choices=[('insurance', 'Insurance'), ('credit_card', 'Credit Card'), ('loan', 'Loan'), ('savings', 'Savings Account'), ('demat', 'Demat Account'), ('investment', 'Investment')], max_length=20)),
                ('proficiency_level', models.IntegerField(default=1)),
                ('last_assessed', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'product_type')},
            },
        ),
    ]
