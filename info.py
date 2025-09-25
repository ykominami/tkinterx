from pathlib import Path
from typing import Any, Dict, List, Union
from jsonfilemanager import JSONFileManager

class Info:
  def __init__(self, path = "info.json"):
    self.path = Path(path)
    self.json_manager = JSONFileManager(self.path)
    self.info = {}
    self.formats = []
    self.patterns = []

  def load_info(self):
    content = self.load_info_json_file_1()
    print(f"App:load_info:content: {content}")

    # 使用例：文字列配列を渡してアプリを起動
    self.formats = content["format"]
    self.patterns = content["pattern"]

  def load_info_json_file(self, data: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
    """
    JSONファイルを読み込み、データが存在しない場合は新しいデータを書き込む
    
    Args:
        data: 書き込むデータ（ファイルが存在しない場合）
        
    Returns:
        読み込んだデータまたは書き込んだデータ
    """
    content = self.json_manager.read()
    print(f"content: {content}")

    if not content:
      # ファイルが存在しないか空の場合、新しいデータを書き込む
      if self.json_manager.write(data):
        return data
      else:
        print("データの書き込みに失敗しました")
        return None
    else:
      # 既存のデータを返す
      return content

  def load_info_json_file_1(self) -> Union[Dict, List, Any]:
    """
    デフォルトのデータリストを読み込みまたは作成する
    
    Returns:
        読み込んだデータまたは作成したデータ
    """
    data = {
      "pattern": [
        "OpenAI-Cursor",
        "web_api_s",
        "web_api_2",
        "web_api_list",
        "pc_config",
        "planning"
      ],
      "format": [
        "get",
        "post_json",
        "post_form",
      ]
    }

    return self.load_info_json_file(data)

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