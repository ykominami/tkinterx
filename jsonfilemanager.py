import json
import os
from typing import Any, Dict, List, Optional, Union
from pathlib import Path


class JSONFileManager:
    """
    JSONファイルの読み書きを行うクラス
    
    機能:
    - JSONファイルの読み込み
    - JSONファイルへの書き込み
    - ファイルの存在確認
    - バックアップ作成
    - エラーハンドリング
    """
    
    def __init__(self, file_path: Union[str, Path]):
        """
        JSONFileManagerの初期化
        
        Args:
            file_path: JSONファイルのパス
        """
        self.file_path = Path(file_path)
        self.encoding = 'utf-8'
        self.file = None
    
    def read(self) -> Optional[Union[Dict, List, Any]]:
        """
        JSONファイルを読み込む
        
        Returns:
            読み込んだJSONデータ（辞書、リスト、その他）
            ファイルが存在しない場合やエラー時はNone
        """
        try:
            if not self.file_path.exists():
                print(f"ファイルが存在しません: {self.file_path}")
                return None
            
            with open(self.file_path, 'r', encoding=self.encoding) as file:
                data = json.load(file)
                print(f"JSONファイルを読み込みました: {self.file_path}")
                return data
                
        except json.JSONDecodeError as e:
            print(f"JSONの解析エラー: {e}")
            return None
        except PermissionError as e:
            print(f"ファイルアクセス権限エラー: {e}")
            return None
        except Exception as e:
            print(f"ファイル読み込みエラー: {e}")
            return None
    
    def write(self, data: Union[Dict, List, Any], create_backup: bool = True) -> bool:
        """
        JSONファイルに書き込む
        
        Args:
            data: 書き込むデータ
            create_backup: 既存ファイルのバックアップを作成するかどうか
            
        Returns:
            書き込み成功時True、失敗時False
        """
        try:
            # ディレクトリが存在しない場合は作成
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # バックアップ作成
            if create_backup and self.file_path.exists():
                self._create_backup()
            
            # 一時ファイルに書き込み（アトミックな書き込み）
            temp_path = self.file_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding=self.encoding) as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            
            # 一時ファイルを本ファイルに移動
            temp_path.replace(self.file_path)
            
            print(f"JSONファイルに書き込みました: {self.file_path}")
            return True
            
        except PermissionError as e:
            print(f"ファイル書き込み権限エラー: {e}")
            return False
        except OSError as e:
            print(f"ファイルシステムエラー: {e}")
            return False
        except Exception as e:
            print(f"ファイル書き込みエラー: {e}")
            return False
        finally:
            # 一時ファイルを削除
            if 'temp_path' in locals() and temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception:
                    pass  # 一時ファイル削除の失敗は無視
    
    def _create_backup(self) -> None:
        """
        既存ファイルのバックアップを作成
        
        Raises:
            Exception: バックアップ作成に失敗した場合
        """
        try:
            backup_path = self.file_path.with_suffix('.bak')
            self.file_path.rename(backup_path)
            print(f"バックアップを作成しました: {backup_path}")
        except PermissionError as e:
            print(f"バックアップ作成権限エラー: {e}")
            raise
        except OSError as e:
            print(f"バックアップ作成ファイルシステムエラー: {e}")
            raise
        except Exception as e:
            print(f"バックアップ作成エラー: {e}")
            raise
    
    def exists(self) -> bool:
        """
        ファイルが存在するかチェック
        
        Returns:
            ファイルが存在する場合True、存在しない場合False
        """
        return self.file_path.exists()
    
    def get_file_info(self) -> Dict[str, Any]:
        """
        ファイル情報を取得
        
        Returns:
            ファイル情報を含む辞書
            - exists: ファイルの存在有無
            - path: ファイルパス（存在する場合）
            - size: ファイルサイズ（存在する場合）
            - modified: 最終更新日時（存在する場合）
            - is_file: ファイルかどうか（存在する場合）
        """
        if not self.exists():
            return {"exists": False}
        
        try:
            stat = self.file_path.stat()
            return {
                "exists": True,
                "path": str(self.file_path),
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "is_file": self.file_path.is_file()
            }
        except OSError as e:
            print(f"ファイル情報取得エラー: {e}")
            return {"exists": False, "error": str(e)}
    
    def delete(self) -> bool:
        """
        ファイルを削除
        
        Returns:
            削除成功時True、失敗時またはファイルが存在しない場合False
        """
        try:
            if self.exists():
                self.file_path.unlink()
                print(f"ファイルを削除しました: {self.file_path}")
                return True
            else:
                print(f"ファイルが存在しません: {self.file_path}")
                return False
        except PermissionError as e:
            print(f"ファイル削除権限エラー: {e}")
            return False
        except OSError as e:
            print(f"ファイル削除ファイルシステムエラー: {e}")
            return False
        except Exception as e:
            print(f"ファイル削除エラー: {e}")
            return False



