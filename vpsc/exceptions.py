class APIException(Exception):
    def __init__(self, status, json):
        self.status = status
        self.json = json


def exception_handler(exc):
    if isinstance(exc, APIException):
        if exc.status == 400:
            # Bad Request
            print(f"エラー: リクエストが不正です (400 Bad Request)")
            print(f"エラーコード: {exc.json.get('code', 'unknown')}")
            print(f"メッセージ: {exc.json.get('message', '不明なエラー')}")
            if 'errors' in exc.json and exc.json['errors']:
                print("詳細:")
                for field, errors in exc.json['errors'].items():
                    if field == 'non_field_errors':
                        for error in errors:
                            print(f"  - {error.get('message', '')}")
                    else:
                        for error in errors:
                            print(f"  - {field}: {error.get('message', '')}")
        elif exc.status == 404:
            # Not Found
            print(f"エラー: リソースが見つかりません (404 Not Found)")
            print(f"エラーコード: {exc.json.get('code', 'unknown')}")
            print(f"メッセージ: {exc.json.get('message', '不明なエラー')}")
        elif exc.status == 409:
            # Conflict
            print(f"エラー: リソースの状態が競合しています (409 Conflict)")
            print(f"エラーコード: {exc.json.get('code', 'unknown')}")
            print(f"メッセージ: {exc.json.get('message', '不明なエラー')}")
        elif exc.status == 429:
            # Too Many Requests
            print(f"エラー: リクエスト数が制限を超えています (429 Too Many Requests)")
            print(f"エラーコード: {exc.json.get('code', 'unknown')}")
            print(f"メッセージ: {exc.json.get('message', '不明なエラー')}")
        elif exc.status == 503:
            # Service Unavailable
            print(f"エラー: サービスが一時的に利用できません (503 Service Unavailable)")
            print(f"エラーコード: {exc.json.get('code', 'unknown')}")
            print(f"メッセージ: {exc.json.get('message', '不明なエラー')}")
        else:
            # Other errors
            print(f"エラー: ステータスコード {exc.status}")
            print(f"内容: {exc.json}")
