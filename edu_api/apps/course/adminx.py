import xadmin
from course.models import Course, CourseCategory, CourseLesson, CourseChapter, Teacher


class CourseCategoryModelAdmin(object):
    """课程分类表"""
    pass

xadmin.site.register(CourseCategory, CourseCategoryModelAdmin)


class CourseModelAdmin(object):
    """课程信息表"""
    pass

xadmin.site.register(Course, CourseModelAdmin)


class CourseChapterModelAdmin(object):
    """课程章节表"""
    pass

xadmin.site.register(CourseChapter, CourseChapterModelAdmin)


class CourseLessonModelAdmin(object):
    """课程课时表"""
    pass

xadmin.site.register(CourseLesson, CourseLessonModelAdmin)


class TeacherLessonModelAdmin(object):
    """讲师表"""
    pass

xadmin.site.register(Teacher, TeacherLessonModelAdmin)
