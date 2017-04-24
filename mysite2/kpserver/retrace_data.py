#coding:utf-8
import re
import os.path
import sys
import subprocess
import json
import types
import hashlib
import ast
from configure import *
import gzip
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from .proguardks3 import Conn



def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        try:
            os.makedirs(path)
        except:
            return False
    return True


def md5_encryption(string):#使用MD5加密算法加密数据
    m = hashlib.md5()
    if string:
        m.update(string)
        psw = m.hexdigest()
        return psw
    return None


def get_file_path(data, mapping_seletor):#获取文件保存位置,并保存 version, appkey,package三个信息
    version = split_data(data, 'version')#获取版本信息
    appkey = split_data(data, 'appkey')#获取appkey
    package = split_data(data, 'package')#获取包名
    try:
        mapping_seletor.update({'version': version, 'appkey': appkey, 'package': package})#保存mapping信息
        version = md5_encryption(version)  # 使用MD5加密version
        package = md5_encryption(package)#使用MD5加密package
        appkey = appkey.lower()#将appkey转化为小写
        package = package.lower()
        version = version.lower()
        path = WORK_PATH + appkey + '/' + version + '/' + package + '/'
    except:
        return None
    res = mkdir(path)#根据路径创建文件
    if res:#创建文件成功
        return path
    return None


def load_mapping(filename):#将mapping一次性读取
    try:
        file_object = open(filename)
        all_the_text = file_object.readlines()#按行读取文件所有内容，保存到列表中
        file_object.close()
    except:
        return None
    return all_the_text#返回文件内容列表


def find_file(filename):#到指定目录查找mapping.txt
    filename = filename.strip()
    FileExists = os.path.exists(filename)
    if FileExists:
        return True
    else:
        return False


def getdata(request):#获取post数据
    try:
        data = request.read()
        return data
    except:
        return None


def split_data(data, key):#根据key获取数据
    try:#将字符串转化为字典
        data = ast.literal_eval(data)
    except:
        return None
    if type(data) is types.DictionaryType:
        if key in data:
            value = data.get(key, None)
        else:
            return None
        return value
    else:
        try:#将字符串转化为字典
            data = ast.literal_eval(data)
        except:
            return None
    if key in data:
        value = data.get(key, None)
    else:
        return None
    return value


def data_process(request, dictr):#获取数据段
    data = getdata(request)
    if not data or data.strip() == '':#数据段是否为空
        data = None
        dict1 = {'result': 'fail', 'stacks': data, 'reason': 'data is empty'}
        dictr.update(dict1)
        return None
    else:#数据段不为空时执行获取stacks数据
        return data


def get_proguarded_data(request, data, dictr):#提取stacks数据段
    stack = split_data(data, 'stacks')#获取stacks段
    if stack:
        return stack
    else:
        dict1 = {'result': 'fail', 'stacks': None, 'reason': 'stacks is not exist'}
        dictr.update(dict1)
        return None

'''
获取匹配规则,并返回
list_rules = [
            {'proguardclass': strclass, 混淆的类名 
            'rule': str_rule,           匹配规则 
            'rawstack': rawstack,       原始stacks数据
            'result': [],               匹配结果
            'function': strfunction     函数名
            },...]
'''
def get_rules(stack):
    list_rules = []  # 保存混淆规则
    if type(stack) is types.StringType:  # stacks 是一个字符串
        rule = get_string_rules(stack)
        list_rules.append(rule)
    else:#stacks是一个列表
        for v in stack: # 循环取出列表中的每一个stack
            rule = get_string_rules(v)
            list_rules.append(rule)
    return list_rules

