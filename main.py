import requests
import json
import sys
from datetime import datetime
from urllib import request as req

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}

WEBHOOK_URL = "Input_Webhook_Url_Here"

urls = [
    'www.google.com.tw',
    'tw.yahoo.com',
    'www.bing.com'
]

def Web_Check(urls):
    status_report = []
    status_Check = False
    for url in urls:
        url = f"https://{url}/"
        try:
            response = requests.get(url, timeout=20, verify=False, headers=headers)
            if response.status_code == 200:
                status_report.append(f"✅ 正常運作 (狀態碼: {response.status_code})  {url}")
            else:
                status_report.append(f"⚠️ 存取異常 (狀態碼: {response.status_code})  {url}")
                status_Check = True
        except requests.exceptions.RequestException as e:
            status_report.append(f"❌ 無法存取 {url}: {e}" + "\n")
            status_Check = True

    return status_report, status_Check

def post_message(messages: list) -> None:
    request = req.Request(url=WEBHOOK_URL, method="POST")
    request.add_header("Content-Type", "application/json")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_text = f"📅 檢查時間：{current_time}\n\n" + " <br>" + "\n\n".join(messages)
    #message_text = "\n\n".join(messages)
    data = json.dumps({"text": message_text}).encode()
    #print(data)
    with req.urlopen(url=request, data=data) as response:
        if response.status != 200:
            raise TeamsWebhookException(response.reason)

def get_time_str():
    time_stamp = time.time()
    time_str = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time_stamp))
    return time_str

def is_in_time_range():
    now = datetime.now()
    current_time = now.strftime("%H%M")  # 轉換成 4 位數時間格式 (HHMM)
    time_ranges = [("0859", "0901"), ("1359", "1401"), ("1659", "1701")]

    return any(start <= current_time <= end for start, end in time_ranges)

check_Time = is_in_time_range()
status_report, status_Check = Web_Check(urls)
Debug_Mode = False

if status_Check or check_Time:
    if not Debug_Mode: post_message(status_report)
    else:
        print('異常顯示')
        print(status_Check)
        print(status_report)
        print("\n".join(status_report))
else:
    if not Debug_Mode: pass
    else:
        print('沒問題顯示')
        print(status_Check)
        print(status_report)
        print("\n".join(status_report))
    
