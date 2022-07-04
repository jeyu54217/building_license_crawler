import time
from pathlib import Path
from urllib import response
import requests
import base64
import json
import shutil
from selenium import webdriver

start_time = time.time()  # timer


SOURCE_URL_1 = "https://building-management.publicwork.ntpc.gov.tw/bm_query.jsp?rt=3"
SOURCE_URL_2 = "https://building-management.publicwork.ntpc.gov.tw/bm_list.jsp"

# CHROME_DRIVER_PATH = f"{Path(__file__).resolve().parent}\chromedriver.exe"
OCR_PIC_PATH = 'C:\\Users\\Administrator\Desktop\\image.jpg'

# def get_cookie():
#     HEADERS = { 
#        'user-agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
#        'Host': 'building-management.publicwork.ntpc.gov.tw',
#        'Referer': 'https://building-management.publicwork.ntpc.gov.tw/bm_query.jsp?rt=3',
#       }
#     rsp = requests.get(
#         SOURCE_URL_1,
#         headers = HEADERS,
#         )
#     cookies_1 = rsp.cookies['TS01983ad5']
#     cookies_2 = rsp.cookies['pcLevinSid'] 
    
#     return (cookies_1 , cookies_2)
    
    
def download_ocr_pic():


    pic_url ='https://building-management.publicwork.ntpc.gov.tw/ImageServlet'
    
    req = requests.session()
    get_rsp = req.get(
        pic_url,
        stream = True,
        verify = False,
        )
    
    if get_rsp.status_code == 200:
        with open("C:\\Users\\Administrator\\Desktop\\image.jpg", 'wb') as f:
            f.write(get_rsp.content)
            f.close()
            
        with open(OCR_PIC_PATH, 'rb') as pic_file:
            ocr_img64 = base64.b64encode(pic_file.read())

        params = {
            "username": "%s" % 'ctbc_china_biz1',
            "password": "%s" % 'ctbcbank',
            "captchaData": ocr_img64,
            "captchaType": 1001,
            }
        
        post_ocr_rsp = req.post("http://www.bingtop.com/ocr/upload/", data = params)
        dictdata = json.loads(post_ocr_rsp.text)
        ocr_code = dictdata['data']['recognition']
        
        
        PAYLOAD = {
            'rt': 'BM',
            'PagePT': 0,
            'A2': 3,
            'F1':'1090102', # Date
            'Z1': int(ocr_code),  # OCR code
            }
    
        post_rsp = req.post(
            SOURCE_URL_2,
            data = PAYLOAD,
            verify = False,
            ).text  
        
        print(post_rsp)
        
        

    

    
    # with open(self.captcha_path, 'wb') as file:
    #         file.write(base64.b64decode(img_base64))
    #         file.close()
            # captcha_result = self.get_ocr_result(self.captcha_path, 1001)
            # return captcha_result

# 冰拓_OCR : https://www.bingtop.com/
def ocr_post(triger):
    if triger == 'ok':
        with open(OCR_PIC_PATH, 'rb') as pic_file:
            ocr_img64 = base64.b64encode(pic_file.read())

        params = {
            "username": "%s" % 'ctbc_china_biz1',
            "password": "%s" % 'ctbcbank',
            "captchaData": ocr_img64,
            "captchaType": 1001,
            }
    
        response = requests.post("http://www.bingtop.com/ocr/upload/", data = params)
        dictdata = json.loads(response.text)
        ocr_code = dictdata['data']['recognition']
        return ocr_code

    
def main_crawler(ocr_code):
    # HEADERS = { 
    #    'user-agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    #    'Host': 'building-management.publicwork.ntpc.gov.tw',
    #    'Referer': 'https://building-management.publicwork.ntpc.gov.tw/bm_query.jsp?rt=3',
    #    'Cookie': f'pcLevinSid={cookies[0]}; TS01983ad5={cookies[1]}',
    #    'Origin': 'https://building-management.publicwork.ntpc.gov.tw',
    #   }
    
    PAYLOAD = {
        'rt': 'BM',
        'PagePT': 0,
        'A2': 3,
        'F1':'1090102', # Date
        'Z1': int(ocr_code),  # OCR code
        }
    
    response = requests.post(
        SOURCE_URL_2,
        # headers = HEADERS,
        data = PAYLOAD,
        verify = False,
        ).text  
            
    print(response)
    
if __name__ == '__main__':
    
    # keyword = '中國信託'
    # cookies = get_cookie()
    
    # triger = download_ocr_pic()
    # ocr_code = ocr_post(triger)
    # main_crawler(ocr_code)
    # download_ocr_pic()
    
    import pandas as pd
    from datetime import date
    start_date = date(2008, 8, 15) 
    end_date = date(2008, 9, 15)    # perhaps date.now()

    print(pd.date_range(start = start_date, end = end_date).strftime('%Y%m%d').tolist())
    



    # start_date = date(2008, 8, 15) 
    # end_date = date(2008, 9, 15)    # perhaps date.now()

    # delta = end_date - start_date   # returns timedelta

    # print( [start_date + timedelta(days=i) for i in range(delta.days + 1)][3])
    
    
        # day = start_date + timedelta(days=i)
        # print(day)


# for date diff
    # from datetime import date
    
    # request.POST.getlist('date_ary[]')[0]
    
    # year_0 = '1992'
    # year_1 = '1992'
    # month_0 = int(month.replace('0','')) if month[0]=='0' else int(month)
    # month_1 = int(month.replace('0','')) if month[0]=='0' else int(month)
    # day_0 = int(month.replace('0','')) if month[0]=='0' else int(month)
    # day_1 = int(month.replace('0','')) if month[0]=='0' else int(month)
    
    # d0 = date(2017,  , 18)
    # d1 = date(2017, 10, 26)
    # delta = d1 - d0
    # print(delta.days)


print("Cost：" + str(time.time() - start_time) + " s")

