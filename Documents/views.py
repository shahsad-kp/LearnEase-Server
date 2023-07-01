from rest_framework.generics import CreateAPIView, ListAPIView

from Documents.models import Document
from Documents.serializer import DocumentSerializer


class DocumentCreateAPIView(CreateAPIView, ListAPIView):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def perform_create(self, serializer):
        classroom_id = self.kwargs.get('room_id')
        serializer.save(room_id=classroom_id)

    def get_queryset(self):
        classroom_id = self.kwargs.get('room_id')
        return Document.objects.filter(room_id=classroom_id)
