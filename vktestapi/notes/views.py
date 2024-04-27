from rest_framework.viewsets import ModelViewSet
from .models import Note    
from .serializers import NoteSerializer, AuthenticatedNoteSerializer
from django.http import QueryDict
from .permissions import AuthenticatedPermission
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.pagination import LimitOffsetPagination
import datetime
from pytz import timezone as tz
from django_filters import rest_framework as filters


#Fitlering class
class SimpleFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="time_created", lookup_expr = "gte")
    end_date = filters.DateFilter(field_name="time_created", lookup_expr = "lte")
    


    class Meta:
        model = Note
        fields = ['time_created', 'user']


#Pagination class
class SimplePagination(LimitOffsetPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10000
    offset_query_param = 10


#Main view for notes app
class NotesView(ModelViewSet):
    queryset = Note.objects.all()
    permission_classes = (AuthenticatedPermission, )
    serializer_class = NoteSerializer
    pagination_class = SimplePagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SimpleFilter
    ordering_fields = ['time_created']
    ordering = ['time_created']


    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return AuthenticatedNoteSerializer
        return NoteSerializer

    def get_user_from_request(self, request):
        #Add user to validated_data
        req_dict = request.data.dict()
        req_dict["user"] = request.user.id
        data_from_request = QueryDict('', mutable=True)
        data_from_request.update(req_dict)

        return data_from_request

    def create(self, request, *args, **kwargs):
        
        data_from_request = self.get_user_from_request(request)

        serializer = self.get_serializer(data=data_from_request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance: Note = self.get_object()
        
        data_from_request = self.get_user_from_request(request)

        serializer = self.get_serializer(instance, data=data_from_request, partial=partial)
        serializer.is_valid(raise_exception=True)



        if (datetime.datetime.now().replace(tzinfo=tz("Europe/Moscow")) - instance.time_created).days < 1:
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response({"time_created":"Запрещено редактирование заметки сроком размещения более 1 дня"}, status=status.HTTP_400_BAD_REQUEST)