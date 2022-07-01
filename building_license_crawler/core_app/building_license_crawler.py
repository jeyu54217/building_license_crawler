import time
from pathlib import Path
import requests
import base64
import json
from selenium import webdriver

start_time = time.time()  # timer


SOURCE_URL_1 = "https://building-management.publicwork.ntpc.gov.tw/bm_query.jsp?rt=3"
SOURCE_URL_2 = "https://building-management.publicwork.ntpc.gov.tw/bm_list.jsp"

# CHROME_DRIVER_PATH = f"{Path(__file__).resolve().parent}\chromedriver.exe"
OCR_PIC_PATH = 'C:\\Users\\Administrator\Desktop\\image.jpg'

def get_cookie():
    HEADERS = { 
       'user-agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
       'Host': 'building-management.publicwork.ntpc.gov.tw',
       'Referer': 'https://building-management.publicwork.ntpc.gov.tw/bm_query.jsp?rt=3',
      }
    rsp = requests.get(
        SOURCE_URL_1,
        headers = HEADERS,
        )
    cookies_1 = rsp.cookies['TS01983ad5']
    cookies_2 = rsp.cookies['pcLevinSid'] 
    
    return (cookies_1 , cookies_2)
    
    
def download_ocr_pic():
    # browser = webdriver.Chrome(CHROME_DRIVER_PATH,)
    # browser.get(SOURCE_URL)
    # img_base64 = browser.execute_script(
    #     """
    #     var ele = arguments[0];
    #     var cnv = document.createElement('canvas'); canvas
    #     cnv.width = 252;
    #     cnv.height = 72;
    #     cnv.getContext('2d').drawImage(ele, 0, 0);
    #     return cnv.toDataURL('image/jpeg').substring(22);
    #     """, 
    #     browser.find_element_by_xpath(
    #         "//*[@id=\"realPic\"]"
    #         )
    #     )
    
    HEADERS = { 
       'user-agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
       'Host': 'building-management.publicwork.ntpc.gov.tw',
       'Referer': 'https://building-management.publicwork.ntpc.gov.tw/bm_query.jsp?rt=3',
    #    'Cookie': f'pcLevinSid={cookies[0]}; TS01983ad5={cookies[1]}',
      }
    #  session test
    s = requests.session()
    s.headers = HEADERS
    
    
    
    pic_url ='https://building-management.publicwork.ntpc.gov.tw/ImageServlet'
    # Picture_request = requests.get(
    #     pic_url,
    #     headers = HEADERS,
    #     )
    
    Picture_request = s.get(
        pic_url,
        headers = HEADERS,
        )
    
    if Picture_request.status_code == 200:
        with open("C:\\Users\\Administrator\\Desktop\\image.jpg", 'wb') as f:
            f.write(Picture_request.content)
    s.close()
    # with open(self.captcha_path, 'wb') as file:
    #         file.write(base64.b64decode(img_base64))
    #         file.close()
            # captcha_result = self.get_ocr_result(self.captcha_path, 1001)
            # return captcha_result

# 冰拓_OCR : https://www.bingtop.com/
def ocr_post():
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

    
def main_crawler( ocr_code):
    HEADERS = { 
       'user-agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
       'Host': 'building-management.publicwork.ntpc.gov.tw',
       'Referer': 'https://building-management.publicwork.ntpc.gov.tw/bm_query.jsp?rt=3',
       'Cookie': f'pcLevinSid={cookies[0]}; TS01983ad5={cookies[1]}',
       'Origin': 'https://building-management.publicwork.ntpc.gov.tw',
      }
    
    PAYLOAD = {
        'rt': 'BM',
        'PagePT': 0,
        'A2': 3,
        'F1':'1090102', # Date
        'Z1': ocr_code,  # OCR code
        }
    
    output = requests.post(
        SOURCE_URL_2,
        headers = HEADERS,
        data = PAYLOAD,
        ).text
            
    print(output)
    
if __name__ == '__main__':
    pass
    # keyword = '中國信託'
    # cookies = get_cookie()
    
    # download_ocr_pic()
    # ocr_code = ocr_post()
    # main_crawler(ocr_code)


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

