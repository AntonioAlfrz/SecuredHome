import subprocess

from datetime import datetime
from rest_framework import permissions
from rest_framework import viewsets

#import raspi_setup
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

import azure_setup
from django.http import HttpResponse

import fcm_server
from api.models import User, Log
from api.permissions import ReadOnly
from api.serializers import UserSerializer, LogSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Must be iterable
    permission_classes = (permissions.IsAuthenticated,permissions.IsAdminUser)

class LogViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = (permissions.IsAuthenticated,ReadOnly)

# /test/test
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def test(request):
    print "\nPresence detected. Uploading image"
    #subprocess.check_call(["fswebcam", "--no-banner", "imagen.jpg"])
    date = str(datetime.now())
    azure_setup.upload(date, "rutina2.jpg")
    #subprocess.check_call(["rm", "imagen.jpg"])
    print "\nSending Presence notification"
    fcm_server.send_notification(fcm_server.token, "SecuredHome.Presence detected!", azure_setup.base_url + date)
    return Response({
        "title": "Response",
        "message": "Test notification"
    })

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def index(request):
    content = {
        "title": "Response",
        'message': "API direction"
    }
    return Response(content)

# /test/photo
@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def take_photo(request):
    content = {
        "title": "Response",
        'message': "Photo taken"
    }
    return Response(content)

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def list(request):
    return Response(azure_setup.list_blobs())


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def token(request):
    response = {}
    for user in User.objects.all():
        response[user]=Token.objects.get_or_create(user=user)

    return Response(response)

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def refresh():
    for user in User.objects.all():
        new_token = Token.objects.get(user=User.objects.get(id=1)).generate_key()
        print "New token. Usuario: "+user+" Token: "+new_token
        Token.objects.filter(user=user).update(key=new_token)
        fcm_server.send_data(fcm_server.token, new_token)

'''
# More concise form
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

@api_view(['GET'])
def api_root(request, format=None):
    print "Entrypoint"
    return Response({
        'users': reverse('users', request=request, format=format)
    })

# Mixin: Class developed to be inherited by another, not to work by itself
# Reusable code, mixin could be reused in other APIs
# Core function (GenericApiView) + Mixins
class UserList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# Class based views
class UserList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, name):
        try:
            return User.objects.get(name=name)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, name, format=None):
        user = self.get_object(name)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Wrapper with better features and handles wrong verbs
# and formats explicitly given in the URLs
@api_view(['GET', 'POST'])
def user_list(request, format = None):
    # List all code snippets, or create a new snippet.
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        # Response Rest Framework. It handles the content type
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, name, format=None):
    # Retrieve, update or delete a code snippet.
    try:
        user = User.objects.get(name=name)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''