'''
{'proguardclass': strclass, 'rule': str_rule, 'rawstack': rawstack, 'result': [], 'function': strfunction}
    混淆的类名              匹配规则        原始stacks数据         匹配结果         函数名
'''
def get_string_rules(rawstack):

    dic_t = {}
    stack = re.findall(r'\w*\.\w*\..*', rawstack)
    if stack:  # 第一次提取匹配字符串成功
        stack = stack[0]
        if '(' and ')' in stack:
            stack = re.findall(r'^(.+?)\(', stack)
            if stack:  # 第二次提取待字符串匹配成功
                strl = stack[0]
                length = len(strl)
                index = strl.rfind('.')
                strclass = strl[0:index]  # 保存混淆类名
                strfunction = strl[index + 1:length]  # 保存混淆函数名
                str_rule = ')' + ' -> ' + strfunction
                dic_t = {'proguardclass': strclass, 'rule': str_rule, 'rawstack': rawstack, 'result': [], 'function': strfunction}
            else: # stacks无效
                dic_t = {'proguardclass': None, 'rule': None, 'rawstack': rawstack, 'result': []}
        else:
            length = len(stack)
            index = stack.rfind('.')
            strclass = stack[0:index]  # 保存混淆类名
            strfunction = stack[index + 1:length]  # 保存混淆函数名
            str_rule = ')' + ' -> ' + strfunction
            dic_t = {'proguardclass': strclass, 'rule': str_rule, 'rawstack': rawstack, 'result': [], 'function': strfunction}
    else:  # stacks无效
        dic_t = {'proguardclass': None, 'rule': None, 'rawstack': rawstack, 'result': []}
    return dic_t


def match_string(file_content, rules):#第一个参数是文件内容，第二个参数是匹配规则列表
    length = len(file_content)
    for i in range(0, length):#循环从列表中取出文件内容
        line = file_content[i]
        line = line.rstrip('\n')#去掉最后一个字符'\n'
        line = line.strip()#去掉空格符
        if len(line) == 0:
            continue
        for r_dict in rules:#循环从rules中取出匹配规则
            rawstack = r_dict['rawstack']#stacks原始数据
            rule = r_dict['rule']#匹配规则
            proguardclass = r_dict['proguardclass']#混淆的类名
            if (proguardclass is None) or (rule is None):#如果匹配类名或者匹配规则为None,则结束本次循环
                continue
            else:
                strend = proguardclass + ':'
                if line.endswith(strend):#先根据被混淆的类名找到开始匹配的位置
                    start_index = i#保存起始位置下标
                    lis_t = line.split('->')
                    retrace_class = lis_t[0]#保存混淆前的类名
                    retrace_class = retrace_class.strip()
                    while i < length - 1:
                        i = i + 1
                        line = file_content[i]
                        line = line.rstrip('\n')  # 去掉最后一个字符'\n'
                        line = line.strip()
                        if len(line) == 0:
                            continue
                        if line.endswith(':'):  # 另一种类型
                            end_index = i#保存结束位置下标
                            i = i - 1
                            rules = search(file_content, start_index, end_index, proguardclass, rules, retrace_class)#传入匹配范围下标
                            break
                else:
                    continue
        i = i + 1
    return rules

def search(file_content, start_index, end_index, proguardclass, rules, retrace_class):
    dict_1 = {'retrace_class': retrace_class}#保存混淆之前的类名
    for i in range(start_index, end_index):#范围匹配
        for r_dic in rules:#从规则列表中取出，存放在字典中的匹配信息
            if r_dic['proguardclass'] == proguardclass:#判断当前规则 proguardclass 值是否为需要匹配的 proguardclass 值
                line = file_content[i]
                line = line.rstrip('\n')#去结尾换行符
                line = line.strip()#去空格
                rule = r_dic['rule']
                result = r_dic['result']
                if 'retrace_class' not in r_dic:#字典中无类名就更新
                    r_dic.update(dict_1)
                if line.endswith(rule):#此字符串是否以 rule结尾
                    line1 = re.findall(' .*\(', line)
                    str4 = str(line1[0])
                    str5 = str4.replace('(', '')
                    str5 = str5.strip()
                    str5 = str5.split(' ')
                    leng = len(str5)
                    result.append(str(str5[leng - 1]))#保存匹配结果（原函数名）
            else:
                continue
    return rules


