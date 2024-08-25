from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Todo, User
from .serializers import TodoSerializer
from rest_framework import status

class Todos(APIView):

  def get_user(self, user_id):
    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      raise NotFound("유저를 찾을 수 없습니다.")
    return user

  def get(self, request, user_id):
    # month와 day 쿼리 파라미터로 받아서 필터링
    now = timezone.localtime(timezone.now())
    current_month = now.month
    current_day = now.day
    
		# 쿼리 파라미터에 "month"값이 없으면, 디폴트 값으로 current_month 가져옴
    month = request.query_params.get("month", current_month)
    month = int(month)

    day = request.query_params.get("day", current_day)
    day = int(day)

    user = self.get_user(user_id)
    todos = Todo.objects.filter(
      date__month=month,
      date__day=day,
      user=user
    )
    serializer = TodoSerializer(
      todos,
      many=True
    )
    return Response(serializer.data)

  def post(self, request, user_id):
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
      user = self.get_user(user_id)
      serializer.save(
        user=user
      )
      return Response(serializer.data)
    else:
      return Response(serializer.errors)
class CheckTodo(APIView):

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        return user

    def get_todo(self, user_id, todo_id):
        try:
            todo = Todo.objects.get(id=todo_id, user=user_id)
        except Todo.DoesNotExist:
            raise NotFound("할 일을 찾을 수 없습니다.")
        return todo

    def patch(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user_id, todo_id)

        # 요청 본문에서 `is_checked` 값을 받아서 업데이트합니다.
        is_checked = request.data.get("is_checked")
        if is_checked is None:
            return Response({"error": "is_checked 필드가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        todo.is_checked = is_checked
        todo.save()

        serializer = TodoSerializer(todo)
        return Response(serializer.data)

class ReviewTodo(APIView):

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        return user

    def get_todo(self, user, todo_id):
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("할 일을 찾을 수 없습니다.")
        return todo

    def patch(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user, todo_id)

        # 요청 본문에서 리뷰 내용을 받아서 업데이트합니다.
        review = request.data.get("review")
        if review is None:
            return Response({"error": "review 필드가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 리뷰 내용을 업데이트하고 저장합니다.
        todo.review = review
        todo.save()

        return Response({"message": "리뷰가 성공적으로 업데이트되었습니다."}, status=status.HTTP_200_OK)
