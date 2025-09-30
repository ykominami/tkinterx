from pathlib import Path
from typing import Any, Dict, List, Union
from jsonfilemanager import JSONFileManager

class Info:
  def __init__(self, path = "info.json"):
    self.path = Path(path)
    # If file missing or empty (0 bytes or only whitespace), recreate it
    if not self.path.exists() or self.path.stat().st_size == 0:
      # attempt to remake the file; if remake succeeds, JSONFileManager will be
      # recreated below with the updated path
      self.remake(str(self.path))

    else:
      # If file exists but contains only whitespace, remake as well
      try:
        with self.path.open("r", encoding="utf-8") as f:
          content = f.read()
        if content.strip() == "":
          self.remake(str(self.path))
      except Exception:
        # If any error reading the file, attempt to remake
        self.remake(str(self.path))

    self.json_manager = JSONFileManager(self.path)
    self.info = {}
    self.formats = []
    self.patterns = []

  def load_info(self):
    content = self.load_info_json_file()
    # print(f"App:load_info:content: {content}")

    # 使用例：文字列配列を渡してアプリを起動
    self.formats = content["format"]
    self.patterns = content["pattern"]

  def load_info_json_file(self):
    """
    JSONファイルを読み込み、データが存在しない場合は新しいデータを書き込む
    
    Args:
        無し
        
    Returns:
        読み込んだデータ
    """
    content = self.json_manager.read()

    return content

  def remake(self, path: str) -> bool:
    """
    指定したパスに既定の連想配列を持つ JSON ファイルを作成する。

    Args:
      path: 作成する JSON ファイルのパス（文字列）

    Returns:
      書き込みに成功したら True、失敗したら False
    """
    target_path = Path(path)
    manager = JSONFileManager(target_path)
    default_data = {
      "pattern": [],
      "format": []
    }

    success = manager.write(default_data)
    if success:
      # 更新されたファイルパスを反映して内部状態をリセット
      self.path = target_path
      self.json_manager = manager
      self.info = default_data
      self.formats = []
      self.patterns = []

    return success