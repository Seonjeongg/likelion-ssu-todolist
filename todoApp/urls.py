from django.urls import path
from . import views

urlpatterns = [
    path("<int:user_id>", views.Todos.as_view()),
    path("<int:user_id>/<int:todo_id>/check", views.CheckTodo.as_view(), name='check_todo'),
    path("<int:user_id>/<int:todo_id>/reviews", views.ReviewTodo.as_view(), name='review_todo'),
]
