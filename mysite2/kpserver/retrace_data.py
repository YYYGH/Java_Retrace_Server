#coding:utf-8
import re
import os.path
import json
import types
import hashlib
import ast
from configure import *
import gzip
import logging
from .proguardks3 import Conn
logger = logging.getLogger(LOGGING_NAME)


'''
根据路径创建目录
@param    path    指定的路径 
@return ：成功返回True， 否则返回False
'''
def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        try:
            os.makedirs(path)
        except:
            logger.error("retrace_data.py file call function mkdir 26 line error")
            return False
    return True

'''
使用MD5加密算法加密数据
@param string   待加密的字符串
@return ：成功返回加密后的字符串， 否则返回None
'''
def md5_encryption(string):
    m = hashlib.md5()
    if string:
        m.update(string)
        psw = m.hexdigest()
        return psw
    return None

'''
 加载分析上下文，将mapping_raw 生成一个字典 
 @param mapping_raw: mapping 文本,一个字符串
 @return ：返回一个字典
'''
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
        logger.error("retrace_data.py file call function get_file_path error")
        return None
    res = mkdir(path)#根据路径创建文件
    if res:#创建文件成功
        return path
    return None

'''
 加载分析上下文，将mapping_raw 生成一个字典
 @param mapping_raw: mapping 文本,一个字符串
 @return ：返回一个字典
'''
def load_mapping(mapping_raw):#将mapping一次性读取
    lis_a = mapping_raw.split("\n")
    dic_t = {}  # 字典保存结果
    retrace_class = ""
    proguard_class = ""

    length = len(lis_a)
    for i in range(0, length):
        line = lis_a[i]
        line = line.rstrip("\n")
        line = line.strip()
        if len(line) == 0:
            continue
        if line.endswith(":"):  # 找到新类型开始的行
            lis_t = line.split("->")
            retrace_class = lis_t[0]  # 保原始的类名
            retrace_class = retrace_class.strip()
            proguard_class = lis_t[1]  # 保原混淆后的类名
            proguard_class = re.findall("\w*.*:", proguard_class)
            proguard_class = proguard_class[0].replace(":", "")
            proguard_class = proguard_class.strip()
            dict_new = {proguard_class: retrace_class}
            dic_t.update(dict_new)
        else:
            if ("(" in line) and ")" in line:  # 函数类型
                lis_t = line.split("->")
                str_lis = re.findall(' .*\(', lis_t[0])
                str_l = str_lis[0]
                str_l = str_l.replace('(', '')
                str_l = str_l.strip()
                lis_l = str_l.split(" ")
                retracefunc_name = lis_l[len(lis_l) - 1]
                retracefunc_name = retracefunc_name.strip()  # 原函数名
                proguardfunc_name = lis_t[1].strip()  # 混淆后的函数名
                rfunc_name = retrace_class + "." + retracefunc_name  # 原始类名加原始函数名 作为value
                pfunc_name = proguard_class + "." + proguardfunc_name  # 混淆的类名加混淆的函数名 作为key
                if pfunc_name in dic_t:  # 已经存在 key
                    value = dic_t.get(pfunc_name)  # 取出其中对应的value
                    if value.endswith(")"):  # 多匹配的情况
                        rfunc_name = value.replace(")", " | " + retracefunc_name + ")")
                    else:  # 只有一个匹配
                        rfunc_name = value + "(" + retracefunc_name + ")"
                dict_new = {pfunc_name: rfunc_name}
                dic_t.update(dict_new)
            else:
                continue
    return dic_t

'''
存储字典到文件
@:param   dict_l   load_mapping 返回的字典
@:param   path      将要存储的目录
'''
def storage_dict(dict_l,path):
    file_path = path + "mapping.dict"
    fp = open(file_path, "w")
    string = json.dumps(dict_l)
    fp.write(string)
    fp.close()

'''
从指定位置读取字典
@:param   path      mapping.dict 存放的目录
@:return  返回一个字典
'''
def get_dict(path):
    file_path = path + "mapping.dict"
    with open(file_path) as fp:
        string = fp.read()
    return ast.literal_eval(string)

'''
从指定位置查找文件
@:param   filename      文件路径
@:return  True 找到文件， 否则文件不存在
'''
def find_file(filename):#到指定目录查找
    filename = filename.strip()
    FileExists = os.path.exists(filename)
    if FileExists:
        return True
    else:
        return False

'''
获取请求数据
@:param   request    一个request  
@:return  有数据则返回，否则返回None
'''
def getdata(request):#获取post数据
    try:
        data = request.body
    except:
        return None
    try:  # 将字符串转化为字典
        data = json.loads(data)
        data = eval(data)
        return data
    except:
        return None

'''
将data数据转化成字典格式，并从中获取key 值对应的value
@:param   data    getdata函数返回的数据
@:param   key     需要获取的值对应的key
@:return  成功则返回value，否则返回None
'''
def split_data(data, key):#根据key获取数据
    if type(data) is types.DictionaryType:
        if key in data:
            value = data.get(key, None)
        else:
            return None
        return value


