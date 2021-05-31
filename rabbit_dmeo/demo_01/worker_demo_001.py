#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pika
import time

hostname = 'localhost'
parameters = pika.ConnectionParameters(hostname)
connection = pika.BlockingConnection(parameters)

# 创建通道
channel = connection.channel()
# durable=True后将任务持久化存储，防止任务丢失
channel.queue_declare(queue='test_queue', durable=True)


# ch.basic_ack为当工作者完成任务后，会反馈给rabbitmq
def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))
    time.sleep(5)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# basic_qos设置prefetch_count=1，使得rabbitmq不会在同一时间给工作者分配多个任务，
# 即只有工作者完成任务之后，才会再次接收到任务。
channel.basic_qos(prefetch_count=1)

# 去除no_ack=True参数或者设置为False后可以实现
# 一个工作者ctrl+c退出后，正在执行的任务也不会丢失，rabbitmq会将任务重新分配给其他工作者。
channel.basic_consume('test_queue', callback, False)
# 开始接收信息，按ctrl+c退出
print('worker 1 [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
