# Vibe Coding 關鍵提示詞

請保留你實際與 AI 的對話截圖，以下為本版關鍵提示詞。

1. 設計 AMB82-MINI 語音控制 LED，左邊開燈控制 LED_B，右邊開燈控制 LED_G。
2. 將 Python GUI 改成 Flask Web，包含語音開關、辨識結果、藍綠 LED 圖形、文字測試與 Log。
3. LED 狀態只能以 Ameba 回傳的 ACK + STATE 為依據。
4. 非控制語句、語音辨識失敗、Serial 失敗不得任意改變 LED。
5. 成功收到 ACK + STATE 後才用瀏覽器 SpeechSynthesis 回覆「左邊藍燈已開啟」。
6. 加入藍燈/綠燈閃爍三次並設計 5+5+1+1 驗收測試。
