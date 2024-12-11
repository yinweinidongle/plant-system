from flask import Flask, jsonify,request
from flask_cors import CORS
import math
import time
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import __common
import paho.mqtt.client as mqtt
import threading
import os


app = Flask(__name__)
CORS(app)

__common.init_env()

import jkrc


rc = jkrc.RC("192.168.2.16")



# Modbus TCP客户端配置
MODBUS_HOST = "192.168.2.14"  # 修改为您的PLC IP地址
MODBUS_PORT = 502  # 默认Modbus TCP端口

# MQTT配置
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "plc/register10"

MQTT_TOPIC_PHOTO_DONE = "plc/photo_done"

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

# 全局变量存储上一次的寄存器值
last_register_value = None
monitor_thread = None
stop_monitor = False


def monitor_register():
    """监控PLC寄存器10的值"""
    global last_register_value, stop_monitor
    client = get_modbus_client()
    connected = False
    firstCount = True # 第一次建立连接时，寄存器写入9
    
    while not stop_monitor:
        try:
            # 如果未连接,尝试建立连接
            if not connected:
                if client.connect():
                    connected = True
                    if firstCount:
                        client.write_register(address=9, value=0)
                        firstCount = False
                else:
                    time.sleep(5)  # 连接失败等待5秒重试
                    continue
                    
            # 读取寄存器
            result = client.read_holding_registers(address=9, count=2)
            if result.isError():
                # 读取错误,关闭连接重试
                connected = False
                client.close()
                client = get_modbus_client()
                time.sleep(5)
                continue
                
            print(result.registers[0])
            current_value = result.registers[0]
            
            if str(current_value) == "2":
                # 发送MQTT消息
                mqtt_client.publish(MQTT_TOPIC, str(current_value))
                
                # 写入寄存器
                write_result = client.write_register(address=9, value=3)
                if write_result.isError():
                    connected = False
                    client.close() 
                    client = get_modbus_client()
                    continue
                    
                robot_path_within()
                
                write_result = client.write_register(address=9, value=4)
                if write_result.isError():
                    connected = False
                    client.close()
                    client = get_modbus_client()
                    continue
                    
            time.sleep(1)  # 每秒检查一次
            
        except Exception:
            # 发生异常时关闭连接重试
            connected = False
            client.close()
            client = get_modbus_client() 
            time.sleep(5)

#==============================PLC==================================

def get_modbus_client():
    """创建并返回Modbus TCP客户端实例"""
    return ModbusTcpClient(host=MODBUS_HOST, port=MODBUS_PORT)

@app.route('/plc/start', methods=['GET'])
def plc_start():
    """启动PLC"""
    try:
        global monitor_thread, stop_monitor
        
        # 写入启动命令（假设使用线圈地址1控制启动）
        #result = client.write_coil(address=9, value=5)
        # client.close()

        # if result.isError():
        #     return jsonify({"status": "error", "message": "启动命令执行失败"}), 500

        # 启动监控线程
        stop_monitor = False
        monitor_thread = threading.Thread(target=monitor_register, daemon=True)
        monitor_thread.start()

        

        return jsonify({"status": "success", "message": "PLC已启动，开始监控寄存器"})

    except ModbusException as e:
        return jsonify({"status": "error", "message": f"Modbus错误: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": f"系统错误: {str(e)}"}), 500



@app.route('/plc/stop', methods=['GET'])
def plc_stop():
    """关闭PLC"""
    try:
        global stop_monitor
        
        # 停止监控线程
        stop_monitor = True
        
        # 写入寄存器20值为0
        client = get_modbus_client()
        if client.connect():
            client.write_register(address=20, value=0)
            client.close()
        
        return jsonify({"status": "success", "message": "PLC已关闭"})

    except ModbusException as e:
        return jsonify({"status": "error", "message": f"Modbus错误: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": f"系统错误: {str(e)}"}), 500








@app.route('/plc/write_register', methods=['POST'])
def write_register():
    """写入寄存器值"""
    try:
        client = get_modbus_client()
        if not client.connect():
            return jsonify({"status": "error", "message": "无法连接到PLC"}), 500

        # 写入寄存器值
        param1 = request.get_json()
        value1 = int(param1["value"])
        print("write test")
        print(value1)
        result = client.write_register(address=9, value=value1)
        client.close()
        
        if result.isError():
            return jsonify({"status": "error", "message": "写入寄存器失败"}), 500
            
        return jsonify({"status": "success", "message": "寄存器写入成功"})
        
    except ModbusException as e:
        return jsonify({"status": "error", "message": f"Modbus错误: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": f"系统错误: {str(e)}"}), 500

#==============================机械臂==================================


