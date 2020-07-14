from django.urls import path

from course import views

urlpatterns = [
    path("category/", views.CourseCategoryListAPIView.as_view()),
    path("list/", views.CourseListAPIView.as_view()),
    path("list_filter/", views.CourseFilterListAPIView.as_view()),
    path("list_infor/<str:id>", views.CourseinforRetrieveAPIView.as_view()),
    path("list_chapter/", views.CourseChapterAPIView.as_view()),

]