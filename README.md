# NCKU COURSE

---

Efficiently and reliably scrapes course information from National Cheng Kung University on a regular basis(if you choose to store data on onedrive). The collected data is organized into Excel files and can be automatically uploaded to OneDrive or saved locally (to your personal computer or github repo).

---

## Feature

- Organized the course information of NCKU and then prepare an `excel` file.
- Execute using multithreading.
- Solve the captcha with RCNN AI model to prevent block by the website server.
  
### On github action

- Run at a specified time automatically with github action.
- Upload the result `excel` file to onedrive(you should set some info).
- Save the result `excel` file just on the current repo(that need some setting, you can refer to [this](https://github.com/heyihuang826/web_page_listener/blob/f75487fdce52cc4ec0bbafa8eb9df3c33016e6f2/.github/workflows/main.yml#L35)).

### On personal machine

- Upload the result `excel` file to onedrive(you should set some info).
- Save the result `excel` file just on that machine(by setting the args `save` with `local` for function `run` in `main.py`).

---

## Example

Download `example_202409.xlsx` for example.

## Usage

- Fork and set `github action secret` (if you need to store course data in onedrive).

or

- Download, setting the args `save` with `local` for function `run` in `main.py`, and enjoy it.

## Dependence

- python==3.8.10
