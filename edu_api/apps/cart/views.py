import logging

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django_redis import get_redis_connection
from course.models import Course, CourseExpire
from rest_framework.permissions import IsAuthenticated


#获取一个日志记录器
from edu_api.settings import constants

log = logging.getLogger("django")


class CartViewSet(ViewSet):

    #只有登录且认证成功的用户才可以访问此接口

    permission_classes = [IsAuthenticated]

    def add_cart(self, request):
        print(123)
        print(request)
        # 将用户提交的信息添加进购物车
        # request: 用户id,勾选状态,有效期,课程id

        course_id = request.data.get("course_id")
        user_id = request.user.id
        #是否勾选
        select = True
        #有效期
        expire = 0
        #校验前端获取的数据
        try:
            Course.objects.get(is_show=True,id=course_id)
        except Course.DoesNotExist:
            return Response({"message":"参数有误，数据不存在"},status=status.HTTP_400_BAD_REQUEST)
        try:
            #获取redis保连接对象
            redis_connection = get_redis_connection("cart")
            #将数据保存到redis
            pipeline = redis_connection.pipeline()
            #管道开启
            pipeline.multi()
            #商品的信息以及对应的有效期
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            #被勾选的商品
            pipeline.sadd("selected_%s" % user_id, course_id)
            # 执行
            pipeline.execute()
            #获取购物车中数据的数量
            cart_length = redis_connection.hlen("cart_%s" % user_id)
        except:
            log.error("购物车数据存储失败")
            return Response({"message":"参数有误，购物车添加失败"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message":"购物车商品添加成功","cart_length":cart_length})

    def list_cart(self,request):
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")
        cart_list_bytes = redis_connection.hgetall('cart_%s' % user_id)
        select_list_bytes = redis_connection.smembers("selected_%s" % user_id)
        #循环找出商品的信息
        data = []
        for course_id_byte,expire_id_byte in cart_list_bytes.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            try:
                course = Course.objects.get(is_show=True,is_delete=False,pk=course_id)
            except:
                continue

            #将购物车所需要的信息返回
            data.append({
                "selected": True if course_id_byte in select_list_bytes else False,
                "course_img":constants.IMAGE_SRC + course.course_img.url,
                "name":course.name,
                "id":course.id,
                # 购物车列表需要课程有效期
                "expire_list": course.expire_list,
                # 获取真实价格
                "real_price": course.real_expire_price(expire_id),
                #有效期id
                'expire_id':expire_id
            })

        return Response(data)

    def change_select(self,request):
        print(666)
        user_id = request.user.id
        selected = request.data.get("selected")
        course_id = request.data.get("course_id")
        print(123)

        try:
            Course.objects.get(is_show=True,is_delete=False,pk=course_id)

        except:
            return Response({"message":"参数有误，当前商品不存在"},status=status.HTTP_400_BAD_REQUEST)

        redis_connectonn = get_redis_connection("cart")
        if selected:
            #使状态变为勾选
            redis_connectonn.sadd("selected_%s" % user_id,course_id)
        else:
            #使状态变为不勾选
            redis_connectonn.srem("selected_%s" % user_id,course_id)

        return Response({"message":"切换状态成功"})

    def delete_cart(self,request,*args,**kwargs):

        # course_id = request.data.get("course_id")
        # print(course_id)
        course_id = kwargs.get('id')
        user_id = request.user.id
        try:
            Course.objects.get(is_show=True,id=course_id)
        except Course.DoesNotExist:
            return Response({"message":"参数有误，数据不存在"},status=status.HTTP_400_BAD_REQUEST)

        try:
            #获取redis保连接对象
            redis_connection = get_redis_connection("cart")
            #将数据保存到redis
            pipeline = redis_connection.pipeline()
            #管道开启
            pipeline.multi()
            #商品的信息以及对应的有效期
            pipeline.hdel("cart_%s" % user_id, course_id)
            # 执行
            pipeline.execute()
            #获取购物车中数据的数量
            cart_length = redis_connection.hlen("cart_%s" % user_id)
        except:
            return Response({"message":"参数有误，购物车删除失败"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message":"购物车商品删除成功","cart_length":cart_length})


    def change_expire(self, request):
        """改变redis中课程的有效期"""
        user_id = request.user.id
        expire_id = request.data.get("expire_id")
        course_id = request.data.get("course_id")
        print(course_id, expire_id,66666)

        try:
            course = Course.objects.get(is_show=True, is_delete=False, id=course_id)
            # 如果前端传递来的有效期选项  如果不是0  则修改课程对应的有效期
            if expire_id > 0:
                expire_iem = CourseExpire.objects.filter(is_show=True, is_delete=False, id=expire_id)
                if not expire_iem:
                    raise Course.DoesNotExist()
        except Course.DoesNotExist:
            return Response({"message": "课程信息不存在"}, status=status.HTTP_400_BAD_REQUEST)

        connection = get_redis_connection("cart")
        connection.hset("cart_%s" % user_id, course_id, expire_id)

        # 重新计算切换有效期后的价钱
        real_price = course.real_expire_price(expire_id)

        return Response({"message": "切换有效期成功", "real_price": real_price})



    def get_select_course(self, request):
        """
        获取购物车中已勾选的商品  返回前端所需的数据
        """

        user_id = request.user.id
        redis_connection = get_redis_connection("cart")

        # 获取当前登录用户的购车中所有的商品
        cart_list = redis_connection.hgetall("cart_%s" % user_id)
        select_list = redis_connection.smembers("selected_%s" % user_id)

        total_price = 0  # 商品总价
        data = []

        for course_id_byte, expire_id_byte in cart_list.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            print(course_id, expire_id)

            # 判断商品id是否在已勾选的的列表中
            if course_id_byte in select_list:
                try:
                    # 获取到的所有的课程信息
                    course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                except Course.DoesNotExist:
                    continue
                # 如果有效期的id大于0  则需要计算商品的价格  id不大于0则代表永久有效 需要默认值
                original_price = course.price
                expire_text = "永久有效"

                try:
                    if expire_id > 0:
                        course_expire = CourseExpire.objects.get(id=expire_id)
                        # 对应有效期的价格
                        original_price = course_expire.price
                        expire_text = course_expire.expire_text
                except CourseExpire.DoesNotExist:
                    pass

                # 根据已勾选的商品的对应有效期的价格去计算勾选商品的最终价格
                real_expire_price = course.real_expire_price(expire_id)

                # 将购物车所需的信息返回
                data.append({
                    "course_img": constants.IMAGE_SRC + course.course_img.url,
                    "name": course.name,
                    "id": course.id,
                    "expire_text": expire_text,
                    # 活动、有效期计算完成后的  真实价格
                    "real_price": "%.2f" % float(real_expire_price),
                    # 原价
                    "price": original_price,
                    "discount_name": course.discount_name,
                })

                # 商品叠加后的总价
                total_price += float(real_expire_price)

        return Response({"course_list": data, "total_price": total_price, "message": '获取成功'})