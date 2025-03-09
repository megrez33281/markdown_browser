import pytest
import unittest
from unittest.mock import patch, mock_open
import MarkdownToHtml
from bs4 import BeautifulSoup

@patch("base64.b64encode")
@patch("builtins.open", new_callable=mock_open, read_data=b"test string")  # binary mode
def test_image_to_base64(mock_file, mock64):
    path = "./test.png"
    # 設定 mock 返回值
    mock64.return_value = b"encode64"  # base64.b64encode 回傳 bytes
    # 調用被測函數
    result = MarkdownToHtml.image_to_base64(path)

    # 驗證 open() 是否被正確呼叫
    mock_file.assert_called_once_with(path, "rb")

    # 驗證 base64 的行為
    mock64.assert_called_once() 


    # 驗證返回結果
    expected_result = "data:image/" + "png" + ";base64," + "encode64"
    assert result == expected_result


def test_MakeMarkdownContainer():
    # 測試參數
    contents = [BeautifulSoup('<p>Test Content</p>', 'html.parser').p]
    scriptContents = "console.log('Hello, world!');"
    title = "測試標題"

    # 調用函式
    result = MarkdownToHtml.MakeMarkdownContainer(contents, scriptContents, title)

    # 解析輸出的 HTML
    soup = BeautifulSoup(result, "html.parser")

    # 驗證 <!DOCTYPE html> 存在
    assert result.startswith("<!DOCTYPE html>")

    # 驗證 <html lang="zh">
    assert soup.html and soup.html.get("lang") == "zh"

    # 驗證 <head> 存在
    head = soup.head
    assert head is not None

    # 驗證 <meta charset="UTF-8">
    assert head.find("meta", {"charset": "utf-8"}) is not None

    # 驗證 <title>
    title_tag = head.find("title")
    assert title_tag and title_tag.getText().replace("\n", "").replace(' ', '') == title

    # 驗證 <link rel="shortcut icon">
    assert head.find("link", {"rel": "shortcut icon", "href": "../static/favicon.ico"}) is not None

    # 驗證 <link rel="stylesheet">
    assert head.find("link", {"rel": "stylesheet", "href": "../static/markdownStyles.css"}) is not None

    # 驗證 <body> 存在
    body = soup.body
    assert body is not None

    # 驗證 <div class="title-region">
    title_region = body.find("div", {"class": "title-region"})
    assert title_region is not None
    assert title_region.get("onclick") == 'location.href = this.querySelector("a").href;'

    # 驗證 <a> 連結
    a_tag = title_region.find("a", {"href": "../home", "class": "title-href"})
    assert a_tag is not None

    # 驗證 <div id="markdown-content">
    markdown_content = body.find("div", {"id": "markdown-content", "class": "scrollable"})
    assert markdown_content is not None

    # 驗證 contents 是否正確插入
    assert markdown_content.find("p") is not None
    assert markdown_content.find("p").getText().find("Test Content") != -1

    # 驗證 <script> 內容
    script_tag = body.find("script")
    assert script_tag is not None
    assert script_tag.text.strip() == scriptContents


def test_getRoot():
    pathI = "C:哈哈/123/456.png"
    pathII = "./666/5555/789.mp3"
    resultI = MarkdownToHtml.getRoot(pathI)
    resultII = MarkdownToHtml.getRoot(pathII)
    assert resultI == "C:哈哈/123/"
    assert resultII == "./666/5555/"

def test_get_name():
    pathI = "C:哈哈/123/456.png"
    pathII = "./666/5555/789.mp3"
    resultI = MarkdownToHtml.get_name(pathI)
    resultII = MarkdownToHtml.get_name(pathII)
    assert resultI == "456.png"
    assert resultII == "789.mp3"


def test_CatchPic():
    test_md = """
        ![測試](C:/哈哈/123/456.png)
        測試測試測試
        ![000](./666/5555/789.jpg)
        tes 
        ![5555](https://test/temp.webp)
        feefsfewef

    """
    path = "D:/test/"
    expect = {
        "C:/哈哈/123/456.png": "C:/哈哈/123/456.png",
        "./666/5555/789.jpg": "D:/test/666/5555/test/789.jpg",
    }
    result = MarkdownToHtml.CatchPic(test_md, path)
    assert len(result) == len(expect)
    for key in expect.keys():
        assert result.fromkeys(key) == expect.fromkeys(key)
