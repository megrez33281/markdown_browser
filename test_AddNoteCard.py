import unittest
from unittest.mock import patch, mock_open
from bs4 import BeautifulSoup
from AddNoteCard import AddElement
import chardet

class TestAddElement(unittest.TestCase):

    #mock Database中的GetAllHtml function
    @patch("AddNoteCard.Database.GetAllHtml")
    #mock open() function
    @patch("builtins.open", new_callable=mock_open, read_data="<html><body><ul id='card-box-ul'></ul></body></html>")
    #mock chardet.detect，並偽造回傳結果
    @patch("chardet.detect", return_value={'encoding': 'utf-8'})
    def test_AddElement(self, mock_chardet, mock_file, mock_db):
        # 模擬資料庫返回的 HTML 元素資料
        mock_db.return_value = [
            ("id1", "name1"),
            ("id2", "name2")
        ]

        # 執行函式
        result_html = AddElement("fakepath.html")

        # 解析結果的 HTML
        soup = BeautifulSoup(result_html, "html.parser")

        # 確保 ul#card-box-ul 存在
        container = soup.find("ul", {"id": "card-box-ul"})
        self.assertIsNotNone(container)

        # 檢查是否有兩個 li 卡片
        cards = container.find_all("li", {"class": "list card"})
        self.assertEqual(len(cards), 2)

        # 檢查第一個卡片內容
        first_card = cards[0]
        title = first_card.find("h4", {"class": "card-title"}).text
        self.assertEqual(title, "name1")

        # 檢查刪除按鈕是否存在
        delete_img = first_card.find("img", {"class": "delete-img"})
        self.assertIsNotNone(delete_img)

        # 檢查 script 是否正確插入
        script_tag = soup.find("script")
        self.assertIsNotNone(script_tag)
        self.assertIn("const DeleteIcon =", script_tag.text)
