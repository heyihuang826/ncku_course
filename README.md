# NCKU COURSE

---

Efficiently and reliably scrapes course information from National Cheng Kung University on a regular basis. The collected data is organized into Excel files and can be automatically uploaded to OneDrive or saved locally.

有效率且穩定的定期從國立成功大學抓取課程資訊。收集到的資料將整理成 Excel 文件，並可自動上傳至 OneDrive 或本地儲存(也可以直接儲存在github repo上，但需要一些額外設定)。

---

## Feature

- Organized the course information of NCKU and then prepare an `excel` file.
- Execute using multithreading.
- Solve the captcha with RCNN AI model to prevent block by the website server.

- 整理成功大學的課程資料並製作成 excel 檔。
- 使用多執行緒執行。
- 使用 RCNN AI 模型通過驗證碼辨識，防止請求被伺服器拒絕。
  
### On github action

- Run at a specified time automatically with github action.
- Upload the result `excel` file to onedrive(you should set some info).
- Save the result `excel` file just on the current repo(that need some setting, you can refer to [this](https://github.com/heyihuang826/web_page_listener/blob/f75487fdce52cc4ec0bbafa8eb9df3c33016e6f2/.github/workflows/main.yml#L35)).

- 使用 github action 自動在指定時間運行。
- 將結果 excel 檔案上傳到 onedrive（需要設定一些資訊）。
- 將結果 excel 檔案僅保存在當前 repo 中（需要一些設置，您可以參考[此處](https://github.com/heyihuang826/web_page_listener/blob/f75487fdce52cc4ec0bbafa8eb9df3c33016e6f2/.github/workflows/main.yml#L35)) ）。

### On personal machine

- Upload the result `excel` file to onedrive(you should set some info).
- Save the result `excel` file just on that machine(by setting the args `save` with `local` for function `run` in `main.py`).

- 將結果 excel 檔案上傳到 onedrive（需要設定一些資訊）。
- 僅在該本地儲存整理好的 excel 檔案（透過在 main.py 中為函數 run 設定 args save 為 local ）。
---

## Example 成果範例

Download `example_202409.xlsx` for example.

下載 example_202409.xlsx 作為範例。

## Usage

- Fork and set `github action secret` (if you need to store course data in onedrive).

or

- Download, setting the args `save` with `local` for function `run` in `main.py`, and enjoy it


- Fork並設定 `github action secret` （如果您需要在 onedrive 中儲存課程資料）。

或

- 下載所有檔案，在 main.py 中為函數 run 設定參數 save 到 local ，然後開始使用。

## Dependence

- python==3.8.10
