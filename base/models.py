from django.db import models

# Create your models here.


class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)
    room_name = models.CharField(max_length=200)

    joined_at = models.DateTimeField(null=True, blank=True)
    left_at = models.DateTimeField(null=True, blank=True)

    def duration_minutes(self):
        if self.left_at and self.joined_at:
            return int((self.left_at - self.joined_at).total_seconds() / 60)
        return None

    def __str__(self):
        return self.name
