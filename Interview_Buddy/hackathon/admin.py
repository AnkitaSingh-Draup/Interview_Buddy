from django.contrib import admin
from .models import *
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Job, AuthorAdmin)
admin.site.register(Question, AuthorAdmin)
admin.site.register(Level, AuthorAdmin)
admin.site.register(Transcript, AuthorAdmin)
admin.site.register(Interviewer, AuthorAdmin)
admin.site.register(Rating, AuthorAdmin)
admin.site.register(Candidate, AuthorAdmin)
admin.site.register(QuestionLevelRating, AuthorAdmin)
admin.site.register(Interview, AuthorAdmin)





