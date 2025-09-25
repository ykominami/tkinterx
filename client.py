import requests
import json
import urllib.parse

from info import Info

class Client:
    """
    HTTPリクエストを送信するためのクライアントクラス
    """
    
    def __init__(self, formats: [str], patterns: [str]):
        self.formats = formats
        self.patterns = patterns
        self.selected_pattern = None
        self.selected_format = None
        #self.url = "https://script.google.com/macros/s/AKfycbyVI7e9uZ9c7BDWXDd2-272hX2MefjUyJkzHsahYpAINn3-PPYnhKO4LcpvK9uxrIsq/exec"
        # self.url = "https://script.google.com/macros/s/AKfycbwFir48x3T1B9fY3aHGaMYpO96fxFsvTqDusbxe6FB92Htrj4xdO3ZccP_YscAdcAJt/exec" 
        self.url = "https://script.google.com/macros/s/AKfycbwFir48x3T1B9fY3aHGaMYpO96fxFsvTqDusbxe6FB92Htrj4xdO3ZccP_YscAdcAJt/exec"
    
    def object_to_url_encoded(self, obj):
        """
        JavaScriptのオブジェクトをURLエンコーディング形式の文字列に変換する関数
        
        Args:
            obj (dict): 変換するオブジェクト（辞書）
        
        Returns:
            str: URLエンコーディングされた文字列
        
        Example:
            >>> obj = {"name": "John Doe", "age": 30, "city": "New York"}
            >>> result = object_to_url_encoded(obj)
            >>> print(result)
            name=John%20Doe&age=30&city=New%20York
        """
        try:
            # 辞書の各キーと値をURLエンコード形式に変換
            encoded_pairs = []
            
            for key, value in obj.items():
                # キーと値をURLエンコード
                encoded_key = urllib.parse.quote(str(key), safe='')
                encoded_value = urllib.parse.quote(str(value), safe='')
                
                # key=value の形式で追加
                encoded_pairs.append(f"{encoded_key}={encoded_value}")
            
            # すべてのペアを & で結合
            result = "&".join(encoded_pairs)
            
            return result
            
        except Exception as e:
            error_msg = f"URLエンコーディングエラー: {str(e)}"
            print(error_msg)
            return ""

    def make_get_request(self, url: str, params=None, headers=None, timeout=30):
        """
        指定されたURLにGETリクエストを送信する関数
        
        Args:
            url (str): GETリクエストを送信するURL
            params (dict, optional): クエリパラメータ
            headers (dict, optional): リクエストヘッダー
            timeout (int): タイムアウト時間（秒）
        
        Returns:
            dict: レスポンス情報を含む辞書
        """
        try:
            # デフォルトヘッダーを設定
            if headers is None:
                headers = {
                    'User-Agent': 'Python-GET-Client/1.0'
                }
            
            print(f"GETリクエストを送信中: {url}")
            if params:
                print(f"クエリパラメータ: {json.dumps(params, indent=2, ensure_ascii=False)}")
            print(f"ヘッダー: {json.dumps(headers, indent=2, ensure_ascii=False)}")
            
            # GETリクエストを実行
            response = requests.get(
                url=url,
                params=params,
                headers=headers,
                timeout=timeout
            )
            
            # レスポンス情報を取得
            result = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content': response.text,
                'url': response.url
            }
            
            # JSONレスポンスの場合は解析
            try:
                result['json'] = response.json()
            except json.JSONDecodeError:
                result['json'] = None
            
            print(f"\nレスポンス:")
            print(f"ステータスコード: {response.status_code}")
            print(f"レスポンス内容: {response.text[:200]}...")
            print(f"json: {result['json']}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            error_msg = f"リクエストエラー: {str(e)}"
            print(error_msg)
            return {'error': error_msg}
        except Exception as e:
            error_msg = f"予期しないエラー: {str(e)}"
            print(error_msg)
            return {'error': error_msg}

    def make_post_request(self, url, format, data=None, headers=None, timeout=30):
        """
        指定されたURLにPOSTリクエストを送信する関数
        
        Args:
            url (str): POSTリクエストを送信するURL
            data (dict, optional): 送信するデータ
            headers (dict, optional): リクエストヘッダー
            timeout (int): タイムアウト時間（秒）
        
        Returns:
            dict: レスポンス情報を含む辞書
        """
        try:
            # デフォルトヘッダーを設定
            if headers is None:
                if format == 'json':
                    headers = {
                        'Content-Type': 'application/json',
                        'User-Agent': 'Python-POST-Client/1.0'
                    }
                elif format == 'form':
                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'User-Agent': 'Python-POST-Client/1.0'
                    }
            
            # デフォルトデータを設定
            if data is None:
                data = {
                    'message': 'Hello from Python POST client',
                    'timestamp': '2024-01-01T00:00:00Z'
                }
            
            print(f"POSTリクエストを送信中: {url}")
            print(f"送信データ: {json.dumps(data, indent=2, ensure_ascii=False)}")
            print(f"ヘッダー: {json.dumps(headers, indent=2, ensure_ascii=False)}")
            print(f"format: {format}")

            if format == 'json':
                # POSTリクエストを実行
                response = requests.post(
                    url=url,
                    json=data,
                    headers=headers,
                    timeout=timeout
                )
            else:
                # POSTリクエストを実行
                response = requests.post(
                    url=url,
                    data=data,
                    headers=headers,
                    timeout=timeout
                )

            # レスポンス情報を取得
            result = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content': response.text,
                'url': response.url
            }
            
            # JSONレスポンスの場合は解析
            try:
                result['json'] = response.json()
            except json.JSONDecodeError:
                result['json'] = None
            
            print(f"\nレスポンス:")
            print(f"ステータスコード: {response.status_code}")
            print(f"レスポンス内容: {response.text[:200]}...")
            print(f"json: {result['json']}")

            return result
            
        except requests.exceptions.RequestException as e:
            error_msg = f"リクエストエラー: {str(e)}"
            print(error_msg)
            return {'error': error_msg}
        except Exception as e:
            error_msg = f"予期しないエラー: {str(e)}"
            print(error_msg)
            return {'error': error_msg}

    def make_post_request_json(self, url, data=None, timeout=30):
        return self.make_post_request(url, 'json', data, timeout=timeout)

    def make_get_request_simple(self, url, params=None, timeout=30):
        """
        シンプルなGETリクエスト関数
        
        Args:
            url (str): GETリクエストを送信するURL
            params (dict, optional): クエリパラメータ
            timeout (int): タイムアウト時間（秒）
        
        Returns:
            dict: レスポンス情報を含む辞書
        """
        return self.make_get_request(url, params, None, timeout)

    def resultx(self, result):
        json_text = ""
        if 'error' not in result:
            print(f"\n=== 成功! ===")
            print(f"ステータスコード: {result['status_code']}")
            if result['json']:
                json_text = json.dumps(result['json'], indent=2, ensure_ascii=False)
                print(f"JSONレスポンス: {json_text}")
        else:
            print(f"\n=== エラー ===")
            print(result['error'])

        return {"json_text":json_text, "result": result }

    def test_get(self, url, pattern):
        params = self.make_params(pattern)
        ret = self.test_get_sub(self.url, params)
        print("========================================== GET")
        return ret

    def test_get_sub(self, url, params):
        print("=== GETリクエストのテスト ===")
        # GETリクエストのテスト
        
        result = self.make_get_request_simple(
            url=url,
            params=params
        )
        ret_result = self.resultx(result)

        return ret_result

    def test_post_json(self, url, pattern):
        params = self.make_params(pattern)

        result = self.test_post_sub_json(url, params)
        ret_result = self.resultx(result)
        print("========================================== POST_JSON")
        return ret_result

    def test_post_sub_json(self, url, params):
        print("=== POSTリクエストのテスト ===")
        # POSTリクエストのテスト
        
        result = self.make_post_request_json(
            url=url,
            data=params
        )
        return result

    def test_post_form(self, url, pattern):
        params = self.make_params(pattern)

        result = self.test_post_sub_form(url, params)
        ret_result = self.resultx(result)
        print("========================================== POST_FORM")
        return ret_result

    def test_post_sub_form(self, url, params):
        print("=== POSTリクエストのテスト ===")
        # POSTリクエストのテスト
        result = self.make_post_request(url, 'form', params)
        '''
        result = make_post_request_form(
            url=url,
            data=params
        )
        '''
        return result

    def make_params(self, pattern):
        params = None

        if pattern == 'OpenAI-Cursor':
            params = {
                'cmd': 'web_api',
                'name': 'OpenAI',
                'kind': 'CursorCursor'
            }

        elif pattern == 'web_api_s':
            params = {
                'cmd': 'web_api_s',
                'name': 'OpenAI',
                'kind': 'CursorCursor'
            }
        elif pattern == 'web_api_2':
            params = {
                'cmd': 'web_api_2',
                'name': 'OpenAI',
                'kind': 'CursorCursor'
            }
        elif pattern == "web_api_list":
            params = {
                "cmd": "web_api_list",
            }
        elif pattern == "pc_config":
            params = {
                "cmd": "pc_config",
            }
        elif pattern == "planning":
            params = {
                "cmd": "planning",
            }
        else:
            print(f"pattern: {pattern} is not supported")

        return params

    def run(self, format_option : str, pattern_option : str):
        ret = None
        if format_option in self.formats:
            if pattern_option in self.patterns:
                if format_option == "post_form":
                    ret = self.test_post_form(self.url, pattern_option)
                elif format_option == "post_json":
                    ret = self.test_post_json(self.url, pattern_option)
                else:
                    ret = self.test_get(self.url, pattern_option)
            else:
                print(f"Client.run pattern_option: {pattern_option} is not supported")
        else:
            print(f"Client.run format_option: {format_option} is not supported")

        return ret

if __name__ == "__main__":
    info = Info('info3.json')
    content = info.load_info_json_file_1()
    print(f"client:main:content: {content}")

    formats = content["format"]
    patterns = content["pattern"]
    client = Client(formats=formats, patterns=patterns)
    format = content["format"][1]
    pattern = content["pattern"][2]
    ret = client.run(format, pattern)
    print( f'__main__ ret={ret}' )
    # client.gui_init(content)
    #client.tui_init(content)

