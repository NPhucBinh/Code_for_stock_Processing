import requests
import time
import pandas as pd
import json
from datetime import datetime


__author__ = ["Nguyen Phuc Binh"]
__copyright__ = "Copyright 2022, NPhucBinh"
__license__ = "MIT"
__email__ = "nguyenphucbinh67@gmail.com"
__website__ = "https://nphucbinh.github.io"

'''
You can receive notifications about the change of the vnindex if there is a change. By using IFTTT and Telegarm
'''
vni_url = 'https://banggia.cafef.vn/stockhandler.ashx?index=true'
ifttt_webhook_url = 'https://maker.ifttt.com/trigger/bandemo5/json/with/key/b4tvC8Kz8svIvSWR8mhXUU' ### Your IFTTT link
#remak = requests.post(ifttt_webhook_url)
def get_vni_url():
  re_vni_url = requests.get(vni_url)
  results_vni = json.loads(re_vni_url.text)
  core = results_vni[1]
  dal = dict(core)
  row_labels = [1]
  #datla = print("Tên chỉ số:", dal['name'], "Chỉ số:", dal['index'],"Thay đổi:", dal['change'],"Độ lệch:", dal['percent'],"Khối lượng:", dal['volume'],"Giá trị giao dịch thị trường:", dal['value'])
  datla = pd.DataFrame(data=dal, index=row_labels)
  return datla

def post_ifttt_webhook(event, value):
  #data = {'value1': value}
  ifttt_event_url = ifttt_webhook_url.format(event)
  requests.post(ifttt_event_url, json = {"value1": get_vni_url()})

def format_vnindex_historical(vnindex_historical):
    rows = []
    for vnindex_price in vnindex_historical:
        date = vnindex_price['date'].strftime('%d.%m.%Y %H:%M')
        price = vnindex_price['price']
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)
    return '</b>'.join(rows)

def main():
    vnindex_historical = []
    while True:
        price = get_vni_url()
        date = datetime.now()
        vnindex_historical.append({'date':date, 'price':price})
        
        if len(vnindex_historical) == 5:
           post_ifttt_webhook('vnindex_update', format_vnindex_historical(vnindex_historical))
           vnindex_historical = []
           time.sleep(300)
        
if __name__ == '__main__':
  main()