# circuitpython_dfrobot_gravity_drf0627_dual_uart: Copyright (c) 2022 Graham Beland
#
# SPDX-License-Identifier: MIT

import time
import board
import circuitpython_dfrobot_gravity_drf0627_dual_uart as DualUart

i2c = board.I2C()


uart1 = DualUart.DFRobot_IIC_Serial(
    i2c,
    sub_uart_channel=DualUart.DFRobot_IIC_Serial.SUBUART_CHANNEL_1,
    IA1=1,
    IA0=1,
)

uart2 = DualUart.DFRobot_IIC_Serial(
    i2c,
    sub_uart_channel=DualUart.DFRobot_IIC_Serial.SUBUART_CHANNEL_2,
    IA1=1,
    IA0=1,
)

try:
    uart1.begin(9600, uart1.IIC_Serial_8N1)
    print("Opened: UART 1 ")
finally:
    pass

try:
    uart2.begin(9600, uart2.IIC_Serial_8N1)
    print("Opened: UART 2")
finally:
    pass

sendID = 1
sendDelayCount = 1

while True:
    time.sleep(0.3)
    sendDelayCount -= 1
    if sendDelayCount <= 0:
        sendDelayCount = 10
        uart1.write("From1:" + str(sendID))
        uart2.write("From2:" + str(sendID))

    if uart1 is not None:
        if uart1.available():
            s = ""
            while uart1.available():
                b = uart1.read(1)
                s += chr(b[0])
            print("<1:" + s + " len:" + str(len(s)) + ">")

    if uart2 is not None:
        if uart2.available():
            s = ""
            while uart2.available():
                b = uart2.read(1)
                s += chr(b[0])
            print("<2:" + s + " len:" + str(len(s)) + ">")
