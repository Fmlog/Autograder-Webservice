from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .serializers import UserSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt, datetime

# Create your views here.
 
class RegisterLectureViews(APIView):
    """ Send serialized registeration data for lecuter """
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['is_lecturer'] = True
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    
class RegisterStudentViews(APIView):
    """ Send serialized registeration data for lecuter """
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['is_student'] = True
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class RegisterAdminViews(APIView):
    """ Send serialized registeration data for lecuter """
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['is_superuser'] = True
        serializer.vaidated_data['is_staff'] = True
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class LoginViews(APIView):
    """ Webservice for the login process """
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('Invalid credentials')

        if not user.check_password(password):
            raise AuthenticationFailed('Invalid credentials')
        
        """ 'iat' means the date it was created """
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'lat': datetime.datetime.utcnow()
        }

        serializer = UserSerializers(user)
        token = jwt.encode(payload, 'SECRET_KEY', algorithm='HS256')
        response = Response()

        response.set_cookie('token', token, httponly=True)
        response.data = {
            "status" : "success",
            "data" : serializer.data,
            "message" : "Login Successful",
            "token" : token
        }

        return response

class UserViews(APIView):
    """ Webservice for the users """
    
    def get(self, request):
        """Get user"""
        token = request.COOKIES.get('token')
        if token is None:
            raise AuthenticationFailed('Invalid credentials')

        payload = jwt.decode(token, 'SECRET_KEY', algorithms='HS256')

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            return Response({
                "status": "error", 
                "data": [], 
                "message" : "User not found"
                }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializers(user)

        return Response({
            "status": "success",
            "data": serializer.data,
            "message": "user details"
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        """Delete user"""
        token = request.COOKIES.get('token')
        if token is None:
            raise AuthenticationFailed('Invalid credentials')

        payload = jwt.decode(token, 'SECRET_KEY', algorithms='HS256')

        item = get_object_or_404(User, id=payload['id'])
        item.soft_delete()
        return Response({
            "status": "success", 
            "data": [], 
            "message": "user deleted"
            })
    
class LogoutViews(APIView):
    """ Logout the user """
    def get(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            "status": "success",
            "message" : "Logout Successful"
        }
        return response