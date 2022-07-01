from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Real_estate_raw, Request_list, Querry_list, G0v_matched_data
import cn2an
import time
 
# for email
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template

# for date diff
# from datetime import date


# d0 = date(2017, 8, 18)
# d1 = date(2017, 10, 26)
# delta = d1 - d0
# print(delta.days)


# request
# models querry set
def home_page(request):
    return render(request,"search_page.html")
    # return render(request,"detail_page.html")
    # return render(request,"end_page.html")
    # return render(request,"g0v_result_page.html")

@csrf_exempt
def search_real_estate(request):
    '''
      1) get date from js post
      2) create Request_list
      3) filter Real_estate_raw by given date
      4) create Querry_list 
      5) render result Querry_list
    '''
    if request.method == 'POST':
      # get date from  js post
        start_date_from_js = request.POST.getlist('date_ary[]')[0]
        end_date_from_js = request.POST.getlist('date_ary[]')[1]
      # create Request_list
        rqs_now = Request_list.objects.create(
            start_date = start_date_from_js, 
            end_date = end_date_from_js,
            )
      # filter Real_estate_raw by date
        selected_objs = Real_estate_raw.objects.filter(
          transaction_date__range = [start_date_from_js, end_date_from_js]
          )
      # create Querry_list by date
        for obj in selected_objs:
            Querry_list.objects.create(
                request_id_id = rqs_now.request_id,
                title = '時價登錄 不動產交易',
                transaction_date = obj.transaction_date,
                address = obj.address,
                sale_price = obj.sale_price,
                shifting_area = obj.shifting_area,
                building_state = obj.building_state,
                usage = obj.usage,
                total_floor_number = obj.total_floor_number,
                shifting_floor_number = obj.shifting_floor_number,
                building_age = obj.build_date,
                notes = obj.notes,
                )
          
        # obj_list = []
        # for obj in selected_objs:
        #     _obj = Querry_list(
        #         request_id = rqs_now.request_id,
        #         title = '時價登錄 不動產交易',
        #         transaction_date = obj.transaction_date,
        #         address = obj.address,
        #         sale_price = obj.sale_price,
        #         shifting_area = obj.shifting_area,
        #         building_state = obj.building_state,
        #         usage = obj.usage,
        #         total_floor_number = obj.total_floor_number,
        #         shifting_floor_number = obj.shifting_floor_number,
        #         notes = obj.notes,
        #         )
        #     obj_list.append(_obj)
        # Querry_list.objects.bulk_create(obj_list, batch_size = 100)
        
  # render result Querry_list
    latest_rqs_id = Request_list.objects.latest('request_id')
    result_list = Querry_list.objects.filter(request_id_id = latest_rqs_id)
    context = {
      'result_list' :result_list
      }
    return render(request, "result_page.html", context) 
  
    
@csrf_exempt
def detail_page(request):
    '''
    1.
      1) get post id from into/delete botton in result_page
      2) embed floor_num_translator
      3) querry from Querry_list filter by js post list 
    2.
      1) get list(True or False) from js post
      2) Insert to Querry_list
      3) render Querry_list
    '''
    get_into_id = request.POST.get('into')
    get_del_id = request.POST.get('delete')
    get_checkbox_id = request.POST.get('checkbox')
    
    if get_into_id:
          into_obj = Querry_list.objects.get(id = get_into_id)
          
        # floor num translation
          address_raw = into_obj.address
          address_cn2num = cn2an.transform(address_raw, "cn2an")
          address_num2cn = cn2an.transform(address_raw, "an2cn")
              
        # House age translation
          building_age_raw = into_obj.building_age
          house_age = str(int(time.strftime("%Y")) - 1911 - int(building_age_raw[0:3])) if building_age_raw and len(building_age_raw) == 7 else ''
          
          context = {
              'get_into_id' : get_into_id,
              'into_obj' : into_obj,
              'address_cn2num' : address_cn2num,
              'address_num2cn' : address_num2cn,
              'house_age' : house_age,
              }
          return render(request,"detail_page.html", context)
      
    if get_del_id:
        # del_obj = Querry_list.objects.get(id = get_del_id)
        update_del =  Querry_list.objects.filter(id = get_del_id).update(finished = 1)
        latest_rqs_id = Request_list.objects.latest('request_id')
        result_list = Querry_list.objects.filter(request_id_id = latest_rqs_id)
        context = {
          'result_list' :result_list
          }
        return render(request,"result_page.html", context)
      
    if get_checkbox_id:
        update_related_person = Querry_list.objects.filter(id = get_checkbox_id).update(related_person_transaction = 1)
        latest_rqs_id = Request_list.objects.latest('request_id')
        result_list = Querry_list.objects.filter(request_id_id = latest_rqs_id)
        context = {
              'result_list' :result_list
              }
        return render(request,"result_page.html", context)
  
