import sys
import timeit

sys.path.append('../')
from kpserver.retrace_data import *
from kpserver.views import *
from kpserver.configure import *
import unittest
from ttk import Widget


class kpserverTestCase(unittest.TestCase):
    def setUp(self):
        self.data = ''

    def tearDown(self):
        self.payload = None


class FunctionCallSuccessfulTest(kpserverTestCase):
    def runTest(self):
        mapping_selector = {}
        data = '''{"appkey": "deadbeef", "version": "0.0.1",
                    "stacks": ["03-30 14:37:24.107  1258  1258 E AndroidRuntime: FATAL EXCEPTION: main", 
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
                    "03-30 14:37:39.553  3291  3291 E AndroidRuntime:        at com.xsj.crasheye.NetSender.a(Unknown Source)"],
                    "package": "chencanmao.ndkprofiler1"}'''
        path = get_file_path(data, mapping_selector)
        #print 'path : ', path
        self.assertIsNotNone(path, 'path is None')
        file_path = path + MAPPING_FILENAME
        all_content = load_mapping(file_path)
        #print 'path : ', file_path
        #print 'all_content: ', all_content
        self.assertIsNotNone(all_content, 'all_content is exits')
        try:
            data1 = ast.literal_eval(data)
        except:
            data1 = None

        self.assertIsNotNone(data1, " data1 is None")
        rules = get_rules(data1['stacks'])
        self.assertIsNotNone(rules, 'rules is None')
        self.assertNotEqual(0, len(rules), 'rules unvalue')
        # print 'all_content: ', all_content
        # print 'rules: ', rules
        # print 'type rules: ', type(rules)
        result = match_string(all_content, rules)

        self.assertIsNotNone(result, 'result is None')
        res = arrange_result(result)
        self.assertIsNotNone(res, 'res is None')


def time_Test_init():
    mapping_selector = {}

    data = '''{"appkey": "deadbeef", "version": "0.0.1", 
                "stacks": ["03-30 14:37:24.107  1258  1258 E AndroidRuntime: FATAL EXCEPTION: main",
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
                        "03-30 14:37:39.553  3291  3291 E AndroidRuntime:        at com.xsj.crasheye.NetSender.a(Unknown Source)"], 
                "package": "chencanmao.ndkprofiler1"}'''
    path = get_file_path(data, mapping_selector)
    file_path = path + MAPPING_FILENAME
    #print "**************************************\n"
    #print 'file_path: ', file_path
    all_content = load_mapping(file_path)
    #print 'all_content:', all_content
    data1 = ast.literal_eval(data)
    rules = get_rules(data1['stacks'])
    list1 = [all_content, rules]
    return list1


def time_test(all_content, rules):
    #print 'all_content', all_content
    content = list(all_content)
    lrules = list(rules)
    result = match_string(content, lrules)


if __name__ == '__main__':
    res = time_Test_init()
    #print 'res: ', res
    #print 'res[0]: ', res[0]
    all_text = res[0]
    rules = res[1]
    #print 'text: ', all_text
    #print 'rules: ', rules
    Time_test = 'time_test(' + str(all_text) + ',' + str(rules) + ')'
    print timeit.timeit(Time_test, 'from __main__ import time_test', number=1)
    unittest.main()

