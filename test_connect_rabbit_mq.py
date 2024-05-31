# import pika
#
# connection_params = pika.ConnectionParameters(
#     host="192.168.1.109",
#     port=5672,
#     # virtual_host='your_virtual_host',
#     credentials=pika.PlainCredentials('admin', '123456')
# )
#
# # producer
#
# # 建立连接
# connection = pika.BlockingConnection(connection_params)
#
# # 创建通道
# channel = connection.channel()
#
# # 声明一个交换机
# exchange_name = 'my_exchange'
# channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
#
# # 声明一个队列
# queue_name = 'my_queue'
# channel.queue_declare(queue=queue_name)
#
# # 将队列绑定到交换机
# routing_key = 'my_routing_key'
# channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
#
# # 发送消息到交换机
# message_body = 'Hello, RabbitMQ!'
# channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message_body)
#
# print(f" [x] Sent '{message_body}' with routing key '{routing_key}' to {exchange_name}")
#
# # 关闭连接
# connection.close()
#
# # consumer
#
#
# def callback(ch, method, properties, body):
#     print(f" [x] Received {body}")
#
# # 建立连接
# connection = pika.BlockingConnection(connection_params)
#
# # 创建通道
# channel = connection.channel()
#
# # 声明一个队列
# queue_name = 'my_queue'
# channel.queue_declare(queue=queue_name)
#
# # 设置回调函数，处理接收到的消息
# channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
#
# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()
