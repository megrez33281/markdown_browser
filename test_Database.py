import pytest
import Database
from unittest import mock

@mock.patch("Database.sqlite3.connect")    # 建立一個連線資料庫的mock
def test_initial_database(mocker):
    
    # 建立假的cusor以及conn
    mock_conn = mocker.MagicMock()
    mock_cursor = mocker.MagicMock()
    
    # 將mock的回傳值設為mock_conn
    mocker.return_value = mock_conn
    # 修改conn.cursor()的回傳值
    mock_conn.cursor.return_value = mock_cursor

    # 執行測試
    # 此時Database中的squlie3.connect已被mock替換
    Database.InitialDatabase()

    # 確保 `sqlite3.connect()` 被呼叫一次，且為指定路徑
    mocker.assert_called_once_with("./MarkdownData.db")

    # 確保 `cursor.execute()` 被正確呼叫
    mock_cursor.execute.assert_called_once_with('''
        CREATE TABLE IF NOT EXISTS markdowns (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            html TEXT NOT NULL
        )
    ''')

@mock.patch("Database.sqlite3.connect") 
def test_ExecuteCommand(mocker):
    # 建立假的cusor以及conn
    mock_conn = mocker.MagicMock()
    mock_cursor = mocker.MagicMock()
    # 將mock的回傳值設為mock_conn，即替換在Database.py中使用的sqlite3.connect
    mocker.return_value = mock_conn
    # 修改conn.cursor()的回傳值
    mock_conn.cursor.return_value = mock_cursor
    command = "test"
    Database.ExecuteCommand(command)
    # 確保呼叫的路徑正確
    # 檢查在Database中sqlite3.connect是否只被呼叫了一次，並且路徑正確
    mocker.assert_called_once_with("./MarkdownData.db")
    mock_cursor.execute.assert_called_once_with(command)
    # 檢查commit以及close是否有執行
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


@mock.patch("Database.sqlite3.connect") 
def test_QueryCommand(mocker):
    # 建立假的cusor以及conn
    mock_conn = mocker.MagicMock()
    mock_cursor = mocker.MagicMock()
    # 將mock的回傳值設為mock_conn，即替換在Database.py中使用的sqlite3.connect
    mocker.return_value = mock_conn
    # 修改conn.cursor()的回傳值
    mock_conn.cursor.return_value = mock_cursor
    # 模擬fetchall()的回傳
    mock_cursor.fetchall.return_value = ["test"]

    command = "test"
    Database.QueryCommand(command)
    # 確保呼叫的路徑正確
    # 檢查在Database中sqlite3.connect是否只被呼叫了一次，並且路徑正確
    mocker.assert_called_once_with("./MarkdownData.db")
    mock_cursor.execute.assert_called_once_with(command)
    mock_cursor.fetchall.assert_called_once()
    
    # 檢查commit以及close是否有執行
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

    
def test_MakeString():
    tests = [122, "哈哈", 1.2]
    assert Database.MakeString(tests[0])  == "'122'"
    assert Database.MakeString(tests[1])  == "'哈哈'"
    assert Database.MakeString(tests[2])  == "'1.2'"

def test_MakeString_Error():
    with pytest.raises(Exception) as error:
        result = Database.MakeString(None)
    assert str(error.value) == '輸入的a_str不存在'


@mock.patch("Database.sqlite3.connect") 
def test_InsertMarkdown(mocker):
    # 建立假的cusor以及conn
    mock_conn = mocker.MagicMock()
    mock_cursor = mocker.MagicMock()
    # 將mock的回傳值設為mock_conn，即替換在Database.py中使用的sqlite3.connect
    mocker.return_value = mock_conn
    # 修改conn.cursor()的回傳值
    mock_conn.cursor.return_value = mock_cursor
    # 模擬fetchall()的回傳
    mock_cursor.fetchall.return_value = ["test"]

    # 偽造從資料庫中取得的資料
    md_id = 10206262 
    html_name = "測試測試" 
    html = "fd4f8e4sf84esf4e8sfe4s8es4f8es4f8es4fes8f4esf84es"
    html_byte = html.encode("utf-8") 
    Database.InsertMarkdown(md_id, html_name, html_byte)

    # 確保呼叫的路徑正確
    # 檢查在Database中sqlite3.connect是否只被呼叫了一次，並且路徑正確
    mocker.assert_called_once_with("./MarkdownData.db")
    mock_cursor.execute.assert_called_once_with('INSERT INTO markdowns (id, name, html) VALUES (?, ?, ?)', (str(md_id), html_name, html_byte))
    # 檢查commit以及close是否有執行
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

@mock.patch("Database.QueryCommand") #替代Database中的QueryCommand
def test_GetHtml(mocker):
    mocker.return_value = [["html name", "html"]]
    name, html = Database.GetHtml("1234567")
    mocker.assert_called_once_with("select name, html from markdowns where id = '1234567'")
    assert name == "html name" and html == "html"


@mock.patch("Database.QueryCommand") #替代Database中的QueryCommand
def test_GetHtml_No_Html(mocker):
    # 測試資料庫中沒有對應檔案的情況
    mocker.return_value = []
    name, html = Database.GetHtml("1234567")
    mocker.assert_called_once_with("select name, html from markdowns where id = '1234567'")
    assert name == '' and html == ''



@mock.patch("Database.QueryCommand") #替代Database中的QueryCommand
def test_GetAllHtml(mocker):
    mocker.return_value = [
        ["123", "name1"],
        ["456", "name2"],
        ["789", "name3"]
    ]
    Database.GetAllHtml()
    mocker.assert_called_once_with("select id, name from markdowns")


@mock.patch("Database.ExecuteCommand") #替代Database中的ExecuteCommand
def test_DeleteHtml(mocker):
    Database.DeleteHtml("123456789")
    mocker.assert_called_once_with("delete from markdowns where id = '123456789'")

@mock.patch("Database.ExecuteCommand") #替代Database中的ExecuteCommand
def test_clear(mocker):
    Database.clear()
    mocker.assert_called_once_with("delete from markdowns")