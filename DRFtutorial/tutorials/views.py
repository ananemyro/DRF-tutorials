from .models import Tutorial
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .serializers import TutorialSerializer


# 1 : Function-based view
@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    # GET list of new tutorials, POST new tutorial, DELETE all tutorials
    if request.method == 'GET':
        tutorials = Tutorial.objects.all()
        title = request.GET.get('title', None)
        # filter by title
        if title is not None:
            tutorials = tutorials.filter(title_icontains=title)

        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)  # safe=False for objects serialization
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        count = Tutorial.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


# 1.1 : Class-based view extending views from django
from django.views import View


class TutorialListView(View):
    def get(self, request):
        tutorials = Tutorial.objects.all()
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)


# 1.2 : Class-based views using GENERICS, MIXINS from rest_framework
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated


class TutorialListViewGenericsMixins(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    # permission_classes = (IsAuthenticated,)
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def delete(self, request):
        return self.delete(request)


# viewset
from rest_framework import viewsets


class TutorialViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer

    def list(self, request):
        return self.list(request)

    def create(self, request):
        return self.create(request)

    def destroy(self, request):
        return self.destroy(request)


# 1.3 : Class-based views using GENERICS from rest_framework
class TutorialListViewGenerics(generics.ListCreateAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer


# 2 : Function-based view
@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    # find tutorial by pk (id)
    try:
        tutorial = Tutorial.objects.get(pk=pk)
    except Tutorial.DoesNotExist:
        return JsonResponse({'message': 'The tutorial does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        tutorial_serializer = TutorialSerializer(tutorial)
        return JsonResponse(tutorial_serializer.data)
    elif request.method == 'PUT':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        tutorial.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# 2.1 : Generics + mixins
class TutorialDetailViewGenericsMixins(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin):
    # permission_classes = (IsAuthenticated,)
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    # default to pk
    # lookup_field for other things
    lookup_field = "id"

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)

    def put(self, request, *args, **kwargs):
        return self.update(request)

    def delete(self, request, id=None):
        if id:
            return self.destroy(request)


# 2.2 : Class-based views using GENERICS from rest_framework
class TutorialDetailViewGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer


# (1st tutorial, class-based views from django)
from rest_framework.views import APIView
from django.http import Http404


class DetailsOfTutorial(APIView):

    def get_object(self, pk):
        try:
            return Tutorial.objects.get(pk=pk)
        except Tutorial.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tutorial = self.get_object(pk)
        tutorial_serializer = TutorialSerializer(tutorial)
        return JsonResponse(tutorial_serializer.data)

    def put(self, request, pk, format=None):
        tutorial = self.get_object(pk)
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        tutorial = self.get_object(pk)
        tutorial.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# 3 : Function-based view
@api_view(['GET'])
def tutorial_list_published(request):
    # GET all published tutorials
    tutorials = Tutorial.objects.filter(published=True)
    if request.method == 'GET':
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)


# 3.1 : Generics + mixins
class TutorialListPublishedViewGenericsMixins(generics.GenericAPIView, mixins.ListModelMixin):
    # permission_classes = (IsAuthenticated,)
    queryset = Tutorial.objects.filter(published=True)
    serializer_class = TutorialSerializer

    def get(self, request):
        return self.list(request)


# 3.2 : Class-based views using GENERICS from rest_framework
class TutorialListPublishedViewGenerics(generics.ListCreateAPIView):
    queryset = Tutorial.objects.filter(published=True)
    serializer_class = TutorialSerializer
