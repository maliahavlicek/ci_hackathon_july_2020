from accounts.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StatusInputSerializer
from .models import Status
from datetime import datetime
import pytz

utc = pytz.UTC


@api_view(['post'])
def send_status(request):
    """
    Create or update a User Status if input form is valid and user is in system
    """
    serializer = StatusInputSerializer(data=request.data)
    if serializer.is_valid():
        # need to make sure user is in system system
        user = User.objects.filter(id=serializer.data['user']).first()
        if user:
            # check if status exists or if this is first time user is reporting in
            if Status.objects.filter(id=serializer.data['user_id']).count() > 0:
                # updating
                user.status.mood = serializer.data['mood']
                user.status.plans = serializer.data['plans']
                user.status.help = serializer.data['help']
                user.status.updated_date = utc.localize(datetime.today())
                user.save()
            else:
                # creating
                status = Status.objects.create(
                    owner=user,
                    mood=serializer.data['mood'],
                    plans=serializer.data['plans'],
                    help=serializer.data['help'],
                )

        # send back ok status
        return Response(serializer.data)

    return Response(serializer.data)
