from django.shortcuts import render
from rest_framework import viewsets
from .models import Server
from .serializers import ServerSerializer
from rest_framework .response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count
from .schema import server_list_docs



class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        # Return a list of servers filtering by parameters
        # WARNING: Comments said filter/filters backend is standard rather than conditions
        # https://www.django-rest-framework.org/api-guide/filtering/
        category = request.query_params.get('category')
        qty = request.query_params.get('qty')
        by_user = request.query_params.get('by_user') == 'true'
        by_serverid = request.query_params.get('by_serverid')
        with_num_members = request.query_params.get('with_num_members') == 'true'

        if category:
            # filter by category name
            self.queryset = self.queryset.filter(category__name=category)
        if by_user:
            # filter by servers the user is associated to
            if request.user.is_authenticated:
                userId = request.user.id
                self.queryset = self.queryset.filter(member=userId)
            else:
                raise AuthenticationFailed()
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count('member'))
        if by_serverid:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(detail=f'Server id {by_serverid} does not exist')
            except ValueError:
                raise ValidationError(detail='Server value error')
        if qty:
            # also filter by amount (ex: first 4 servers), appends to the end of query
            self.queryset = self.queryset[: int(qty)]

        serializer = ServerSerializer(self.queryset, many=True, context={'num_members':with_num_members})
        return Response(serializer.data)

# 16/45
