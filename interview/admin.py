from django.contrib import admin
from interview.models import Scope, Profession, Questions, SubScope, ProfessionSalaries, ProfessionLinks,\
    SuggestedQuestions, Account, Post, PostLikes, PostComments, NotifyUser, Feedback

# Register your models here.

admin.site.register(Scope)
admin.site.register(Profession)
admin.site.register(Questions)
admin.site.register(SubScope)
admin.site.register(ProfessionSalaries)
admin.site.register(ProfessionLinks)
admin.site.register(SuggestedQuestions)
admin.site.register(Account)
admin.site.register(Post)
admin.site.register(PostLikes)
admin.site.register(PostComments)
admin.site.register(NotifyUser)
admin.site.register(Feedback)
