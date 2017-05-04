#coding=utf-8
import os
MAPPING_FILENAME = 'mapping.txt'#对照表文件名
GZIP_MAPPING_FILENAME = 'mapping.txt.gz'#指定保存下载的数据的文件名
APP_PATH = os.path.split(__file__)[0]
ROOT_PATH = os.path.split(APP_PATH)[0]
WORK_PATH = ROOT_PATH + '/Work/'#指定工作根目录
LOGGING_NAME = ROOT_PATH + 'kpserver.log'

KS3_K = {
    "AK": "LZGEzlI8FzeVLM+Dxam9",
    "SK": "hySg7p4D/epwsp9vJmiuPG+IE54g7EtKiRWs3kFa",
    "PROGUARD_BUCKET_NAME": "crasheye-proguard"
}
