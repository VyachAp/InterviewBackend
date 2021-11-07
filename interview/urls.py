from .api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"scopes", views.ScopeView, basename='Scope')
router.register(r"news", views.NewsView)
router.register(r"subscopes", views.SubScopeView, basename='SubScope')
router.register(r"questions", views.QuestionsView, basename='Question')
router.register(r"professions", views.ProfessionsView, basename='Profession')
router.register(r"suggest", views.SuggestedQuestionsView, basename='SuggestQuestion')
router.register(r"posts", views.RetrievePostsView, basename='Post')
router.register(r"create_post", views.CreatePostView, basename='CreatePost')
router.register(r"like_post", views.PostLikeView, basename='LikePost')
router.register(r"feedback", views.FeedbackView, basename='feedback')