def data_process(request, dictr):#获取数据段
    data = getdata(request)
    if data is None:#数据段是否为空
        dict1 = {'result': 'fail', 'stacks': data, 'reason': 'data is empty'}
        dictr.update(dict1)
        logger.error("retrace_data.py file call function data_process error %s",
                     "not have data or data is empty")
        return None
    else:#数据段不为空时执行获取stacks数据
        return data

'''
获取stacks 数据段
@:param   data    getdata函数返回的数据
@:param   dictr   保存失败信息
@:return  成功则返回stack数据，否则返回None
'''
def get_stacks_data(data, dictr):#提取stacks数据段
    stack = split_data(data, 'stacks')#获取stacks段
    if stack:
        return stack
    else:
        dict1 = {'result': 'fail', 'stacks': None, 'reason': 'stacks is not exist'}
        dictr.update(dict1)
        return None

'''
分析原始stack数据，提取匹配规则
@:param  rawstack   原始stack数据
@return 成功返回匹配规则，否则返回None
'''
def get_rules(rawstack):
    dic_t = {}
    stack = re.findall(r'\w*\.\w*\..*', rawstack)
    if stack:  # 第一次提取匹配字符串成功
        stack = stack[0]
        if ('(' in stack) and (')' in stack):  # 含有()的类型
            str_rule = re.findall(r'^(.+?)\(', stack)
            if str_rule:  # 第二次提取待匹配字符串成功
                return str_rule[0]
            else:  # stacks无效
                return None
        else:
            return stack
    else:  # stacks无效
        return None

'''	
分析一行堆栈数据
@param line: 待分析的一条堆栈数据
@param dict_l：load_mapping  返回的 字典
#@return   成功返回被回溯的line, 否则返回原始数据 line
'''
def deobfuscate(dict_l, line):
    key = get_rules(line)#获取匹配规则
    result = ""
    try:
        result = dict_l.get(key)#获取回溯值
    except:
        return line
    if result is None:
        return line
    line = line.replace(key, result)#将混淆值替换为回溯值
    return line



def search(path,stacks):
    file_path_dict = path+"mapping.dict"
    file_path_mapp = path + MAPPING_FILENAME
    res = find_file(file_path_dict)
    list_result = []
    dict_l = {}
    if res is False:#指定路径下没有mapping.dict文件
        with open(file_path_mapp) as fp:
            dict_l = load_mapping(fp.read())
        storage_dict(dict_l, path)#存储mapping.dict 文件下次直接加载
    mapp_dict = get_dict(path)#获取mapping.dict里面的内容
    if type(stacks) is types.StringType:#只有一条stack数据 是字符串
        result = deobfuscate(mapp_dict, stacks)#获取反混淆的内容
        return result
    else:#stacks是一个列表
        for stack in stacks:
            result = deobfuscate(mapp_dict, stack)  # 获取反混淆的内容
            list_result.append(result)
        return list_result


'''	
处理一条request
@param   request   一个request
#@return           返回查找结果
'''
def Request(request):#处理请求
    dic_tr = {}
    mapping_selector = {}
    data = data_process(request, dic_tr)  # 获取data数据
    if data is None:  # data 为空
        dictjson = json.dumps(dic_tr)
        return dictjson
    stacks = get_stacks_data(data, dic_tr)  #获取stacks数据段
    if stacks is None:
        dictjson = json.dumps(dic_tr)
        return dictjson
    path = get_file_path(data, mapping_selector)  # 获取文件所在目录,和 mapping文件信息
    if path is None:
        dic_t = {'result': 'fail', 'stacks': stacks, 'reason': 'No search directory or create directory fail'}
        dictjson = json.dumps(dic_t)
        return dictjson
    file_path = path + MAPPING_FILENAME#指定文件路径
    res = find_file(file_path)  # 指定路径下查找 mapping.txt文件
    if res is False:  # 在指定路径下找不到mapping.txt
        # 根据mapping信息从金山云上获取mapping.txt,保存到path路径下
        res_ks3 = get_mapping_from_ks3(path, mapping_selector)
        if res_ks3 is None:  # 从金山云获取数据失败
            dic_t = {'result': 'fail', 'stacks': stacks, 'reason': 'request ks3 fail'}
            dictjson = json.dumps(dic_t)
            return dictjson

    result = search(path, stacks)
    dic_t = {'result': 'successful', 'stacks': result}
    dictjson = json.dumps(dic_t)
    return dictjson

'''	
从金山云上获取mapping压缩数据，加压后保存在指定目录下，保存为 mapping.txt
@param     path    文件保存的路径
@:param    mapping_selector   一个字典，包含mapping.txt 对应的version，appkey，package
#@return      成功返回文件保存的目录，否则返回None
'''
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

'''
把从金山云获取的mapping压缩文件解压为mapping.txt
@:param     gzfile    要解压的文件路径
@:param     dst       解压结果保存的文件路径  
'''
def gunzipfile(gzfile, dst):
    fin = gzip.open(gzfile, 'rb')
    fout = open(dst, 'wb')
    in_out(fin, fout)

'''
把mapping解压的内容写入文件
@:param     fin    解压结果
@:param     fout   要保存的文件 
'''
def in_out(fin, fout):
    BufSize = 1024 * 8
    while True:
        buf = fin.read(BufSize)
        if len(buf) < 1:
            break
        fout.write(buf)
    fin.close()
    fout.close()
