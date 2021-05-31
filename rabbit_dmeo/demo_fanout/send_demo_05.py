#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 每次消息都只会发送给其中一个接收端，如果需要将消息广播出去，让每个接收端都能收到，那么就要使用交换机
# 定义交换机
# 不是将消息发送到hello队列，而是发送到交换机

import pika

hostname = 'localhost'
parameters = pika.ConnectionParameters(hostname)
connection = pika.BlockingConnection(parameters)

# 创建通道
channel = connection.channel()
# 定义交换机，设置类型为topic
channel.exchange_declare(exchange='change_fan', exchange_type='fanout')

# 将消息发送到交换机
# basic_publish方法的参数exchange被设定为相应交换机
# 因为是要广播出去，发送到所有队列，所以routing_key就不需要设定
channel.basic_publish(exchange='change_fa', routing_key='', body='Hello RabbitMQ!')


connection.close()