#连接机械臂
@app.route('/robot/connection', methods=['POST'])
def robot_connection():
    """连接机械臂"""
    param = request.get_json()
    status = param['status']
    try:
        if status:
            rc.login()
            print(rc.power_on())
            print(rc.enable_robot())
            return jsonify({"status": "success", "message": "机械臂连接成功"}), 200 
        else:
            print(rc.disable_robot())
            print(rc.power_off())
            print(rc.logout())
            return jsonify({"status": "success", "message": "机械臂已断开"}), 500
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"系统错误: {str(e)}"}), 500



@app.route('/robot/status', methods=['GET'])
def get_robot_status():
    """获取机械臂状态"""
    try:
      
      ret = rc.get_robot_status()
      return jsonify({"status": ret[1][19], "message": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"系统错误: {str(e)}"}), 500



@app.route('/control/all', methods=['GET','POST'])
def control_move():
    """控制机械臂关节"""
    param1 = request.get_json()
    #return jsonify({"status": param1['angles'], "connected": True, "message": "success"}), 200
    seconds = 1
    try:
      jstep_pos = param1['angles']

      print('joint_move {}'.format(rc.joint_move(jstep_pos, 0, True, 0.1 * math.pi)))

      time.sleep(seconds)

      return jsonify({"status": "操作成功", "message": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"系统错误: {str(e)}"}), 500

@app.route('/robot/move', methods=['GET','POST'])
def robot_move():
    """机械臂移动"""

    seconds = 5
    try:
      jstep_pos = [3.2275728085307915, 0.2084609041277263, 1.4049673585751594, -0.042503322595409634,
                     -1.6624165132137128, -0.02929782986226265]

      jstep_pos1 = [-3.1043420913644786, 0.2084609041277263, 1.4049673585751594, -0.042503322595409634,
                      -1.6624165132137128, -0.02929782986226265]

      jstep_pos2 = [-3.1043420913644786, 0.3635379460234777, 1.1980285560880974, 0.009358581112899734,
                      -1.6624165132137128, -0.02929782986226265]

      jstep_pos3 = [3.2275728085307915, 0.3635379460234777, 1.1980285560880974, 0.009358581112899734,
                      -1.6624165132137128, -0.02929782986226265]

      

      print('joint_move {}'.format(rc.joint_move(jstep_pos, 0, True, 0.2 * math.pi)))

      time.sleep(seconds)

      print('joint_move {}'.format(rc.joint_move(jstep_pos1, 0, True, 0.2 * math.pi)))

      time.sleep(seconds)

      print('joint_move {}'.format(rc.joint_move(jstep_pos2, 0, True, 0.2 * math.pi)))

      time.sleep(seconds)

      print('joint_move {}'.format(rc.joint_move(jstep_pos3, 0, True, 0.2 * math.pi)))

      time.sleep(seconds)

      print('joint_move {}'.format(rc.joint_move(jstep_pos, 0, True, 0.2 * math.pi)))

      time.sleep(seconds)


      return jsonify({"status": "操作成功", "message": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"系统错误: {str(e)}"}), 500


#按照轨迹移动
@app.route('/take-path', methods=['GET', 'POST'])
def robot_path():
    """按照轨迹移动"""
    seconds = 1
    try:
        jstep_pos = [3.421245074388507,0.4216572301278098,1.6015262762972118,-0.6340206915069545,-1.5187618875202742,0.2971691964211417]

        jstep_pos1 = [-3.331219502353403,0.4350980812235341,1.6169649785331874,-0.6670020878405415,-1.5363756361328524,0.39199373978631286]

        jstep_pos2 = [-3.246968652508203,0.503098661803149,0.662501153184118,0.22295499090091325,-1.5209532140164426,0.30909292360629015]

        jstep_pos3 = [3.401810773086636,0.503098661803149,0.662501153184118,0.22295499090091325,-1.5209532140164426,0.30909292360629015]



        print('joint_move {}'.format(rc.joint_move(jstep_pos, 0, True, 0.1 * math.pi)))
        time.sleep(seconds)

        print('joint_move {}'.format(rc.joint_move(jstep_pos1, 0, True, 0.1 * math.pi)))
        time.sleep(seconds)

        print('joint_move {}'.format(rc.joint_move(jstep_pos2, 0, True, 0.1 * math.pi)))
        time.sleep(seconds)

        print('joint_move {}'.format(rc.joint_move(jstep_pos3, 0, True, 0.1 * math.pi)))
        time.sleep(3)
     

        #return jsonify({"status": "操作成功", "message": "success"}), 200
    except Exception as e:
        print(str(e))
        #return jsonify({"status": "error", "message": f"系统错误: {str(e)}"}), 500


