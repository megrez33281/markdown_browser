# markdown Browser

## python verison
```
python 3.11.7 or python 3.11.9
```

## install package
```python=
pip install flask==3.0.3
pip install mistune==3.0.2
pip install beautifulsoup4==4.12.3
pip install lxml==5.3.0
pip install chardet==5.2.0
```

## UI說明
* 目錄
![Markdown 目錄](https://github.com/megrez33281/markdown_browser/blob/main/img/1.png?raw=true)
* 閱讀md檔案介面
![瀏覽md檔案](https://github.com/megrez33281/markdown_browser/blob/main/img/2.png?raw=true)


## 使用說明
1. 安裝相關依賴套件
2. 執行MarkdownBrowser.py
3. 前往** http://127.0.0.1:5000 **可見Markdown Browser目錄


## 架構圖
![架構圖](https://github.com/megrez33281/markdown_browser/blob/main/img/%E6%9E%B6%E6%A7%8B%E5%9C%96.png?raw=true)

## 流程圖
![流程圖](https://github.com/megrez33281/markdown_browser/blob/main/img/%E6%B5%81%E7%A8%8B%E5%9C%96.png?raw=true)


## 單元測試
* 安裝套件
    ```
    pip install pytest pytest-cov pytest-mock
    ```
* 測試框架
    ```
    python -m pytest
    ```
* 測試覆蓋率
    ```
    python -m pytest --cov --cov-branch 
    ```
* 測試覆蓋率並生成html報告
    ```
    pytest --cov --cov-branch --cov-report=html
    ```