from django.contrib import admin
from interview.models import Scope, Profession, Questions, SubScope, ProfessionSalaries, ProfessionLinks

# Register your models here.

admin.site.register(Scope)
admin.site.register(Profession)
admin.site.register(Questions)
admin.site.register(SubScope)
admin.site.register(ProfessionSalaries)
admin.site.register(ProfessionLinks)