def arrange_result(rules):#整理匹配结果
    match_result = []#保存匹配结果
    for r_dict in rules:#取出所有结果进行整理
        if len(r_dict['result']) == 0:#如果结果为0个,说明没有匹配，则保存原始数据
            stack = r_dict['rawstack']  # 得到stacks
            try:
                proguardclass = r_dict['proguardclass']#混淆的类名
                classname = r_dict['retrace_class']#混淆之前的类名
                stack = stack.replace(proguardclass, classname)#如果有classname就成功替换，替换失败直接执行append
            except:
                match_result.append(r_dict['rawstack'])
                continue
            match_result.append(r_dict['rawstack'])
        else:
            if len(r_dict['result']) == 1:#如果结果只有一个
                match = r_dict['result']#保存结果，列表
                stack = r_dict['rawstack']#得到stacks
                func = r_dict['function']#被混淆的函数名
                proguardclass = r_dict['proguardclass']#混淆后的类名
                classname = r_dict['retrace_class']#混淆之前的类名
                strl = str(match[0])
                strl = strl.strip()
                strl = str(strl)
                strold = proguardclass + '.' + func#混淆后的类名+函数名
                strnew = classname + '.' + strl#混淆之前的类名和函数名
                stack = stack.replace(strold, strnew)#将混淆的类名和函数名替换为混淆之前的名字
                match_result.append(stack)#保存匹配结果到列表中
            else:#多个匹配结果

                match = r_dict['result']  # 保存结果，列表
                stack = r_dict['rawstack']  # 得到stacks原始数据
                func = r_dict['function']  # 被混淆的函数名
                proguardclass = r_dict['proguardclass']#混淆后的类名
                classname = r_dict['retrace_class']#混淆之前的类名
                strl = match[0] #先取出第一个匹配结果
                length = len(match)#获取匹配记过里的表的长度
                for i in range(1, length):#将其余匹配以 (*** | *** | ***)格式保存
                    if i == 1:
                        strl = strl + '(' + str(match[i])
                    else:
                        strl = strl + ' | ' + str(match[i])
                strl = strl + ')'
                strl1 = classname + '.' + strl#混淆之前的类名和所有可能的函数名
                str2 = proguardclass + '.' + func#混淆后的类名+函数名
                stack = stack.replace(str2, strl1)
                match_result.append(stack)
    return match_result


def Request(request):#处理请求
    dic_tr = {}
    mapping_selector = {}
    data = data_process(request, dic_tr)  # 获取data数据
    if data is None:  # data 为空
        dictjson = json.dumps(dic_tr)
        return dictjson
    stack = get_proguarded_data(request, data, dic_tr)  #获取stacks数据段
    if stack is None:
        dictjson = json.dumps(dic_tr)
        return dictjson
    path = get_file_path(data, mapping_selector)  # 获取文件所在目录,和 mapping文件信息
    if path is None:
        dic_t = {'result': 'fail', 'stacks': stack, 'reason': 'No search directory or create directory fail'}
        dictjson = json.dumps(dic_t)
        return dictjson
    rules = get_rules(stack)  # 获取匹配规则
    file_path = path + MAPPING_FILENAME#指定文件路径
    res = find_file(file_path)  # 指定路径下查找 mapping.txt文件
    if res is False:  # 在指定路径下找不到mapping.txt
        # 根据mapping信息从金山云上获取mapping.txt,保存到path路径下
        res_ks3 = get_mapping_from_ks3(path, mapping_selector)
        if res_ks3 is None:  # 从金山云获取数据失败
            dic_t = {'result': 'fail', 'stacks': stack, 'reason': 'request ks3 fail'}
            dictjson = json.dumps(dic_t)
            return dictjson
    all_file_context = load_mapping(file_path)  # 读取mapping.tx文件
    rule = match_string(all_file_context, rules)  # 获取匹配结果
    res = arrange_result(rule)  # 整理结果
    dic_t = {'result': 'successful', 'stacks': res}
    dictjson = json.dumps(dic_t)
    return dictjson


def get_mapping_from_ks3(path, mapping_selector):#从金山云上获取数据,保存在path路径下
    connect = Conn(KS3_K["AK"], KS3_K["SK"], "kss.ksyun.com", KS3_K['PROGUARD_BUCKET_NAME'])
    version = mapping_selector['version']
    appkey = mapping_selector['appkey']
    package = mapping_selector['package']
    key = connect.make_key(appkey, version, package)
    path_file = path + GZIP_MAPPING_FILENAME #保存下载数据的文件路径
    re_d = connect.download(path_file, key)
    if re_d['result'] == 0:#下载成功
        gzfile = path_file
        dest_file = path + MAPPING_FILENAME #保存解压结果的文件路径
        gunzipfile(gzfile, dest_file)
        return path
    else:
        return None


def gunzipfile(gzfile, dst):
    fin = gzip.open(gzfile, 'rb')
    fout = open(dst, 'wb')
    in_out(fin, fout)


def in_out(fin, fout):
    BufSize = 1024 * 8
    while True:
        buf = fin.read(BufSize)
        if len(buf) < 1:
            break
        fout.write(buf)
    fin.close()
    fout.close()