def robot_path_within():
    """按照轨迹移动"""
    seconds = 1
    try:
        jstep_pos = [3.421245074388507,0.4216572301278098,1.6015262762972118,-0.6340206915069545,-1.5187618875202742,0.2971691964211417]

        jstep_pos1 = [-3.331219502353403,0.4350980812235341,1.6169649785331874,-0.6670020878405415,-1.5363756361328524,0.39199373978631286]

        jstep_pos2 = [-3.246968652508203,0.503098661803149,0.662501153184118,0.22295499090091325,-1.5209532140164426,0.30909292360629015]

        jstep_pos3 = [3.401810773086636,0.503098661803149,0.662501153184118,0.22295499090091325,-1.5209532140164426,0.30909292360629015]



        print('joint_move {}'.format(rc.joint_move(jstep_pos, 0, True, 0.4 * math.pi)))
        time.sleep(seconds)

        print('joint_move {}'.format(rc.joint_move(jstep_pos1, 0, True, 0.4 * math.pi)))
        time.sleep(seconds)

        print('joint_move {}'.format(rc.joint_move(jstep_pos2, 0, True, 0.4 * math.pi)))
        time.sleep(seconds)

        print('joint_move {}'.format(rc.joint_move(jstep_pos3, 0, True, 0.4 * math.pi)))
        time.sleep(3)
     

        #return jsonify({"status": "操作成功", "message": "success"}), 200
    except Exception as e:
        print(str(e))
        #return jsonify({"status": "error", "message": f"系统错误: {str(e)}"}), 500

 #旋转拍照指令
@app.route('/take-photo', methods=['GET', 'POST'])
def robot_photo():
    """旋转拍照"""

    seconds = 1
    try:
        jstep_pos = [3.3104008039177644, 0.2345506038754577, 1.2486988344560341, -0.09865889516601413, -1.5390541147611683, 0.2846528425232535]

        jstep_pos1 = [-3.092362238500228, 0.2345506038754577, 1.2486988344560341, -0.09865889516601413, -1.5390541147611683, 0.2846528425232535]


        print('joint_move {}'.format(rc.joint_move(jstep_pos, 0, True, 0.4 * math.pi)))
        time.sleep(seconds)

        print('joint_move {}'.format(rc.joint_move(jstep_pos1, 0, True, 0.4 * math.pi)))
        time.sleep(seconds)
 

        #plc寄存器10写入1
        client = get_modbus_client()
        client.write_register(address=10, value=3)
        client.close()

        # 发送MQTT消息,拍照完成
        
        #mqtt_client.publish(MQTT_TOPIC_PHOTO_DONE, "1")

        print('joint_move {}'.format(rc.joint_move(jstep_pos, 0, True, 0.4 * math.pi)))
        time.sleep(seconds)
     

        return jsonify({"status": "操作成功", "message": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"系统错误: {str(e)}"}), 500
    
#急停
@app.route('/emergency-stop', methods=['GET', 'POST'])
def robot_stop():
    """急停"""
    try:
      
      print(rc.disable_robot())
      print(rc.power_off())
      return jsonify({"status": "操作成功", "message": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"系统错误: {str(e)}"}), 500



#==============================nerf重建==================================
"""
远程执行指令流程:
1. 判断指令类型：01-录屏，02-抽帧；03-重建；04-生成点云
2. 运行对应指令命令
3. 运行完成后，返回操作成功，发送mqtt消息
"""
@app.route('/task/job', methods=['GET','POST'])
def task_job():
    """执行任务"""
    param1 = request.get_json()
    task_id = str(param1['taskId'])

    
    # exec_02_frames.bat的BAT文件,存放抽帧指令
    bat_frames = r'C:\Users\86151\Desktop\Nerf\exec_02_frames.bat'
    # exec_03_rebuild.bat的BAT文件,存放nerf重建指令
    bat_nerf = r'C:\Users\86151\Desktop\Nerf\exec_03_nerf.bat'
    # exec_04_points.bat的BAT文件,存放生成点云指令
    bat_points = r'C:\Users\86151\Desktop\Nerf\exec_04_points.bat'


    if task_id == '1':
        #录屏
        # 启动监控线程
        monitor_thread = threading.Thread(target=handle_task_camera, daemon=True)
        monitor_thread.start()
        
        pass
    elif task_id == '2':
        #抽帧
        os.system(bat_frames)
        #todo mqtt发送抽帧  mqtt_client.publish("task/job", str(task_id))
        pass
    elif task_id == '3':
        #重建
        os.system(bat_nerf)
        #todo mqtt发送重建  mqtt_client.publish("task/job", str(task_id))
        pass  
    elif task_id == '4':
        #生成点云
        os.system(bat_points)
        #todo mqtt发送点云  mqtt_client.publish("task/job", str(task_id))
        pass

    return jsonify({"status": param1['taskId'], "connected": True, "message": "success"}), 200
    
    try:
      

      return jsonify({"status": "操作成功", "message": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"系统错误: {str(e)}"}), 500
    

def handle_task_camera():
    # exec_01_camera.bat的BAT文件,存放录屏指令
    bat_camera = r'C:\Users\86151\Desktop\Nerf\exec_01_camera.bat'
    os.system(bat_camera)
    print("task1:camera")
    #todo mqtt发送录屏  mqtt_client.publish("task/job", str(task_id))
    time.sleep(3)
    mqtt_client.publish("task/job", "1")

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)