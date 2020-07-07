from accounts.models import Family
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StatusInputSerializer
from accounts.serializers import FamilySerializer
from rest_framework.exceptions import Throttled
from .models import Status
from users.models import User
from datetime import datetime
import pytz

utc = pytz.UTC


class SendStatus(APIView):
    """
    Create or update a User Status
    """
    lookup_url_kwarg = "query"
    throttle_scope = "send_status"

    def post(self, request, **kwargs):
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
                status, created = Status.objects.update_or_create(
                    owner=user,
                    defaults={
                        "owner": user,
                        "mood": serializer.data['mood'],
                        "plans": serializer.data['plans'],
                        "help": serializer.data['help'],
                        "updated_date": utc.localize(datetime.today())
                    }
                )

                # send back ok status
                return Response(serializer.data, 200)

            else:
                return Response({'inputs': serializer.data, 'errors': serializer.errors}, 200)

        return Response(serializer.data)

    def throttled(self, request, wait):
        raise Throttled(detail={"message": "rate limit exceeded"})


class GetAllStatus(APIView):
    """
    Get Status based on user and Family
    """
    lookup_url_kwarg = "query"
    throttle_scope = "get_status"

    def post(self, request, **kwargs):
        """
        Send All User Status For A Family
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
                    # check if user is in members and is allowed to see statuses
                    if user in members:
                        result_serializer = FamilySerializer(instance=family)
                        return Response(result_serializer.data)

        return Response({'inputs': serializer.data, 'errors': serializer.errors}, 200)

    def throttled(self, request, wait):
        raise Throttled(detail={"message": "rate limit exceeded"})
