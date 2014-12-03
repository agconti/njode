from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


class NodeServer(APIView):
    """
    Processes all requests to node server. Requires authentication.
    """
    authentication_classes = (authentication.TokenAuthentication,
                              authentication.SessionAuthentication)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        """
        Redirects to node server if authenticated.
        """
        return redirect('http://localhost:3000/')