#coding:utf-8
import httplib 
import urllib
import sys
import requests
import json

def data():
	#conn = httplib.HTTPConnection("127.0.0.1:8000")   #请求http服务器，这里的ip.ip.ip.ip要换成服务器端所在ip  
	#print "requesting..." 
	#params = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
	list = []
	#payload = {'appkey': 'deasdfsdbeef', 'version': '0.0.fsdafs1', 'packafsage': 'chencafsdanmao.ndkprofiler1', 'stacks': "03-30 14:37:24.107  1258  1258 E AndroidRuntime: FATAL EXCEPTION: main"}
	#list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': "03-31 14:37:24.107  1258  1258 E AndroidRuntime: FATAL EXCEPTION: main"}
	list.append(payload)
	
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': "android.support.a.a.b.a(1)"}
	list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': "android.support.a.a.b.a"}
	list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1',
	'stacks': [
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime: FATAL EXCEPTION: main",
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime: Process: chencanmao.ndkprofiler1, PID: 1258",
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime: java.lang.RuntimeException: he ate a table yesterday.",
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at chencanmao.ndkprofiler1.Pong.Action(Unknown Source)",
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at chencanmao.ndkprofiler1.Pong.d(Unknown Source)",
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at chencanmao.ndkprofiler1.MainActivity$1.onClick(Unknown Source)",
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at android.view.View.performClick(View.java:5207)",
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at android.view.View$PerformClick.run(View.java:21177)",
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at android.os.Handler.handleCallback(Handler.java:739)",
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at android.os.Handler.dispatchMessage(Handler.java:95)",
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at android.os.Looper.loop(Looper.java:148)",
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at android.app.ActivityThread.main(ActivityThread.java:5458)",
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at java.lang.reflect.Method.invoke(Native Method)",
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:738)",
	"03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:628)",
	"03-30 14:37:39.553  3291  3291 E AndroidRuntime:        at com.xsj.crasheye.NetSender.a(Unknown Source)",
	"03-30 14:37:39.553  3291  3291 E AndroidRuntime:        at com.xsj.crasheye.n.a(Unknown Source)",
	"03-30 14:37:39.553  3291  3291 E AndroidRuntime:        at com.xsj.crasheye.n$1.a(Unknown Source)"
	]}
	list.append(payload)

	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': "03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at android.os.Looper.loop(Looper.java:148)"}
	list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': "03-30 14:37:39.553  3291  3291 E AndroidRuntime:        at chencanmao.ndkprofiler1.Pong.c(Unknown Source)"}
	list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': "03-30 14:37:39.553  3291  3291 E AndroidRuntime:        at com.xsj.crasheye.NetSender.a(Unknown Source)"}
	list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': "com.xsj.crasheye.n$1.a(Unknown Source)"}
	list.append(payload)
	
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': "AndroidRuntime:        at chencanmao.ndkprofiler1.Pong.c(Unknown Source)"}
	list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': ":        at chencanmao.ndkprofiler1.Pong.c(Unknown Source)"}
	list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': "        at chencanmao.ndkprofiler1.Pong.c(Unknown Source)"}
	list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': "at chencanmao.ndkprofiler1.Pong.c(Unknown Source)"}
	list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': "chencanmao.ndkprofiler1.Pong.c"}
	list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': "chencanmao.ndkprofiler1.Pong.c(Unknown Source)"}
	list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': "c(Unknown Source)"}
	list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': ".c(Unknown Source)"}
	list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': "c"}
	list.append(payload)
	payload = {'appkey': 'deadbeef', 'version': '0.0.1', 'package': 'chencanmao.ndkprofiler1', 'stacks': ".Pong.c(Unknown Source)"}
	list.append(payload)
	
	for val in list:
	
		js = json.dumps(val)
		
		r3 =requests.post('http://20.20.126.19:8000/index/',json = js)
		print "******************************************************************\n"
		print 'r3.txt: ', r3.text
		
	print "________________________________________________________________________________________________________________________________\n"	


def main():
	data()
	
main()