@csrf_exempt
def search_g0v(request):
    keyword_list = request.POST.getlist('kwyword_ary[]')
    Querry_list_id =  request.POST.get('id_ary[]')
    
    if keyword_list:
      for keyword in keyword_list:
          search_result = g0v_crawler.g0v_crawler(keyword)
          if search_result == "No Company Found":
            continue
          # elif search_result['one_time_matched']:
          #     G0v_matched_data.objects.create(
          #       querry_id_id = Querry_list_id,
          #       comp_id = search_result['one_time_matched']['comp_id'],
          #       comp_name = search_result['one_time_matched']['comp_name'],
          #       comp_address = search_result['one_time_matched']['comp_address'],
          #       comp_status = search_result['one_time_matched']['comp_status'],
          #       )
          # elif search_result == '該行為人非為公司組織, 或該公司非屬核准設立中':
          #   continue
          elif search_result['multi_matched']:
            for i in range(0, len(search_result['multi_matched']['comp_id_list'])):
              G0v_matched_data.objects.update_or_create(
                querry_id_id = Querry_list_id,
                comp_id = search_result['multi_matched']['comp_id_list'][i],
                comp_name = search_result['multi_matched']['comp_name_list'][i],
                comp_address = search_result['multi_matched']['comp_address_list'][i],
                comp_status = search_result['multi_matched']['comp_status_list'][i],
                )
          else:
            continue
    latest_querry_list_id = G0v_matched_data.objects.latest('querry_id_id').querry_id_id
    result_list = G0v_matched_data.objects.filter(querry_id_id = latest_querry_list_id)
    Querry_list_obj = Querry_list.objects.get(id = latest_querry_list_id)
    context = {
      'result_list' : result_list,
      'Querry_list_obj' : Querry_list_obj,
      
      }
    return render(request,"g0v_result_page.html", context)
  
    
@csrf_exempt
def send_email(request): 
    comp_id_list_raw =  request.POST.getlist('checked_ary[]')
    comp_id_list = [id.replace('checkbox_','') for id in comp_id_list_raw]
    
    latest_querry_list_id = G0v_matched_data.objects.latest('querry_id_id').querry_id_id
    Querry_list_obj = Querry_list.objects.get(id = latest_querry_list_id)
    
    for id in comp_id_list:
        G0v_matched_data.objects.filter(comp_id = id).update(send_mail = 1)
    g0v_objs_to_send = G0v_matched_data.objects.filter(querry_id_id = latest_querry_list_id).filter(send_mail = 1)
    
    
   #  House age translation
    building_age_raw = Querry_list_obj.building_age
    house_age = str(int(time.strftime("%Y")) - 1911 - int(building_age_raw[0:3])) if building_age_raw and len(building_age_raw) == 7 else ''
          

    template = get_template('mail_page.html')
    template_tag = {
      'g0v_objs_to_send': g0v_objs_to_send,
      'Querry_list_obj' : Querry_list_obj,
      'house_age' : house_age,
        }
    html_content = template.render(template_tag)
    
    subject = '實價登錄商機'
    message = ''

    mail = EmailMultiAlternatives(
        subject, 
        message, 
        settings.EMAIL_HOST_USER, 
        ['jeyu54217@gmail.com'], # reciver
        )
    mail.attach_alternative(html_content, "text/html")
    mail.send()

    latest_rqs_id = Request_list.objects.latest('request_id')
    result_list = Querry_list.objects.filter(request_id_id = latest_rqs_id)
    context = {
              'result_list' :result_list
              }

    return render(request,"result_page.html", context)
  
    