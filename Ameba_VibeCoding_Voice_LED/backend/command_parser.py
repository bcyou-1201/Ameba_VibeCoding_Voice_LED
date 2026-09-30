def normalize(text):
    return "".join(text.strip().lower().split())

def parse_command(text):
    t = normalize(text)
    exact = {
        "左邊開燈":"LEFT_ON", "右邊開燈":"RIGHT_ON", "全部關燈":"ALL_OFF",
        "關閉全部燈":"ALL_OFF", "藍燈閃爍三次":"FLASH_BLUE_3",
        "綠燈閃爍三次":"FLASH_GREEN_3", "閃爍三次":"FLASH3",
        "查詢狀態":"GET_STATUS", "取得狀態":"GET_STATUS"
    }
    if t in exact: return exact[t]
    if "左邊" in t and "開燈" in t: return "LEFT_ON"
    if "右邊" in t and "開燈" in t: return "RIGHT_ON"
    if "藍燈" in t and "閃爍" in t and "三次" in t: return "FLASH_BLUE_3"
    if "綠燈" in t and "閃爍" in t and "三次" in t: return "FLASH_GREEN_3"
    return None
