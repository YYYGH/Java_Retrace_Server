1.Work目录下存放mapping.txt文件，文件所在目录是根据 appkey,version（Md5加密）,package（Md5加密）生成的
2.进入mysite2/kpserver目录修改 configure.py 配置文件中的 
KS3_K = {
    "AK": "此处填入连接金山云的AK",
    "SK": "此处填入连接金山云的SK",
    "PROGUARD_BUCKET_NAME": "此处填入Bucket"
}
3.启动服务器： 进入mysite2目录下，在终端下执行： Python manage.py runserver 或者 Python manage.py runserver IP:post ,
  当不指定ip和端口号时默认为127.0.0.1:8000
4.mysite/KpserverTest目录下的kpserverTest.py用于对程序的测试
5.Client.py 文件是访问服务器的客户端文件 
	数据段格式 payload = {'appkey': '***', 'version': '****', 'package': '****', 'stacks': "***********************"}
	其中appkey,version,pakcage,三个key的名称是固定值
	js = json.dumps(payload)#将数据段转为json
     	r= requests.post('http://10.20.126.19:8000/index/',json = js)#连接服务器
	print 'r.txt: ', r.text #输出服务器返回的数据