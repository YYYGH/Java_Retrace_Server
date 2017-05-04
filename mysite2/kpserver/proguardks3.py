#coding: utf8
#author: lijianjun

import requests
import traceback
import md5
from ks3.connection import Connection
  
class Conn:
  def __init__(self, ak, sk, host, bucket):
    self.bucket = bucket
    self.ksyun = Connection(ak, sk, host=host)
    if not self._exist(bucket):
      self.ksyun.create_bucket(bucket)
    assert self._exist(bucket)
  
  def _exist(self, bucket):
    buckets = [b.name for b in self.ksyun.get_all_buckets()]
    return bucket in buckets

  def upload(self, keyname, filename):
    try:
      bucket = self.ksyun.get_bucket(self.bucket)
      key_object = bucket.new_key(keyname)
      key_object.set_contents_from_filename(filename)
      return {"result": 0, "msg": keyname}
    except:
      return {"result": -1, "msg": traceback.format_exc()}
      pass
  
  def download(self, filename, keyname):
    try:
      bucket = self.ksyun.get_bucket(self.bucket)
      key_object = bucket.get_key(keyname)
      key_object.get_contents_to_filename(filename)
      return {"result": 0, "msg": filename}
    except:
      return {"result": -1, "msg": traceback.format_exc()}
      pass
  
  def make_key(self, app_key, version, package_name):
    return ''.join([
      app_key,
      md5.new(version).hexdigest(),
      md5.new(package_name).hexdigest()
    ]).lower()

if __name__ == '__main__':
  import unittest
  import os
  class TestKs3Yun(unittest.TestCase):
    def setUp(self):
      KS3 ={
         "AK": "***********************",
         "SK": "****************************",
         "PROGUARD_BUCKET_NAME": "*********************"
      }
      self.mapping_selector = {
        "version": '0.0.1',
        "package_name": 'chencanmao.ndkprofiler1',
        "app_key": 'deadbeef'
      }
      self.file_name = "mapping.txt.gz"
      assert os.path.isfile(self.file_name)
      self.c = Conn(KS3["AK"], KS3["SK"], "kss.ksyun.com", KS3['PROGUARD_BUCKET_NAME'])
      
    def test_key(self):
      print self.c.make_key(**self.mapping_selector)
      
    def test_upload(self):
      ret = self.c.upload(self.c.make_key(**self.mapping_selector), self.file_name)
      self.assertEqual(ret['result'], 0)
      
    def test_download(self):
      ret = self.c.download('tmp.gz', self.c.make_key(**self.mapping_selector))
      self.assertEqual(ret['result'], 0)
      
    def test_download_not_exist(self):
      ret = self.c.download('tmp.gz', self.c.make_key(**self.mapping_selector) + 'no')
      self.assertEqual(ret['result'], -1)
      self.assertTrue(ret['msg'])

  unittest.main()