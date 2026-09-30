# 0917 作業報告內容架構

## 專題目標
使用瀏覽器麥克風進行中文語音辨識，將結果轉換成控制指令，透過 USB Serial 控制 AMB82-MINI 的 LED_B/LED_G。

## 系統架構
麥克風 → Chrome/Edge Web Speech API → JavaScript → Flask → PySerial → AMB82-MINI → LED → ACK/STATE → Web UI。

## Vibe Coding
放入實際 Prompt、AI 產生程式、測試截圖與修正紀錄。

## 實際問題
PC 送出指令不等於 LED 實際成功。因此修正為：只有收到 AMB82-MINI 的 ACK + STATE 才更新網頁 LED 狀態。

## 驗收
填寫 test_results.md。

## Demo
YouTube：【你的連結】

## GitHub
【你的連結】

## 學習心得
Vibe Coding 是透過自然語言描述、程式生成、實機測試、問題分析與修正完成系統，而不是一次生成後直接使用。
