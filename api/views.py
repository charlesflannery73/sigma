from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from web.models import Type, Signature
from .serializers import TypeSerializer, SigSerializer, SigDetailSerializer


class TypeViewSet(viewsets.ModelViewSet):
    """
    list:
    filter parameters: name, name_like, id, comment

    create:
    add create help here

    read:
    add read help here

    update:
    add update help here

    partial_update:
    add partial update help here

    delete:
    add delete help here
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    def get_queryset(self):

        queryset = Type.objects.all()

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        name_like = self.request.query_params.get('name_like', None)
        if name_like is not None:
            queryset = queryset.filter(name__contains=name_like)

        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)

        comment = self.request.query_params.get('comment', None)
        if comment is not None:
            queryset = queryset.filter(comment__contains=comment)

        return queryset

class SigViewSet(viewsets.ModelViewSet):
    """
    list:
    filter parameters: text, text_like, id, type_id, type, type_like, expiry, reference, comment

    create:
    add create help here

    read:
    add read help here

    update:
    add update help here

    partial_update:
    add partial update help here

    delete:
    add delete help here
    """

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Signature.objects.all()
    serializer_class = SigSerializer
    detail_serializer_class = SigDetailSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):

        queryset = Signature.objects.all()

        text = self.request.query_params.get('text', None)
        if text is not None:
            queryset = queryset.filter(text=text)

        text_like = self.request.query_params.get('text_like', None)
        if text_like is not None:
            queryset = queryset.filter(text__contains=text_like)

        type_like = self.request.query_params.get('type_like', None)
        if type_like is not None:
            queryset = queryset.filter(type__name__contains=type_like)

        type = self.request.query_params.get('type', None)
        if type is not None:
            queryset = queryset.filter(type__name=type)

        type_id = self.request.query_params.get('type_id', None)
        if type_id is not None:
            queryset = queryset.filter(type_id=type_id)

        expiry = self.request.query_params.get('expiry', None)
        if expiry is not None:
            queryset = queryset.filter(expiry=expiry)

        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)

        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)

        reference = self.request.query_params.get('reference', None)
        if reference is not None:
            queryset = queryset.filter(reference=reference)

        comment = self.request.query_params.get('comment', None)
        if comment is not None:
            queryset = queryset.filter(comment__contains=comment)

        return queryset
