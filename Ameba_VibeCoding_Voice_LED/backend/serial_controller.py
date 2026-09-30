import os, time, serial
from serial import SerialException

DEFAULT_PORT = os.getenv("AMEBA_PORT", "COM5")
BAUDRATE = int(os.getenv("AMEBA_BAUD", "115200"))
ACK_TIMEOUT = float(os.getenv("AMEBA_ACK_TIMEOUT", "2.0"))

class SerialController:
    def __init__(self):
        self.port = DEFAULT_PORT
        self.ser = None
        self.state = {"blue": False, "green": False}

    def is_connected(self):
        return self.ser is not None and self.ser.is_open

    def connect(self):
        if self.is_connected(): return True, f"已連線：{self.port}"
        try:
            self.ser = serial.Serial(self.port, BAUDRATE, timeout=0.15)
            time.sleep(.5); self.ser.reset_input_buffer()
            self.send_raw("GET_STATUS"); self._read(.8)
            return True, f"已連線：{self.port}"
        except (SerialException, OSError) as e:
            self.ser = None
            return False, f"通訊失敗：無法連線 {self.port}（{e}）"

    def disconnect(self):
        if self.ser:
            try: self.ser.close()
            except Exception: pass
        self.ser = None

    def send_raw(self, cmd):
        if not self.is_connected(): raise SerialException("開發板未連線")
        self.ser.write((cmd+"\n").encode()); self.ser.flush()

    def _read(self, seconds):
        lines=[]; deadline=time.time()+seconds
        while time.time()<deadline:
            raw=self.ser.readline()
            if not raw: continue
            line=raw.decode("utf-8","ignore").strip()
            if not line: continue
            lines.append(line)
            self._state_from(line)
        return lines

    def _state_from(self, line):
        if not line.startswith("STATE "): return
        for part in line[6:].split():
            if part.startswith("BLUE="): self.state["blue"] = part.split("=")[1]=="1"
            if part.startswith("GREEN="): self.state["green"] = part.split("=")[1]=="1"

    def send_command(self, command):
        if not self.is_connected():
            return {"ok":False,"accepted":True,"command":command,
                    "message":"❌ 通訊失敗：開發板未連線，LED 狀態未更新",
                    "event":f"指令 {command} → 通訊失敗",**self.state}
        try:
            self.ser.reset_input_buffer(); self.send_raw(command)
            deadline=time.time()+ACK_TIMEOUT; ack=False; got_state=False
            while time.time()<deadline:
                raw=self.ser.readline()
                if not raw: continue
                line=raw.decode("utf-8","ignore").strip()
                if line==f"ACK {command}": ack=True
                if line.startswith("STATE "): got_state=True; self._state_from(line)
                if ack and got_state: break
            if not (ack and got_state):
                return {"ok":False,"accepted":True,"command":command,
                        "message":"❌ 通訊失敗：未收到完整 ACK/STATE，LED 狀態未更新",
                        "event":f"指令 {command} → ACK/STATE timeout",**self.state}
            messages={"LEFT_ON":"✓ 左邊藍燈已開啟","RIGHT_ON":"✓ 右邊綠燈已開啟",
                      "ALL_OFF":"✓ 藍、綠燈已關閉","FLASH_BLUE_3":"✓ 藍燈已完成三次閃爍",
                      "FLASH_GREEN_3":"✓ 綠燈已完成三次閃爍","FLASH3":"✓ 藍、綠燈已完成三次閃爍",
                      "GET_STATUS":"✓ 已取得開發板實際 LED 狀態"}
            return {"ok":True,"accepted":True,"command":command,
                    "message":messages.get(command,f"✓ 指令 {command} 已由開發板確認"),
                    "event":f"Board：ACK {command}；STATE BLUE={int(self.state['blue'])} GREEN={int(self.state['green'])}",
                    **self.state}
        except (SerialException,OSError) as e:
            self.disconnect()
            return {"ok":False,"accepted":True,"command":command,
                    "message":f"❌ 通訊失敗：{e}","event":f"指令 {command} → Serial 例外",**self.state}
