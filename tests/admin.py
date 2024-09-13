from django.contrib import admin
from .models import Test, Question


class QuestionInline(admin.TabularInline):
    model = Question


class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Test, TestAdmin)
