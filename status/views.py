from accounts.models import Family
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StatusInputSerializer
from rest_framework.exceptions import Throttled
from .models import Status
from users.models import User
from datetime import datetime
import pytz

utc = pytz.UTC


class SendStatus(APIView):
    lookup_url_kwarg = "query"
    throttle_scope = "send_status"

    def post(self, request, **kwargs):
        """
        Create or update a User Status if input form is valid and user is in system
        """
        serializer = StatusInputSerializer(data=request.data)
        if serializer.is_valid():
            # need to make sure user is in system system
            user = User.objects.filter(id=serializer.data['user_id']).first()
            if user:
                # check if family exists
                family = Family.objects.get(pk=serializer.data['family_id'])
                if family:
                    members = family.get_members()
                    # check if family exists
                    if user not in members:
                        return Response({'inputs': serializer.data, 'errors': serializer.errors}, 200)
                else:
                    return Response({'inputs': serializer.data, 'errors': serializer.errors}, 200)

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
                return Response(serializer.data, 200)

            else:
                return Response({'inputs': serializer.data, 'errors': serializer.errors}, 200)

        return Response(serializer.data)

    def throttled(self, request, wait):
        raise Throttled(detail={"message": "rate limit exceeded"})
