import xadmin
from order.models import Order,OrderDetail

class OrderModelAdmin(object):
    """订单模型管理类"""
    pass


xadmin.site.register(Order, OrderModelAdmin)

class OrderDetailModelAdmin(object):
    """订单详情模型管理类"""
    pass


xadmin.site.register(OrderDetail, OrderDetailModelAdmin)