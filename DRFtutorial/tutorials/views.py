import logging
from .models import Tutorial, Teacher, Skill
from django.http import Http404
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from .serializers import TutorialSerializer, TeacherSerializer, TeacherPublicSerializer, SkillSerializer


logger = logging.getLogger(__name__)


class TutorialListView(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Tutorial.objects.all().order_by("id")
    serializer_class = TutorialSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == "GET" or self.request.method == "POST":
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        logger.info("Listing current tutorial list...")
        response = super().list(request)
        logger.info("Listed successfully.")
        return response

    def create(self, request, *args, **kwargs):
        if "teacher" not in request.data:
            request.data.pop("teacher", None)
        logger.info("Adding new tutorial to the list...")
        response = super().create(request)
        logger.info("Added successfully.")
        return response

    def delete_all(self, request, *args, **kwargs):
        logger.info("Deleting tutorial list...")
        self.queryset.delete()
        logger.info("Deleted successfully.")
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeacherListView(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Teacher.objects.all().order_by("id")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return TeacherSerializer
        else:
            return TeacherPublicSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            if not self.request.user.is_authenticated:
                return []
        elif self.request.method == "DELETE":
            return [IsAdminUser()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        logger.info("Listing current teacher list...")
        response = super().list(request)
        logger.info("Listed successfully.")
        return response

    def create(self, request, *args, **kwargs):
        if "skills" not in request.data:
            request.data.pop("skills", None)
        logger.info("Adding new teacher to the list...")
        response = super().create(request)
        logger.info("Added successfully.")
        return response

    def get_object(self):
        return self.queryset.first()

    def delete_all(self, request, *args, **kwargs):
        logger.info("Deleting teacher list...")
        self.queryset.delete()
        logger.info("Deleted successfully.")
        return Response(status=status.HTTP_204_NO_CONTENT)


class SkillListView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Skill.objects.all().order_by("id")
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        logger.info("Listing current skill list...")
        response = super().list(request)
        logger.info("Listed successfully.")
        return response

    def create(self, request, *args, **kwargs):
        logger.info("Adding new skill to the list...")
        response = super().create(request)
        logger.info("Added successfully.")
        return response

    def delete_all(self, request, *args, **kwargs):
        logger.info("Deleting all skill items...")
        self.queryset.delete()
        logger.info("All skill items deleted successfully.")
        return Response(status=status.HTTP_204_NO_CONTENT)


class TutorialDetailView(
    generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    queryset = Tutorial.objects.all().order_by("id")
    serializer_class = TutorialSerializer
    # default to pk
    # lookup_field for other things
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            logger.info("Listing requested tutorial item...")
            response = self.retrieve(request)
            logger.info("Listed successfully.")
            return response

    def put(self, request, *args, **kwargs):
        logger.info("Replacing requested tutorial item...")
        title = request.data.get("title")
        description = request.data.get("description")
        published = request.data.get("published")
        teacher = request.data.get("teacher")
        if not title or not description or not published or not teacher:
            return Response(
                "Title, description, published, and teacher entries are required.", status=status.HTTP_400_BAD_REQUEST
            )
        response = self.update(request)
        logger.info("Replaced successfully.")
        return response

    def patch(self, request, *args, **kwargs):
        logger.info("Modifying requested tutorial item...")
        response = self.partial_update(request)
        logger.info("Modified successfully.")
        return response

    def delete(self, request, id=None):
        if id:
            logger.info("Deleting requested tutorial item...")
            response = self.destroy(request)
            logger.info("Deleted successfully.")
            return response


class TeacherDetailView(
    generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    queryset = Teacher.objects.all().order_by("id")
    serializer_class = TeacherSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            logger.info("Listing requested teacher entry...")
            response = self.retrieve(request)
            logger.info("Listed successfully.")
            return response

    def put(self, request, *args, **kwargs):
        logger.info("Replacing requested teacher entry...")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        skills = request.data.get("skills")
        if not first_name or not last_name or not skills:
            return Response(
                "First name, last name, and skill entries are required.", status=status.HTTP_400_BAD_REQUEST
            )
        response = self.update(request)
        logger.info("Replaced successfully.")
        return response

    def patch(self, request, *args, **kwargs):
        logger.info("Modifying requested teacher entry...")
        response = self.partial_update(request)
        logger.info("Modified successfully.")
        return response

    def delete(self, request, id=None):
        if id:
            logger.info("Deleting requested teacher entry...")
            response = self.destroy(request)
            logger.info("Deleted successfully.")
            return response


class SkillDetailView(
    generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    queryset = Skill.objects.all().order_by("id")
    serializer_class = SkillSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            logger.info("Listing requested skill item...")
            response = self.retrieve(request)
            logger.info("Listed successfully.")
            return response

    def put(self, request, *args, **kwargs):
        logger.info("Replacing requested skill item...")
        name = request.data.get("name")
        level = request.data.get("level")
        if not name or not level:
            return Response("Name and level entries are required.", status=status.HTTP_400_BAD_REQUEST)
        response = self.update(request)
        logger.info("Replaced successfully.")
        return response

    def patch(self, request, *args, **kwargs):
        logger.info("Modifying requested skill item...")
        response = self.partial_update(request)
        logger.info("Modified successfully.")
        return response

    def delete(self, request, id=None):
        if id:
            logger.info("Deleting requested skill item...")
            response = self.destroy(request)
            logger.info("Deleted successfully.")
            return response


class TutorialListPublishedView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Tutorial.objects.filter(published=True).order_by("id")
    serializer_class = TutorialSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info("Listing published tutorial list...")
        response = self.list(request)
        logger.info("Listed successfully.")
        return response


"""

# 1 FUNCTION-BASED VIEWS: represent a simple and straightforward approach for handling HTTP requests and returning
#   HTTP responses; implemented as Python functions.

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

@api_view(['GET'])
def tutorial_list_published(request):
    # GET all published tutorials
    tutorials = Tutorial.objects.filter(published=True)
    if request.method == 'GET':
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)



# 2 CLASS-BASED VIEW (extending base views from django): defines views by using classes instead of functions; one of
#   the most commonly used base views in Django is the View class, which is a generic base view that provides the basic
#   structure for handling HTTP requests. 

class TutorialListView(View):
    def get(self, request):
        tutorials = Tutorial.objects.all()
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)


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



# 3 CLASS-BASED VIEWS (using GENERICS from rest_framework): a set of pre-built generic view classes provided by Django;
#   provide a higher level of abstraction.

class TutorialListViewGenerics(generics.ListCreateAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer


class TutorialDetailViewGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer


class TutorialListPublishedViewGenerics(generics.ListCreateAPIView):
    queryset = Tutorial.objects.filter(published=True)
    serializer_class = TutorialSerializer



# 4 VIEWSETS: a convenient way to combine common CRUD (Create, Retrieve, Update, Delete) operations into a single
#   class; often used in conjunction with routers to generate URL patterns for the corresponding views automatically.
#   MIXINS: small, reusable classes that can be mixed into other classes to add specific behaviors or attributes.

class TutorialListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer

    def list(self, request):
        return self.list(request)

    def create(self, request):
        return self.create(request)

    def destroy(self, request):
        return self.destroy(request)
"""
