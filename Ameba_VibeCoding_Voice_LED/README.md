# AMB82-MINI Vibe Coding Voice LED Web Controller

第二版：Web 控制介面 + Python Flask + USB Serial + AMB82-MINI。

## 功能
- 左邊開燈 → 藍燈 LED_B
- 右邊開燈 → 綠燈 LED_G
- Chrome/Edge 中文語音辨識
- LED 狀態以 AMB82-MINI 回傳 ACK + STATE 為依據
- 文字測試、快速指令、系統 Log
- 非控制語句/語音辨識失敗不改變 LED
- Serial 通訊失敗提示
- 瀏覽器語音回饋
- 藍/綠燈閃爍三次

## 硬體
Ameba AMB82-MINI / RTL8735B
- LED_B：Blue，Arduino pin 23
- LED_G：Green，Arduino pin 24

## 執行
Arduino IDE 上傳 `ameba/ameba_led_controller.ino`，Serial 115200。
VS Code Terminal：
```powershell
pip install -r requirements.txt
$env:AMEBA_PORT="COM7"
python backend/app.py
```
把 COM7 換成你的實際 Port。
瀏覽器開 `http://127.0.0.1:5000`。

## 建議測試
先測 Arduino LED → Serial → Web 文字 → Web 語音 → 非控制語句 → 拔 USB 通訊中斷 → 閃爍三次。


## V3 區網多裝置版

- Flask 監聽 `0.0.0.0:5000`，同一 Wi-Fi/LAN 的手機、平板、其他電腦可開啟。
- 網頁會顯示區域網路網址。
- AMB82-MINI 閃爍時，每次狀態切換都回傳 `STATE`，網頁依板端回傳同步更新。
- Windows 防火牆若詢問 Python 網路存取，請允許「私人網路」。
