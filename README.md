# SIC/XE Interpreter

長庚大學資訊工程學系課程實作專題。

本專案使用 Python 與 Tkinter 建立簡易 SIC/XE Assembly 解譯器，提供圖形化操作介面，可載入、編輯、儲存及執行 `.asm` 程式，並顯示執行後的暫存器與記憶體狀態。

Repository 中另外保留三個課程期間使用的 Assembly 測試檔案，可直接用於測試解譯器的載入與執行功能。

**Institution:** 長庚大學 資訊工程學系  
**Language:** Python / SIC/XE Assembly  
**GUI:** Tkinter  
**Development Environment:** Visual Studio Code

---

## Repository Structure

```text
SICXE-Interpreter/
│
├── sicxe.py
├── first.asm
├── second.asm
├── third.asm
└── README.md
```

- `sicxe.py` — SIC/XE 解譯器主程式
- `first.asm` — Assembly 測試程式
- `second.asm` — Assembly 測試程式
- `third.asm` — Assembly 測試程式

---

## Features

程式以 Tkinter 建立簡易操作介面，透過上方指令列輸入指令。

目前包含：

- 載入 `.asm` 程式
- 儲存 Assembly 程式
- 建立 / 清除目前內容
- 編輯程式
- 顯示含行號的程式內容
- 執行 SIC/XE Assembly 測試程式
- 模擬 Register 狀態
- 模擬 Memory Variable
- 顯示程式執行結果

---

## Supported Commands

| Command | Function |
| --- | --- |
| `load <filename>` | 載入指定 `.asm` 檔案 |
| `save <filename>` | 將目前內容儲存為指定檔案 |
| `clear` | 清空目前程式內容 |
| `new` | 建立新的空白內容 |
| `list` | 顯示目前程式並加入行號 |
| `edit` | 切換至可編輯模式 |
| `run` | 執行目前載入的 Assembly 程式 |
| `exit` | 關閉解譯器 |

---

## Supported Assembly Operations

目前版本以課程測試需求為主，實作部分基本 SIC/XE 指令與資料定義。

### Instructions

- `START`
- `LDA`
- `ADD`
- `STA`
- `END`

### Data

- `WORD`

程式會先掃描 Assembly 內容建立記憶體變數，再依序處理可執行指令。

例如：

```asm
COPY    START   2000
        LDA     ALPHA
        ADD     BETA
        STA     RESULT
        END     COPY

ALPHA   WORD    3
BETA    WORD    7
```

執行後會將 `ALPHA` 與 `BETA` 的內容進行運算，並更新暫存器與記憶體狀態。

---

## How to Run

### 1. 安裝 Python

請先確認電腦已安裝 Python。

可在 VS Code Terminal 輸入：

```bash
python --version
```

確認 Python 能正常執行。

本專案 GUI 使用 Python 內建的 `tkinter`。

---

### 2. 使用 VS Code 開啟整個資料夾

本專案載入 `.asm` 檔案時，會直接從目前的工作目錄尋找檔案，因此請將：

```text
sicxe.py
first.asm
second.asm
third.asm
```

放在**同一個資料夾**。

接著不要只單獨開啟 `sicxe.py`，而是使用 VS Code：

```text
File
→ Open Folder...
→ 選擇 SICXE-Interpreter 資料夾
```

確認 VS Code 開啟的資料夾結構為：

```text
SICXE-Interpreter/
├── sicxe.py
├── first.asm
├── second.asm
└── third.asm
```

---

### 3. 執行 Interpreter

在 VS Code Terminal 執行：

```bash
python sicxe.py
```

成功後會開啟 SIC/XE Interpreter GUI。

---

## Loading a Test Program

啟動程式後，在 GUI 上方的指令輸入欄輸入：

```text
load first.asm
```

並按下 `Enter`。

如果載入成功，`first.asm` 的程式內容會顯示於編輯區。

其他測試檔亦可使用：

```text
load second.asm
```

或：

```text
load third.asm
```

---

## Running the Program

成功載入 `.asm` 後，在指令列輸入：

```text
run
```

程式會解析目前載入的 Assembly 內容，初始化模擬暫存器與記憶體，並依序執行支援的指令。

執行完成後會顯示：

```text
[暫存器狀態]

 A: ...
 X: ...
 L: ...
 B: ...
 S: ...
 T: ...
 F: ...

[記憶體變數]

...

最終結果 RESULT: ...
```

---

## Program Flow

```text
             SIC/XE Interpreter
                     │
                     ▼
               Tkinter GUI
                     │
              load filename.asm
                     │
                     ▼
              Read ASM Source
                     │
                     ▼
          Parse WORD Definitions
                     │
                     ▼
          Build Simulated Memory
                     │
                     ▼
          Parse Instructions
                     │
                     ▼
          Execute Instructions
                     │
                     ▼
       Update Registers / Memory
                     │
                     ▼
             Display Result
```

---

## Implementation

程式以 Dictionary 模擬 SIC/XE 暫存器：

```python
register = {
    "A": 0,
    "X": 0,
    "L": 0,
    "B": 0,
    "S": 0,
    "T": 0,
    "F": 0,
    "PC": 0,
    "SW": 0
}
```

並以另一個 Dictionary 模擬程式中的記憶體變數。

Assembly 程式載入後會先掃描資料定義，再建立待執行的 Instruction List，最後依序模擬各指令對 Register 與 Memory 的影響。

---

## Test Files

Repository 提供三個 `.asm` 測試檔案：

### `first.asm`

測試基本的：

```text
LDA → ADD → STA
```

使用 `ALPHA` 與 `BETA` 進行加法後將結果存入 `RESULT`。

### `second.asm`

另一組 SIC/XE Assembly 測試程式，包含資料定義與運算流程。

### `third.asm`

使用不同的變數與程式起始設定測試 Assembly 載入與執行流程。

---

## What I Learned

透過這個實作，我將 SIC/XE Assembly 課程中對指令、暫存器與記憶體的概念轉換成可執行的 Python 模擬程式。

實作過程除了需要處理 Assembly 程式文字解析，也需要思考每一條指令執行後應如何改變暫存器與記憶體狀態。透過 Tkinter 加入載入、編輯、儲存與執行功能後，也讓原本單純的指令模擬進一步形成可以實際操作與測試的簡易解譯器。

---

> 本 Repository 為大學課程實作成果整理，以課程期間完成之程式與測試檔案為主。
