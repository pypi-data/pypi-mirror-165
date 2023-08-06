#encoding:utf-8
import random,time
import os,sys,jsonpath
import platform as pf
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from time import sleep
import shutil

from loguru import logger
from pywebio.input import FLOAT,NUMBER,input_group,select, textarea,file_upload,checkbox,radio,actions
from pywebio.output import close_popup, output, put_file, put_html, put_image, put_markdown, put_text,popup,put_link,put_code,put_row,put_processbar,set_processbar,put_error,put_warning,toast,put_grid,put_button,put_table,use_scope,span,clear,remove
from pywebio import start_server,session,platform
from core.bladeTest.main import RemoteRunner,generateHtmlReport,running
from core.jmeterTool.swagger2jmeter import swagger2jmeter
from core.jmeterTool.har2jmeter import har2jmeter
from core.xmind2excel import makeCase
from core.utils import CFacker,getDateTime,parseJmeterXml,getTimeStamp,getDateTime,formatStr2Timestamp,timeStampStr2FormatTime,jsonPrettyOutput
from core.mqttUtil import NormalMqttGetter,NormalMqttSender
from core.kafkaUtil import general_sender,continue_orderMsg,general_orderMsg,general_orderMsgWithFilter,kafkaFetchServerWithFilter,kafkaFetchServer
from functools import partial
from multiprocessing import Process
import decimal,websockets,asyncio
import json
from functools import partial

import pywebio.output as output
import pywebio.input as inputs
import pywebio.pin as pin
from pywebio.session import hold
import  traceback
from core.httpUtil import HttpOper



