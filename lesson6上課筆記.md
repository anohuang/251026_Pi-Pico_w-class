# 要從新裝置上下載repo之步驟
## 1. 安裝git，安裝過程一直next就好
## 2. 於cursor或antigravity中開啟終端機，注意要選cmd
## 3. 可先輸入git --version來確認是否安裝成功
## 4. 做git初始化
###   a. 輸入git onfig --global user.name "xxxxxxxx" >>名稱不重要，只是裝置名稱
 ###  b. 輸入git config --global user.email "xxxxx@gmail.com"
 ###  c. 輸入git config --global pull.rebase false >>問拉下來後是否建立分支或混合，false代表混合
## 5. 做完初始化可輸入git config --list來確認是否設定成功 >>如果出現上述輸入的名稱即表示成功
## 6. 安裝uv >> 於cursor或antigravity中開啟終端機，注意要選poweshell 
   _**(如果已經有安裝uv的repo，可略過此步驟，直接到第7步)**_
###   a. 輸入powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
## 7. 做uv虛擬環境
###   a. 輸入uv venv
###   b. 輸入uv sync 
###   c. 新的VScode編輯軟體記得要安裝jupyter notebook
###   d. 於ipynb檔案裝選取虛擬環境的核心
## 8. 以上完成即可複製repo至新裝置中，未來連線到git都記得要先同步
資料來源: 可看老師github上教python的repo講義
