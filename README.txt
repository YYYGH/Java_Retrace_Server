1.WorkĿ¼�´��mapping.txt�ļ����ļ�����Ŀ¼�Ǹ��� appkey,version��Md5���ܣ�,package��Md5���ܣ����ɵ�
2.����mysite2/kpserverĿ¼�޸� configure.py �����ļ��е� 
KS3_K = {
    "AK": "�˴��������ӽ�ɽ�Ƶ�AK",
    "SK": "�˴��������ӽ�ɽ�Ƶ�SK",
    "PROGUARD_BUCKET_NAME": "�˴�����Bucket"
}
3.������������ ����mysite2Ŀ¼�£����ն���ִ�У� Python manage.py runserver ���� Python manage.py runserver IP:post ,
  ����ָ��ip�Ͷ˿ں�ʱĬ��Ϊ127.0.0.1:8000
4.mysite/KpserverTestĿ¼�µ�kpserverTest.py���ڶԳ���Ĳ���
5.Client.py �ļ��Ƿ��ʷ������Ŀͻ����ļ� 
	���ݶθ�ʽ payload = {'appkey': '***', 'version': '****', 'package': '****', 'stacks': "***********************"}
	����appkey,version,pakcage,����key�������ǹ̶�ֵ
	js = json.dumps(payload)#�����ݶ�תΪjson
     	r= requests.post('http://10.20.126.19:8000/index/',json = js)#���ӷ�����
	print 'r.txt: ', r.text #������������ص�����