def modle2command_new(modle_str):
    try:
        jstr=json.loads(modle_str)#rawStr2)
        productIds=jsonpath.jsonpath(jstr, "$.standardFunctions[*].identifier")
        allcommands=jsonpath.jsonpath(jstr, "$.standardFunctions[*].commands")
        
        # print(productIds)
        # print(allcommands)

        # for a,b in zip(productIds,allcommands):
        #     print(a,b)

        if productIds.__len__()>=1:
            for productId,commands in zip(productIds,allcommands):
                # commands=jsonpath.jsonpath(jstr, "$.standardFunctions[*].commands[*]")
                if not commands:
                    continue
                else:
                    resTotal=[]
                    for command in commands:
                        # print('--'*10)
                        function_id=command['identifier']
                        command_id=""
                        command_value=[]
                        if command['inputs']!=[] :
                            # print(command['inputs'][0]['identifier'])
                            command_id=command['inputs'][0]['identifier']
                            # print(command['inputs'][0]['dataType'])
                            command_type=command['inputs'][0]['dataType']
                            
                            # if command_type=='enum' or command_type=='bool':
                            if command['inputs'][0].__contains__('specifications'):
                                values=command['inputs'][0]['specifications']
                                # print(values)
                                for value in values:
                                    # print(value['value'])
                                    command_value.append(value['value'])
                            elif command['inputs'][0].__contains__('specification'):
                                
                                values=command['inputs'][0]['specification']
                                if values.__contains__('min'):
                                    # print(values['min'])
                                    minNum=int(values['min'])
                                    command_value.append(minNum-1)
                                if values.__contains__('max'):
                                    # print(values['max'])
                                    maxNum=int(values['max'])
                                    command_value.append(maxNum+1)
                                # if values.__contains__('digit'):
                                    # print(values['digit'])
                                # if values.__contains__('step'):
                                    # print(values['step'])
                                if values.__contains__('accuracy'):
                                    # print(values['accuracy'])
                                    acc=int(values['accuracy'])
                                    command_value.append(round((minNum+maxNum)/2,acc))
                                    command_value.append(round((minNum+maxNum)/2,acc+1))
                                command_value.append((minNum+maxNum)//2)
                        # print(productId)
                        # print(function_id)
                        # print(command_id)
                        # print(command_value)

                        if command_value.__len__()>0:
                            for one in command_value:
                                tempLine=[]
                                tempLine.append(productId)
                                tempLine.append(function_id)
                                tempLine.append(command_id)
                                tempLine.append(one)
                                resTotal.append(tempLine)
                        else:
                                tempLine=[]
                                tempLine.append(productId)
                                tempLine.append(function_id)
                                resTotal.append(tempLine)
                    return resTotal
    except Exception as e:
        print(traceback.print_exc())



def commandConstruct(commandList,deviceId=123):
    totalCmds=""
    for one in commandList:
        if type(one)==list and one.__len__()==4:
            commandStr=f'''{{"cmd": {{"command": "{one[1]}","function": "{one[0]}","param":{{"{one[2]}":"{one[3]}"}} }},"deviceId": "{deviceId}"}}'''
            # return(commandStr)
            totalCmds=totalCmds+commandStr+"\n"
        elif type(one)==list and one.__len__()==2:
            commandStr=f'''{{"cmd": {{"command": "{one[1]}","function": "{one[0]}"}},"deviceId": "{deviceId}"}}'''
            # return(commandStr)
            totalCmds=totalCmds+commandStr+"\n"
    return totalCmds








@use_scope('content',clear=True)
def businessProcess():
    session.set_env(title='testToolKit')
    clear('content')
    select_type = select("选择你要做的操作:",["指令生成","指令生成发送","属性上报--","点位生成--"])
    if select_type=="指令生成":
        commandGenerator()
    elif select_type=="指令生成发送":
        commandGeneratorAndSend()




def modle2command(deviceId,modle_str):
    '''
    用法：
    将数据库xxxx表中字段model_content当做参数modle_str；会生成下发指令的集合
    如：
                                    {
                                "cmd": {
                                    "command": "door_status_set",
                                    "function": "door",
                                    "param":{"door_status_value":"['1', '0']"}
                                },
                                "deviceId": "123456"
                                }
    表示，可以下发的值包含['1', '0']
    '''

    totalCommand=""
    jstr=json.loads(modle_str)#rawStr2)
    productId=jsonpath.jsonpath(jstr, "$.standardFunctions[*].identifier")
    for num, p_id in enumerate(productId):
        totalCommand=totalCommand+"##############################"+"\n"
        commands=jsonpath.jsonpath(jstr, "$.standardFunctions["+str(num)+"].commands[*]")
        if commands:
            for command in commands:
                # print('--'*10)
                totalCommand=totalCommand+"-----------------------------"+"\n"
                # print(command['identifier'])
                function_id=command['identifier']
                # print(f"#######{command['inputs']}")
                command_value=[]
                if command['inputs']!=[] :
                    # print(command['inputs'][0]['identifier'])
                    command_id=command['inputs'][0]['identifier']
                    # print(command['inputs'][0]['dataType'])
                    command_type=command['inputs'][0]['dataType']
                    
                    if command['inputs'][0].__contains__('specifications'):
                        
                        values=command['inputs'][0]['specifications']
                        # print(values)
                        for value in values:
                            # print(value['value'])
                            command_value.append(value['value'])
                    elif command['inputs'][0].__contains__('specification'):
                        minNum=None
                        maxNum=None
                        acc=None
                        values=command['inputs'][0]['specification']
                        # print(f"##################################################{values}")
                        if values!="{}":
                            if values.__contains__('min'):
                                # print(values['min'])
                                minNum=int(values['min'])
                                command_value.append(minNum-1)
                            if values.__contains__('max'):
                                # print(values['max'])
                                maxNum=int(values['max'])
                                command_value.append(maxNum+1)
                            # if values.__contains__('digit'):
                                # print(values['digit'])
                            # if values.__contains__('step'):
                                # print(values['step'])
                            if values.__contains__('accuracy'):
                                # print(values['accuracy'])
                                acc=int(values['accuracy'])
                                command_value.append(round((minNum+maxNum)/2,acc))
                                command_value.append(round((minNum+maxNum)/2,acc+1))
                                command_value.append((minNum+maxNum)//2)
                # print(p_id)
                # print(function_id)
                # print(command_id)
                # print(command_value)
                commandStr=f'''{{"cmd": {{"command": "{function_id}","function": "{p_id}","param":{{"{command_id}":"{command_value}"}} }},"deviceId": "{deviceId}"}}
                '''
                totalCommand=totalCommand+commandStr+"\n"
            return totalCommand
            # print(totalCommand)

def commandGenerator():
    output.put_markdown("## 请输入设备信息和模型信息：")
    pin.put_input(name='deviceId',label='设备信息,设备id')
    pin.put_textarea(name='modleJson',label='模型信息,物模型定义Json字符串',rows=10)
    def getValueAndCall():
        deviceId=pin.pin.deviceId
        modleJson=pin.pin.modleJson

        output.put_text(commandConstruct(deviceId=deviceId, commandList=modle2command_new(modleJson)))

    output.put_button(label='提交', onclick=lambda :getValueAndCall())


def commandGeneratorAndSend():
    put_text("指令信息:")
    data = input_group("配置信息", [
        inputs.input("设备号，必填", name="deviceId",value='123456'),
        inputs.textarea("模型信息json，必填", name="model",value='json 字符串'),
        inputs.input("请求地址，必填", name="url",value='http://127.0.0.1:9999/device'),
        inputs.input("请求头，必填", name="header",value='{"Content-Type":"application/json"}'),
    ])
    # print(data['model'])
    commandStr=commandConstruct(deviceId=data['deviceId'], commandList=modle2command_new(data['model']))
    commandStrList=commandStr.split('\n')
    print(commandStrList)


    # for index,one in enumerate(commandStrList):
    #     output.put_text(f"编号：{index}\n{one}")
        
    # pin.put_input(name="num",value="编号：",label="输入编号,发送请求：")
    # def sendRequest(num):
    #     content=commandStrList[int(num)]
    #     res=HttpOper().call('POST', data['url'],headers=json.loads(data['header']),data=content)
    #     output.popup(title='请求响应信息',content=output.put_text(f"地址：\n{data['url']}\n请求头：\n{data['header']}\n请求数据：\n{content}\n响应：\n{res.res.content.decode('utf-8')}"))
    # output.put_button(label="发送", onclick=lambda: sendRequest(pin.pin.num))
    pin.put_select(name='name',label='选择要发送得指令',options=commandStrList)
    def sendRequest(content):
        content=pin.pin.name
        res=HttpOper().call('POST', data['url'],headers=json.loads(data['header']),data=content)
        res1=res.res.content.decode('utf-8')
        output.popup(title='请求响应信息',content=output.put_text(f"地址：\n{data['url']}\n请求头：\n{data['header']}\n请求数据：\n{content}\n响应：\n{res1}"))
    
    output.put_button(label="单条发送", onclick=lambda: sendRequest(pin.pin.num))


    def sendRequestAll(contentList):
        resList=[]
        for one in contentList:
            res=HttpOper().call('POST', data['url'],headers=json.loads(data['header']),data=one)
            res1=res.res.content.decode('utf-8')
            resList.append(res1+"\n"+"*"*20+"\n")
        
        output.popup(title='请求响应集合',content=output.put_text(f"响应集合：\n{''.join(resList)}"))
    
    output.put_html("<h1>全部发送<h1>")
    output.put_text("\n".join(commandStrList))
    output.put_button(label="全部发送", onclick=lambda: sendRequestAll(commandStrList))


if __name__=='__main__':
    start_server(businessProcess,port=9999,debug=True,cdn=False,auto_open_webbrowser=True)

