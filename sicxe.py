import tkinter as tk #載入tkinter模組，要使用GUI
#載入模組中兩個常用對話框功能，前者用來打開儲存檔案，後者用來跳出訊息式窗
from tkinter import filedialog, messagebox 

#初始化暫存器和記憶體，暫存器儲存運算結果，記憶體儲存變數
register = {"A": 0, "X": 0, "L": 0, "B": 0, "S": 0, "T": 0, "F": 0, "PC": 0, "SW": 0}
memory = {}

#宣告名為SICXE的類別，用來建立、控制解譯器之GUI介面
class SICXE:
    #建立建構子，為啟動GUI畫面時，會執行以下設定
    #self.東西 = 放進這個物件自己的東西
    #root = tkinter的主畫面，這個物件會在主畫面上顯示
    def __init__(self, root):
        self.root = root #記住主畫面root，在物件的屬性self.root
        self.root.title("SIC/XE 解譯器") #設定視窗標題
        #宣告一個變數filename，預設為None，這個變數用來記錄目前載入或儲存的檔案名稱
        self.filename = None 

        #建立一個單行輸入欄位，讓使用者可以輸入指令，使用Courier字型，大小為12
        self.entry = tk.Entry(root, font=("Courier", 12))
        #將輸入欄位放在主畫面上，並設定填滿整個畫面(fill='x'代表寬度填滿整行)，並加入邊框和內邊距(padx=10, pady=5)
        #padx（padding x）：設定元件左右兩側與容器邊界之間的「外邊距」為 10 像素
        #pady（padding y）：設定上下兩側的外邊距為 5 像素
        self.entry.pack(fill="x", padx=10, pady=5)
        #按下Enter鍵時，會執行execute_command函式，就是按下Enter鍵後，會執行輸入的指令
        self.entry.bind("<Return>", self.execute_command)

        #建立一個多行文字框，用來顯示與編輯.asm檔案的內容，使用Courier字型，大小為12，並設定高度為20行
        self.text = tk.Text(root, font=("Courier", 12), height=20)
        #將文字框放在主畫面上，並設定填滿整個畫面(fill='both'代表寬度和高度都填滿)
        #expand=True代表當視窗大小改變時，文字框會隨之擴展，並加入邊框和內邊距(padx=10)
        self.text.pack(fill="both", expand=True, padx=10)

        #建立一個狀態列Label，用來顯示目前的狀態:就緒，anchor="w"代表文字靠左(west)對齊
        self.status = tk.Label(root, text="狀態：就緒", anchor="w")
        #將狀態列放入畫面下方，並設定填滿整個畫面(fill='x'代表寬度填滿整行)
        self.status.pack(fill="x")

    #定義一個函式execute_command，當使用者按下Enter鍵時，會執行這個函式
    #event=None是為了讓這個方法可以被bind("<Return>")綁定使用接收鍵盤事件(event是tkinter的事件物件)
    def execute_command(self, event=None):
        #取得使用者在輸入欄位(Entry)輸入的指令，並去除前後空白(.strip())
        cmd = self.entry.get().strip()
        #清空輸入框的內容（使用者在按下Enter執行後就會清理掉）
        self.entry.delete(0, tk.END)

        #如果指令以load開頭，則表示要載入檔案
        if cmd.startswith("load"):
            #將指令切割成兩部分，第一部分是指令(load)，第二部分是檔案名稱(first.asm)
            #取得檔案名稱(這裡是first.asm)
            self.filename = cmd.split()[1]
            #用try來嘗試讀檔案，這樣如果檔案不存在或讀取失敗，就不會讓程式當機
            try:
                #開啟檔案(讀取模式"r")
                f = open(self.filename, "r")
                #讀取整份檔案內容存到content變數
                content = f.read()
                #關閉檔案
                f.close()
                #清空目前程是碼編輯區(tk.END表示直到最後)
                self.text.delete(1.0, tk.END)
                #將剛剛讀近來的.asm程式碼插入到編輯區(1.0表示從第一行第零個字元開始)
                self.text.insert(1.0, content)
                #更新狀態列的文字，顯示目前載入的檔案名稱
                self.status.config(text="已載入：" + self.filename)
            except: #如果讀檔失敗，則顯示錯誤訊息
                messagebox.showerror("錯誤", "載入失敗")

        #如果指令以save開頭，則表示要儲存檔案
        elif cmd.startswith("save"):
            #將指令切割成兩部分，第一部分是指令(save)，第二部分是檔案名稱(first.asm)
            #取得檔案名稱(這裡是first.asm)
            self.filename = cmd.split()[1]
            #以寫入模式"w"開啟檔案(如果檔案不存在會自動建立)
            f = open(self.filename, "w")
            #將程式編輯區的內容寫入檔案
            f.write(self.text.get(1.0, tk.END))
            f.close()
            self.status.config(text="已儲存：" + self.filename)

        #如果指令是"clear"或"new"，則表示要清空編輯區
        elif cmd == "clear" or cmd == "new":
            self.text.delete(1.0, tk.END)
            self.status.config(text="內容已清空")

        #如果指令是"list"，則表示要加上行號列出目前程式碼
        elif cmd == "list":
            #取得編輯區的內容，並去除前後空白(.strip)，然後用換行符號分割成多行
            #ex:code = ["LDA ALPHA", "ADD BETA", "STA RESULT"]
            code = self.text.get(1.0, tk.END).strip().split("\n")
            listed = "" #建立一個空字串，用來儲存加上行號的程式碼
            i = 1 #i變數作為行號計數器，從第1行開始
            
            for line in code: #逐行走訪，從編輯區抓出每一行程式碼
                #把目前行號i和程式碼組合成，加到字串裡
                #str(i)表示將i轉換成字串，rjust(2, '0')表示如果字串長度小於2，就在前面補0，讓行號都是兩位數
                #line是目前行的程式碼，
                listed += str(i).rjust(2, '0') + ": " + line + "\n"
                i += 1 #行號累加，準備處理下一行
            messagebox.showinfo("程式內容", listed)

        elif cmd == "edit":
            #state="normal"表示可以編輯，"disabled"表示不能編輯，是唯讀
            self.text.config(state="normal")
            self.status.config(text="可編輯模式")

        elif cmd == "exit":
            #destroy()是tkinter表示關閉GUI視窗的方法
            self.root.destroy()

        elif cmd == "run":
            #把編輯區的內容抓出來，並去除前後空白(.strip)，然後用換行符號分割成多行
            code = self.text.get(1.0, tk.END).strip().split("\n")
            #呼叫類別中的 run_code() 方法，傳入程式碼列表進行模擬執行
            self.run_code(code)

    def run_code(self, lines):
        for key in register:
            register[key] = 0
        memory.clear() #清空模擬記憶體

        instructions = [] #用來儲存可執行的指令

        #第一輪掃描整份程式，找出變數定義（例如 ALPHA WORD 3）分解後：parts[0] 是變數名稱（
        # 如 ALPHA）parts[2] 是整數值（如 3）然後把變數放入記憶體字典 memory 中
        i = 0
        while i < len(lines):
            parts = lines[i].strip().split()
            if len(parts) >= 3 and parts[1] == "WORD":
                memory[parts[0]] = int(parts[2])
            i += 1

        #重設 i = 0，再從頭掃描一次程式碼把每一行拆成一個
        #  parts 列表（如 ["LDA", "ALPHA"]）
        i = 0
        while i < len(lines):
            parts = lines[i].strip().split()
            #根據是否有標籤（Label），來決定指令是第幾個位置：若 parts 長度是 3（含標籤），
            # 如 COPY LDA ALPHA，那 op 是 parts[1]，若是 2（無標籤），
            # 如 LDA ALPHA，那 op 是 parts[0]
            if len(parts) >= 2:
                if len(parts) >= 3:
                    op = parts[1]
                else:
                    op = parts[0]
                #如果是 START，跳過這行，因為 START 是起始標記，不需執行
                if op == "START":
                    i += 1
                    continue
                # 如果是有效的執行指令，就加入 instructions 清單中，準備後續執行
                if op == "LDA" or op == "ADD" or op == "STA" or op == "END":
                    instructions.append(parts)
            i += 1

        # 用一個簡單的程式計數器 pc，
        # 從第 0 條指令開始執行每次從 instructions 中取出一條指令
        pc = 0
        while pc < len(instructions):
            parts = instructions[pc]
            if len(parts) == 3: #標籤+指令+操作數
                op = parts[1]
                operand = parts[2] #operand 是操作數
            elif len(parts) == 2: #指令+操作數
                op = parts[0]
                operand = parts[1]
            else: #如果 parts 的長度不是 2 或 3，表示該行格式不符
                pc += 1
                continue

            if op == "LDA":
                #將操作數的值載入暫存器 A
                if operand in memory:
                    register["A"] = memory[operand]
            elif op == "ADD":
                #把目前 A 的值加上該變數值，結果寫回 A
                if operand in memory:
                    register["A"] = register["A"] + memory[operand]
            elif op == "STA":
                #把暫存器 A 的值，存進記憶體的變數裡
                memory[operand] = register["A"]
            elif op == "END":
                break

            pc += 1 #每次執行完一條指令後，程式計數器 pc 加 1，移到下一條指令

        result = "[暫存器狀態]\n"
        keys = ["A", "X", "L", "B", "S", "T", "F"]
        for i in range(len(keys)):
            result += keys[i].rjust(2) + ": " + str(register[keys[i]]) + "\n"

        result += "\n[記憶體變數]\n"
        for key in memory:
            result += key + ": " + str(memory[key]) + "\n"

        if "RESULT" in memory:
            result += "\n 最終結果 RESULT: " + str(memory["RESULT"]) + "\n"
        else:
            result += "\n 最終結果 RESULT: 未定義\n"

        messagebox.showinfo("執行結果", result)
        self.status.config(text="程式執行完成")

#這是程式的主函式，當這個檔案被執行時，會啟動SICXE類別的GUI介面
#為啟動GUI程式的標準寫法，這是啟動 GUI 程式的標準寫法：建立主視窗 root，
# 把 SICXE 類別實體化成一個 app 物件，執行 mainloop() 讓介面不斷運作
if __name__ == "__main__":
    root = tk.Tk()
    app = SICXE(root)
    root.mainloop()
