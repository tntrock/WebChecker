# WebChecker
檢查網站是否還活著，並使用Webhook輸出結果到Microsoft Teams
  
為了避免部分網站基於阻擋爬蟲的緣故，會阻擋Python的header，因此手動設定headers
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}
```
  
請先到Teams取得Webhook的URL，並填入此處
```python
WEBHOOK_URL = "Input_Webhook_Url_Here"
```
  
需要檢查的URL清單
```python
urls = [
    'www.google.com.tw',
    'tw.yahoo.com',
    'www.bing.com'
]
```
  
為了避免檢查頻率過高，造成訊息洗版  
檢查結果若正常，僅有0859-0901、1359-1401、1659-1701這三個時間點才會發訊息  
但檢查結果若有問題時，也會立即發出訊息
```python
def is_in_time_range():
    now = datetime.now()
    current_time = now.strftime("%H%M")  # 轉換成 4 位數時間格式 (HHMM)
    time_ranges = [("0859", "0901"), ("1359", "1401"), ("1659", "1701")]

    return any(start <= current_time <= end for start, end in time_ranges)
```
