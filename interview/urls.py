from .api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"scopes", views.ScopeView)
router.register(r"news", views.NewsView)
router.register(r"subscopes", views.SubScopeView, basename='SubScope')
router.register(r"questions", views.QuestionsView, basename='Question')
router.register(r"professions", views.ProfessionsView, basename='Profession')
router.register(r"suggest", views.SuggestedQuestionsView, basename='SuggestQuestion')
