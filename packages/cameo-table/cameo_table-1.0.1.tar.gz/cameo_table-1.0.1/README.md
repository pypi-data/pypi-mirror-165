# 安裝(installation)
```
pip install cameo_table
```
# CLI 使用(CLI Usage (Chinese Only) )
```
python -m cameo_table
```
選擇想要的功能  
輸入1:挑選出指定欄位為某值的所有列  
輸入2:將直欄轉換為橫向資料  
輸入0:離開  
## 輸入1:挑選出指定欄位為某值的所有列
以空白隔開 請依序輸入:  
要處理的檔名(路徑/url)  
指定值所在的欄位  
指定的值  
輸出的檔名(路徑)
```
path/to/original/file column_to_find_value value path/to/result/file
```
### 舉例 (example)
原始檔案內容 (orginal file content)
|other_data|column_to_find_value|
|:-:|:-:|
|a|1|
|b|2|
|c|3|
|d|1|
|e|2|
|f|3|

在終端機輸入以下參數 (input following arguments to terminal)
```
> python -m cameo_table
選擇想要的功能 輸入1:挑選出指定欄位為某值的所有列 輸入2:將直欄轉換為橫向資料 輸入0:離開
1
已選功能1:挑選出指定欄位為某值的所有列
以空白隔開 請依序輸入:要處理的檔名(路徑/url) 指定值所在的欄位 指定的值 輸出的檔名(路徑)
path/to/original/file column_to_find_value 3 path/to/result/file
```
結果檔案內容 (result file content)
|other_data|column_to_find_value|
|:-:|:-:|
|c|3|
|f|3|
## 輸入2:將直欄轉換為橫向資料
以空白隔開  請依序輸入:
要處理的檔名(路徑/url)  
轉換為欄位標題的欄位  
傳換為對應值的欄位  
輸出的檔名(路徑)
```
path/to/original/file column_to_transform_as_column_label column_to_transform_as_value path/to/result/file
```
### 舉例 (example)
原始檔案內容 (orginal file content)  
|other_data|label|value|
|:-:|:-:|:-:|
|A|a|1|
|A|b|2|
|A|c|3|
|B|a|4|
|B|b|5|
|C|b|6|

在終端機輸入以下參數 (input following arguments to terminal)
```
> python -m cameo_table
選擇想要的功能 輸入1:挑選出指定欄位為某值的所有列 輸入2:將直欄轉換為橫向資料 輸入0:離開
2
已選功能2:將直欄轉換為橫向資料
以空白隔開 請依序輸入:要處理的檔名(路徑/url) 轉換為欄位標題的欄位 對應值所在的欄位 輸出的檔名(路徑)
path/to/original/file label value path/to/result/file
```
結果檔案內容 (result file content)
|other_data|a|b|c|
|:-:|:-:|:-:|:-:|
|A|1|2|3|
|B|4|5||
|C||6||
# Python 使用 (Python usage)
## 引入函式庫 (import module)
```
import cameo_table
```
## cameo_table.pick_row_contain_certain_value()
```
cameo_table.pick_rows_contain_certain_value(
    path: str or df,
    col_to_apply_on: str,
    value,
    result_path: str
)
```
### 參數 (arguments):  
|參數名<br />(Name)|類型<br />(Type)|意義<br />(Meaning)|
|:-:|:-:|:-:|
|path|str|待處理檔案的路徑<br />(path of the file to handle with)|
||DataFrame|待處理的DataFrame<br />(DataFrame to handle with)|
|col_to_apply_on|str|要找到某值的欄位名稱<br />(name of the column to find value)
|value|-|在某欄要找到的值<br />(value to be picked in the column)|
|result_path|str|結果檔案的路徑<br />(path to the result file)

### 舉例 (example)
原始檔案內容 (orginal file content)
|other_data|column_to_find_value|
|:-:|:-:|
|a|1|
|b|2|
|c|3|
|d|1|
|e|2|
|f|3|

使用以下程式碼 (use following codes)
```
import cameo_table
cameo_table.pick_rows_contain_certain_value(
    path = 'path/to/original/file',
    col_to_apply_on = 'column_to_find_value',
    value = 3,
    result_path = 'path/to/result/file')
```
結果檔案內容 (result file content)
|other_data|column_to_find_value|
|:-:|:-:|
|c|3|
|f|3|
## cameo_table.turn_vertical_to_horizontal()
```
cameo_table.turn_vertical_to_horizontal(
    path: str or df,
    col_to_apply_on: str,
    value,
    result_path: str
)
```
### 參數 (arguments):  
|參數名<br />(Name)|類型<br />(Type)|意義<br />(Meaning)|
|:-:|:-:|:-:|
|path|str|待處理檔案的路徑<br />(path of the file to handle with)|
||DataFrame|待處理的DataFrame<br />(DataFrame to handle with)|
|col_to_apply_on|str|要轉換成欄位標題的欄位<br />(column to transform as column label)
|value|str|轉換為對應值的欄位<br />(column_to_transform_as_value)|
|result_path|str|結果檔案的路徑<br />(path to the result file)

### 舉例 (example)
原始檔案內容 (orginal file content)  
|other_data|label|value|
|:-:|:-:|:-:|
|A|a|1|
|A|b|2|
|A|c|3|
|B|a|4|
|B|b|5|
|C|b|6|

使用以下程式碼 (use following codes)
```
import cameo_table
cameo_table.turn_vertical_to_horizontal(
    path = 'path/to/original/file',
    col_to_apply_on = 'label',
    value = 'value',
    result_path = 'path/to/result/file')
```
結果檔案內容 (result file content)
|other_data|a|b|c|
|:-:|:-:|:-:|:-:|
|A|1|2|3|
|B|4|5||
|C||6||