from rest_framework import generics, permissions, status
from rest_framework.response import Response

from users.models import User
from users.serializers import UserActivitySerailizer


class ViewActivity(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserActivitySerailizer

    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    def get(self, request):
        serializer = self.serializer_class(instance=self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
