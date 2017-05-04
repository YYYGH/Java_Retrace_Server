#coding:utf-8
import sys
sys.path.append("../")
from kpserver.views import *
from kpserver.configure import *
import unittest


if __name__ == '__main__':
    mapping = """
        android.support.v7.view.menu.ExpandedMenuView -> android.support.v7.view.menu.ExpandedMenuView:
        int[] TINT_ATTRS -> a
        android.support.v7.view.menu.MenuBuilder mMenu -> b
        int mAnimations -> c
        void <init>(android.content.Context,android.util.AttributeSet) -> <init>
        void <init>(android.content.Context,android.util.AttributeSet,int) -> <init>
        void initialize(android.support.v7.view.menu.MenuBuilder) -> a
        void onDetachedFromWindow() -> onDetachedFromWindow
        boolean invokeItem(android.support.v7.view.menu.MenuItemImpl) -> a
        void onItemClick(android.widget.AdapterView,android.view.View,int,long) -> onItemClick
        int getWindowAnimations() -> getWindowAnimations
        void <clinit>() -> <clinit>
        android.support.v4.app.FragmentManagerImpl$AnimateOnHWLayerIfNeededListener$1 -> android.support.v4.a.q$a$1:
        android.support.v4.app.FragmentManagerImpl$AnimateOnHWLayerIfNeededListener this$0 -> a
        void <init>(android.support.v4.app.FragmentManagerImpl$AnimateOnHWLayerIfNeededListener) -> <init>
        void run() -> run
        android.support.v4.app.FragmentManagerImpl$AnimateOnHWLayerIfNeededListener$2 -> android.support.v4.a.q$a$2:
        android.support.v4.app.FragmentManagerImpl$AnimateOnHWLayerIfNeededListener this$0 -> a
        void <init>(android.support.v4.app.FragmentManagerImpl$AnimateOnHWLayerIfNeededListener) -> <init>
        void run() -> run
        android.support.v4.app.FragmentManagerImpl$FragmentTag -> android.support.v4.a.q$b:
        int[] Fragment -> a
        void <clinit>() -> <clinit>
    """

    data = {
        'appkey': 'deadbeef', 'version': '0.0.1',
        'stacks': [
            '03-30 14:37:24.107  1258  1258 E AndroidRuntime: FATAL EXCEPTION: main',
            '03-30 14:37:24.107  1258  1258 E AndroidRuntime: Process: chencanmao.ndkprofiler1, PID: 1258',
            '03-30 14:37:24.107  1258  1258 E AndroidRuntime: java.lang.RuntimeException: he ate a table yesterday.',
            '03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at chencanmao.ndkprofiler1.Pong.Action(Unknown Source)',
            '03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at chencanmao.ndkprofiler1.Pong.d(Unknown Source)',
            '03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at chencanmao.ndkprofiler1.MainActivity$1.onClick(Unknown Source)',
            '03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at android.view.View.performClick(View.java:5207)',
            '03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at android.view.View$PerformClick.run(View.java:21177)', '03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at android.os.Handler.handleCallback(Handler.java:739)',
            '03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at android.os.Handler.dispatchMessage(Handler.java:95)',
            '03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at android.os.Looper.loop(Looper.java:148)',
            '03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at android.app.ActivityThread.main(ActivityThread.java:5458)',
            '03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at java.lang.reflect.Method.invoke(Native Method)',
            '03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:738)',
            '03-30 14:37:24.107  1258  1258 E AndroidRuntime:        at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:628)',
            '03-30 14:37:39.553  3291  3291 E AndroidRuntime:        at com.xsj.crasheye.NetSender.a(Unknown Source)',
            '03-30 14:37:39.553  3291  3291 E AndroidRuntime:        at com.xsj.crasheye.n.a(Unknown Source)',
            '03-30 14:37:39.553  3291  3291 E AndroidRuntime:        at com.xsj.crasheye.n$1.a(Unknown Source)'],
            'package': 'chencanmao.ndkprofiler1'}

    mapp_ctx_global = {}
    class TestDeobfuscate(unittest.TestCase):
        def setUp(self):
            self.ctx = load_mapping(mapping)
            mapping_selector = {}
            path = get_file_path(data, mapping_selector)
            mappingtxt_path = path + MAPPING_FILENAME
            mappingdict_path = path + "mapping.dict"
            res = find_file(mappingdict_path)
            if res:#没找到
                with open(mappingtxt_path) as fp:
                    self.mapp_ctx = load_mapping(fp.read())
                    mapp_ctx_global.update(self.mapp_ctx)
            else:
                self.mapp_ctx = get_dict(path)
                mapp_ctx_global.update(self.mapp_ctx)

        def testShouldNoMatch(self):
            result = deobfuscate(self.ctx, "android.support.v4.a.q$a$2.run")
            self.assertEqual("android.support.v4.app.FragmentManagerImpl$AnimateOnHWLayerIfNeededListener$2.run", result)

        def testShouldMoreMatch(self):
            result = deobfuscate(self.ctx, "android.support.v7.view.menu.ExpandedMenuView.a")
            self.assertEqual("android.support.v7.view.menu.ExpandedMenuView.initialize(invokeItem)", result)

        def testShouldDeobfuscate(self):
            result = deobfuscate(self.ctx, "android.support.v4.a.q$a$2.<init>")
            self.assertEqual("android.support.v4.app.FragmentManagerImpl$AnimateOnHWLayerIfNeededListener$2.<init>", result)

        def testShouldRemainIntact(self):
            result = deobfuscate(self.ctx, "android.support.v7.view.menu.Hello.ExpandedMenuView")
            self.assertEqual("android.support.v7.view.menu.Hello.ExpandedMenuView", result)

        def testNoMatchMappingFile(self):
            result = deobfuscate(self.mapp_ctx, "android.support.v4.a.q$a$2.run")
            self.assertEqual("android.support.v4.app.FragmentManagerImpl$AnimateOnHWLayerIfNeededListener$2.run", result)

        def testMatchMappingFile(self):
            result = deobfuscate(self.mapp_ctx, "android.support.v4.a.q$a$2.<init>")
            self.assertEqual("android.support.v4.app.FragmentManagerImpl$AnimateOnHWLayerIfNeededListener$2.<init>",result)

import cProfile

cProfile.run('''for i in range(1000):deobfuscate(mapp_ctx_global, 
                "android.support.v4.a.q$a$2.<init>")''')
cProfile.run('''for i in range(1000):deobfuscate(mapp_ctx_global, 
            "android.support.v7.view.menu.Hello.ExpandedMenuView")''')
unittest.main()