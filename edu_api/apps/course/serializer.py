from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Course, Teacher, CourseLesson, CourseChapter


class CourseCategorySerializer(ModelSerializer):
    """课程分类"""

    class Meta:
        model = CourseCategory
        fields = ["id", "name"]


class CourseTeacherSerializer(ModelSerializer):
    """课程所属老师的序列化器"""

    class Meta:
        model = Teacher
        fields = ("id",
                  "name",
                  "role",  #讲师身份
                  "title",   #职称
                  "signature",  #导师签名
                  "brief",  #讲师描述
                  "image",
                  )


class CourseModelSerializer(ModelSerializer):
    """课程列表"""

    # 序列化器嵌套查询老师信息
    teacher = CourseTeacherSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons",
                  "price", "teacher","lesson_list","period","level_name","course_video",'brief_html',
                  "discount_name", "real_price","active_time"]
        # "chapter_list",


class CourseLessonSerializer(ModelSerializer):

    class Meta:
        model = CourseLesson
        fields = ['id',
                  'name',
                  'free_trail',
                  "duration"  #视频时长
                  ]


class CourseChapterSerializer(ModelSerializer):

    coursesections = CourseLessonSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ['id','chapter','name','coursesections']

