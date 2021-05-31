#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import sys

hostname = 'localhost'
parameters = pika.ConnectionParameters(hostname)
connection = pika.BlockingConnection(parameters)

# 创建通道
channel = connection.channel()
# 定义交换机，设置类型为direct
channel.exchange_declare(exchange='change_dir', exchange_type='direct')

# 从命令行获取路由键参数，如果没有，则设置为info
routings = sys.argv[1:]
if not routings:
    routings = ['info']

# 生成临时队列，并绑定到交换机上，设置路由键
# ,durable=True
result = channel.queue_declare(queue='666', exclusive=True)
queue_name = result.method.queue
for routing in routings:
    channel.queue_bind(exchange='change_dir', queue=queue_name, routing_key=routing)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))


channel.basic_consume(queue_name, callback, True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
