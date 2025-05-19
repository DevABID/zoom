from django.contrib import admin
from .models import RoomMember

@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'uid', 'room_name', 'joined_at', 'left_at', 'duration_minutes')

    def duration_minutes(self, obj):
        return obj.duration_minutes()
    duration_minutes.short_description = 'Duration (minutes)'
