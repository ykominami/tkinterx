from pathlib import Path
from typing import Any, Dict, List, Union
from jsonfilemanager import JSONFileManager
import os
import json

class Info:
  def __init__(self, format_path = "info3.json", params_path = "params_map.json"):
    self.formats_jsfm = None
    self.params_jsfm = None
    self.patterns = None
    self.formats = None
    self.params_map = None

    self.format_jsfm = JSONFileManager(format_path)
    content = self.format_jsfm.load()
    # print(f"App:load_info:content: {content}")

    if content is not None:
    # 使用例：文字列配列を渡してアプリを起動
      self.formats = content["format"]

      self.params_jsfm = JSONFileManager(params_path)
      self.params_map = self.params_jsfm.load()
      self.patterns = self.get_keys()

  def get_keys(self):
    return self.params_jsfm.get_keys()

