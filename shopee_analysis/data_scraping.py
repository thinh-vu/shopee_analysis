from ur_gadget import *
import pandas as pd
from pandas import json_normalize
import requests
# import time
# import json
# import io

# Shopee API request setting
def api_request(url, payload={}, method='GET'):
  """Default setting to request data from Shopee.vn"""
  headers = {
    'accept-language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-platform': '"macOS"',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'x-api-source': 'pc',
    'x-requested-with': 'XMLHttpRequest',
    'x-shopee-language': 'vi'
  }
  response = requests.request(f"{method}", url, headers=headers, data=payload)
  return response.json()

# Section name: Danh mục sản phẩm
def category_list(url='https://shopee.vn/api/v4/pages/get_category_tree'):
  """Extract the category list"""
  response = api_request(url)
  df = json_normalize(response['data']['category_list'])
  return df

# # Section name: Home > Tìm kiếm hàng đầu - Stop working due to not login
# def top_product_key (url='https://shopee.vn/api/v4/recommend/recommend?bundle=top_products_homepage&limit=50'):
#   """Return a list of top product keys which can be used to extract item details further"""
#   response = api_request(url)
#   # update_time = response['data']['update_time']
#   ls_count =len(response['data']['sections'])
#   total_item = response['data']['sections'][0]['total']
#   key_df = json_normalize(response['data']['sections'][0]['index']).drop(columns=['data_type', 'filtered', 'filtered_dunit'])
#   return key_df

# Shopee Mall index: https://shopee.vn/mall/brands
def mall_index_all(url='https://shopee.vn/api/v4/official_shop/get_shops_by_category?need_zhuyin=0&category_id=-1'):
  response = api_request(url)['data']['brands']
  ls_len = len(response)
  for i in range(ls_len):
    if i == 0:
      df = json_normalize(response[i]['brand_ids'])
      df['index'] = response[i]['index']
    else:
      df1 = json_normalize(response[i]['brand_ids'])
      df1['index'] = response[i]['index']
      df = pd.concat([df, df1])
  df['created_time'] = pd.to_datetime(df['ctime'],unit='s').dt.date
  df['logo'] = 'https://cf.shopee.vn/file/' + df['logo']
  df['created_year'] = pd.to_datetime(df['created_time']).dt.year
  df['created_month'] = pd.to_datetime(df['created_time']).dt.month
  df['created_day'] = pd.to_datetime(df['created_time']).dt.day
  df = df[['index', 'username', 'brand_name', 'shopid', 'logo', 'created_time', 'created_year', 'created_month', 'created_day']]
  return df

# Get Shop Info by Shop ID
def get_shop_info(shop_id):
  response = api_request(f"https://shopee.vn/api/v4/product/get_shop_info?shopid={str(shop_id)}")
  df = json_normalize(response['data'])
  df['created_time'] = pd.to_datetime(df['ctime'], unit='s').dt.date
  df = df[['shopid', 'name', 'shop_location', 'item_count', 'rating_star', 'response_rate',
          'response_time', 'follower_count', 'rating_bad', 'rating_good',
          'rating_normal', 'is_shopee_verified','is_preferred_plus_seller', 'is_official_shop', 'created_time']]
  return df



