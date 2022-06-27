import time
import requests

start_time = time.time()  # timer

def  main_crawler(keyword):
    SOURCE_URL = "https://building-management.publicwork.ntpc.gov.tw/bm_query.jsp"
    HEADERS = { 
       'user-agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
       'Host': 'building-management.publicwork.ntpc.gov.tw',
       'Referer': 'https://www.104.com.tw/',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.',
    }

    source_json_dict = requests.get(
        SOURCE_URL,
        headers = HEADERS
        ).json()

    item_counts_num/total_page_num 
   

    if total_page_num :
        result_dict = {
            "multi_matched" : {
                "comp_id_list" : [],
                "comp_name_list" : [],
                "comp_address_list" : [],
                "comp_status_list" : [],
                }
            }
        for page in range(1, total_page_num):
            json_dict = requests.get(
                API_URL + f"search?q={keyword}&page={page}",
                headers = HEADERS,
                ).json()    
            for i in range(0, items_per_page):
                # "行號"與"公司"分別使用不同KEY搜尋 : ['商業名稱'] v.s. ['公司名稱']
                # 排除"行號"與"非核准設立"
                if '公司名稱' in multi_json_dict['data'][i] and '核准設立' in multi_json_dict['data'][i]['公司狀況']:
                    # List to List : extend
                    # String to List : append
                    multi_match_dict["multi_matched"]["comp_id_list"].append(multi_json_dict['data'][i]['統一編號'])
                    multi_match_dict["multi_matched"]["comp_name_list"].append(multi_json_dict['data'][i]['公司名稱'])
                    multi_match_dict["multi_matched"]["comp_address_list"].append(multi_json_dict['data'][i]['公司所在地'].replace('\xa0', ''))
                    multi_match_dict["multi_matched"]["comp_status_list"].append(multi_json_dict['data'][i]['公司狀況'])
                else:
                    continue

        return result_dict 
    else:
        pass

    
# if __name__ == '__main__':
#     keyword = '中國信託'
#     print(g0v_crawler(keyword))


print("Cost：" + str(time.time() - start_time) + " s")