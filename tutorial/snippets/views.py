# from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Snippet, User
from .permissions import IsAllowedToWrite, IsAllowedToRead
from .serializers import SnippetSerializer, UserSerializer, RegistrationSerializer


@api_view(['GET', 'POST'])
def registration_view(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = RegistrationSerializer(user, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            password2 = serializer.validated_data['password2']
            try:
                email = serializer.validated_data['email']
            except:
                email = ""
            try:
                address = serializer.validated_data['address']
            except:
                address = ""
            try:
                phone_number = serializer.validated_data['phone_number']
            except:
                phone_number = ""

            if password == password2:
                user = User(
                    user_type=serializer.validated_data['user_type'],
                    email=email,
                    username=serializer.validated_data['username'],
                    address=address,
                    phone_number=phone_number

                )
                user.set_password(password)
                user.save()
            else:
                return Response("Confirm your password and try again")
        else:
            return Response(serializer.errors)

        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_root(request):
    return Response({
        'users': reverse('user-list', request=request),
        'snippets': reverse('snippet-list', request=request)
    })


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticated, IsAllowedToRead, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticated, IsAllowedToRead,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
