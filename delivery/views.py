from django.utils.dateparse import parse_datetime
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view

from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from datetime import timedelta


class createUsersViewSet(APIView):

    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"statusCode": "200", "body": "created"})
        error_string = str(serializer.errors)
        return Response({"statusCode": "400", "body": error_string}, status=status.HTTP_400_BAD_REQUEST)

class loginUsersViewSet(APIView):
    def post(self, request):
        mail = request.data.get('TCEMAIL')
        password = request.data.get('TCPASSWORD')
        data = Users.objects.filter(TCEMAIL=mail).first()
        if data:
            if data.TCPASSWORD == password:
                serializer = UsersSerializer(data)
                return Response({"statusCode": "200", "body": serializer.data})
            return Response({"statusCode": "400", "body": "Нууц үг буруу байна"})
        return Response({"statusCode": "400", "body": "Хэрэглэгч бүртгэгдээгүй байна"})

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        # Get user by username
        user = Users.objects.get(TCUSERNAME=username)
        # Check password
        if check_password(password, user.TCPASSWORD):
            # Serialize user data
            user_data = {
                'id': user.id,
                'username': user.TCUSERNAME,
                'email': user.TCEMAIL,
                'gender': user.TCGENDER,
            }
            return Response({'message': 'Login successful', 'user': user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
    except Users.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# Get Product Information
@api_view(['GET'])
def get_product_info(request):
    products = InfoProduct.objects.all()
    serializer = InfoProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class InfoProductSearchView(generics.ListAPIView):
    serializer_class = InfoProductSerializer

    def get_queryset(self):
        queryset = InfoProduct.objects.all()
        item_code = self.request.query_params.get('itemCode', None)
        item_name = self.request.query_params.get('itemName', None)

        if item_code is not None:
            queryset = queryset.filter(itemCode=item_code)

        if item_name is not None:
            queryset = queryset.filter(itemName__icontains=item_name)

        return queryset


# Get InfoSector Information
@api_view(['GET'])
def get_info_sector_info(request):
    sectors = InfoSector.objects.all()
    serializer = InfoSectorSerializer(sectors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Create or Retrieve History
class HistoryView(APIView):
    def get(self, request):
        # Optionally filter by date range
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date and end_date:
            try:
                start_date = parse_datetime(start_date)
                end_date = parse_datetime(end_date)
                end_date = end_date + timedelta(days=1)
                histories = History.objects.filter(createdDate__range=[start_date, end_date])
            except ValueError:
                return Response({'message': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            histories = History.objects.all()

        serializer = HistorySerializer(histories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = HistoryAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'ok', 'body':serializer.data} , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def filter_history(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')

        # Filter History based on related InfoProduct fields
        histories = History.objects.all()

        if pk:
            histories = histories.filter(historyproduct__history__pk=pk).distinct()

        serializer = HistorySerializer(histories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        return Response({'message': 'POST method is not implemented for filtering'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)