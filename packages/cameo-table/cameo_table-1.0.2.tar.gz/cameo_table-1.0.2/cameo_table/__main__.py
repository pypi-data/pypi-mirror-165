import cameo_table

def main():
    n = input('選擇想要的功能 輸入1:挑選出指定欄位為某值的所有列 輸入2:將直欄轉換為橫向資料 輸入3:將橫向資料轉換為直欄資料 輸入0:離開\n')
    while(n!='0'):
        if(n=='1'):
            print('已選功能1:挑選出指定欄位為某值的所有列')
            path, col_to_apply_on, value, result_path = input('以空白隔開 請依序輸入:要處理的檔名(路徑/url) 指定值所在的欄位 指定的值 輸出的檔名(路徑)\n').split(' ')
            try:
                cameo_table.pick(path, col_to_apply_on, value, result_path)
            except Exception as e:
                print(e)
        elif(n=='2'):
            print('已選功能2:將直欄轉換為橫向資料')
            path, col_to_apply_on, value, result_path = input('以空白隔開 請依序輸入:要處理的檔名(路徑/url) 轉換為欄位標題的欄位 對應值所在的欄位 輸出的檔名(路徑)\n').split(' ')
            try:
                cameo_table.pivot(path, col_to_apply_on, value, result_path)
            except Exception as e:
                print(e)
        elif(n=='3'):
            print('已選功能3:將橫向資料轉為直欄資料')
            data, value_vars, variable_name, value_name, filepath = input('以空白隔開 請依序輸入:要處理的檔名(路徑/url) 要合併為直欄的欄位(以逗號隔開) 合併後直欄的欄位標題 合併後值的欄位標題 輸出的檔名(路徑)\n').split(' ')
            try:
                cameo_table.melt(data=data, value_vars=value_vars, variable_name=variable_name, value_name=value_name, filepath=filepath)
            except Exception as e:
                print(e)
        n = input('選擇想要的功能 輸入1:挑選出指定欄位為某值的所有列 輸入2:將直欄轉換為橫向資料 輸入0:離開\n')

if __name__ == '__main__':
    main()