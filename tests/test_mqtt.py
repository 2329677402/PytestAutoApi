#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
@Date    : 2025/4/3 19:05
@Author  : Poco Ray
@File    : test_mqtt.py
@Software: PyCharm
@Desc    : Description
"""
import paho.mqtt.client as mqtt
import json
import time


def test_mqtt():
    """运行一个基本的 MQTT 设备端示例"""

    # 1. Broker 配置
    broker_address = 'test.mosquitto.org'  # 一个公共测试 Broker
    port = 1883  # 默认端口

    # 2. 定义 Topics
    status_topic = 'device_status'
    control_topic = 'device_control'

    # 用于在 on_message 回调中接收命令
    received_command = ''

    # 3. 定义回调函数
    def on_connect(client, userdata, connect_flags, reason_code, properties):
        """连接成功时的回调"""
        if reason_code == 0:
            print('成功连接到 MQTT Broker!')
            # 连接成功后订阅控制主题
            print(f"订阅主题: {control_topic}")
            client.subscribe(control_topic)
        else:
            print(f'连接失败，原因代码: {reason_code}')

    def on_message(client, userdata, message: mqtt.MQTTMessage):
        """收到消息时的回调"""
        nonlocal received_command
        topic = message.topic
        payload_str = message.payload.decode('utf-8')
        print(f'收到来自主题 "{topic}" 的消息: {payload_str}')
        try:
            # 假设控制命令是 JSON 格式，如 {"cmd": "stop"}
            data = json.loads(payload_str)
            if 'cmd' in data:
                received_command = data['cmd']
                print(f"解析到命令: {received_command}")
        except json.JSONDecodeError:
            print("收到的消息不是有效的 JSON 格式")
        except Exception as e:
            print(f"处理消息时出错: {e}")

    # 4. 创建 MQTT Client 实例
    #    使用 CallbackAPIVersion.VERSION2 和 MQTTv5 协议
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='poco_test_client', protocol=mqtt.MQTTv5)

    # 5. 绑定回调函数
    client.on_connect = on_connect
    client.on_message = on_message

    # 6. 连接 Broker
    print(f"尝试连接到 Broker: {broker_address}:{port}")
    client.connect(broker_address, port, keepalive=60)  # keepalive=60 秒

    # 7. 启动网络循环 (后台线程)
    client.loop_start()

    # 8. 主循环 - 定时发布状态并检查停止命令
    print(f"将定时向主题 '{status_topic}' 发布状态...")
    device_status = {
        "温度": 25.0,
        "电量": 0.80
    }
    publish_interval = 2  # 每隔多少秒发布一次
    run_duration = 20  # 总运行时间

    start_time = time.time()
    while time.time() - start_time < run_duration:
        # 更新状态
        device_status["电量"] = round(max(0, device_status["电量"] - 0.01), 2)
        status_payload = json.dumps(device_status, ensure_ascii=False).encode('utf-8')

        # 9. 发布消息
        result = client.publish(status_topic, payload=status_payload)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"发布状态: {device_status}")
        else:
            print(f"发布失败，代码: {result.rc}")

        time.sleep(publish_interval)

        # 10. 检查是否收到停止命令
        if received_command == 'stop':
            print("收到 'stop' 命令，准备退出...")
            break

    print("运行结束.")

    # 11. 停止循环与断开连接
    client.loop_stop()
    client.disconnect()
    print("已断开连接.")