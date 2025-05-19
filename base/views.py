
from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
import  random
from django.http import  JsonResponse
import time
import json
from django.utils import timezone
from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


#Build token with uid
def getToken(request):
    appId = 'b96848109f5248298f5138ea90fed0cb'
    appCertificate = '69d86112b52d45e4b87270398e57e865'
    channelName = request.GET.get('channel')
    uid = random.randint(1,250)
    expirationTimeInSeconds = 3600 * 24 * 7
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid}, safe=False)
def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')





@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name'],
        defaults={

            'joined_at': timezone.now()
        }
    )
    # If the member exists but joined_at is not set (edge case)
    if not member.joined_at:
        member.joined_at = timezone.now()
        member.save()

    return JsonResponse({'name':data['name']}, safe=False)

def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )

    name = member.name
    return JsonResponse({'name':member.name}, safe=False)





from django.utils import timezone

@csrf_exempt
def recordLeaveTime(request):
    data = json.loads(request.body)
    try:
        member = RoomMember.objects.get(
            name=data['name'],
            uid=data['UID'],
            room_name=data['room_name']
        )
        member.left_at = timezone.now()
        member.save()
        return JsonResponse({
            'message': 'Left time recorded',
            'joined_at': member.joined_at,
            'left_at': member.left_at,
            'duration': member.duration_minutes()
        })
    except RoomMember.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)
