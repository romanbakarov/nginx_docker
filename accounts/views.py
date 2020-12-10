from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import Account
from accounts.serializers import AccountSerializer, AccountActivitySerializer


class AccountCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountActivity(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        serializer = AccountActivitySerializer
        user = get_object_or_404(Account, pk=pk)
        data = serializer(user).data
        return Response(data)
