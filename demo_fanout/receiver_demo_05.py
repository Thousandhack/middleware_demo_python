#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 定义交换机
# 随机生成一个临时队列，并绑定到交换机上,从而接收端从临时队列获取消息
import pika
import sys

hostname = 'localhost'
parameters = pika.ConnectionParameters(hostname)
connection = pika.BlockingConnection(parameters)

# 创建通道
channel = connection.channel()

# 定义交换机，设置类型为topic
channel.exchange_declare(exchange='change_fan', exchange_type='fanout')

# queue_declare的参数exclusive=True表示当接收端退出时，销毁临时产生的队列，这样就不会占用资源。
result = channel.queue_declare(queue='demo_06',exclusive=True)
# 随机生成队列，并绑定到交换机上
queue_name = result.method.queue
channel.queue_bind(exchange='change_fan', queue=queue_name)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))


channel.basic_consume(queue_name, callback, True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
