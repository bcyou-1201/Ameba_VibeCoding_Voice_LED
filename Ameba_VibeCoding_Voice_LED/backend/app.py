import socket
from flask import Flask, jsonify, request, send_from_directory
from serial_controller import SerialController
from command_parser import parse_command
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
serial_controller = SerialController()
last_recognition = ""
last_message = "尚未執行指令"
last_event = "系統已啟動"

@app.get("/")
def index(): return send_from_directory(FRONTEND_DIR, "index.html")

@app.get("/api/status")
def status():
    return jsonify({"connected": serial_controller.is_connected(), "port": serial_controller.port,
                    "blue": serial_controller.state["blue"], "green": serial_controller.state["green"],
                    "recognition": last_recognition, "message": last_message, "event": last_event})

@app.post("/api/connect")
def connect():
    global last_message, last_event
    ok, msg = serial_controller.connect()
    last_message = last_event = msg
    return jsonify({"ok": ok, "message": msg, **serial_controller.state}), (200 if ok else 503)

@app.post("/api/disconnect")
def disconnect():
    global last_message, last_event
    serial_controller.disconnect()
    last_message = last_event = "已中斷開發板連線"
    return jsonify({"ok": True, "message": last_message})

@app.post("/api/recognition")
def recognition():
    global last_recognition, last_message, last_event
    text = str((request.get_json(silent=True) or {}).get("text", "")).strip()
    last_recognition = text
    command = parse_command(text)
    if command is None:
        last_message = "非控制指令：LED 狀態保持不變"
        last_event = f"語音/文字：{text or '(空白)'} → 非控制指令"
        return jsonify({"ok": True, "accepted": False, "message": last_message, "command": None, **serial_controller.state})
    return jsonify(execute_command(command))

@app.post("/api/command")
def command():
    text = str((request.get_json(silent=True) or {}).get("text", "")).strip()
    cmd = (request.get_json(silent=True) or {}).get("command") or parse_command(text)
    if cmd is None:
        return jsonify({"ok": True, "accepted": False, "message": "非控制指令：LED 狀態保持不變",
                        "command": None, **serial_controller.state})
    return jsonify(execute_command(cmd))

def execute_command(command):
    global last_message, last_event
    result = serial_controller.send_command(command)
    last_message, last_event = result["message"], result["event"]
    return result

if __name__ == "__main__":
    print("Open http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
