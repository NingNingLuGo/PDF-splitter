# 导入所需的库
import tushare as ts
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

# 填入tushare的token
pro = ts.pro_api('937bd93c07d2b4f44bdbb7982e57148fa710ba291abdd00aace96edf')

# 定义一个股票代码的列表
stock_codes = ['601318.SH', '600036.SH', '600519.SH']

# 定义一个空的列表来存储DataFrame
data_list = []

# 遍历股票代码列表，通过tushare api获取股票数据
for stock in stock_codes:
    data = pro.daily(ts_code=stock)
    data_list.append(data)

# 按行合并数据
combined_data = pd.concat(data_list)

# 重置索引
combined_data = combined_data.reset_index(drop=True)

# 增加'company'列
combined_data['company'] = np.nan

# 设置字典，提供股票代码和公司名称的映射关系
company_dict = {'601318.SH':'中国平安','600036.SH':'招商银行','600519.SH':'茅台集团'}

# 遍历字典，将对应的公司名称填入'company'列
for key in company_dict:
    combined_data.loc[combined_data['ts_code']==key, 'company'] = company_dict[key]

# 将'trade_date'设置为日期时间格式
combined_data['trade_date'] = pd.to_datetime(combined_data['trade_date'])

# 创建Streamlit应用
st.title('股票收盘价图表')

# 添加按钮选择log或linear
y_axis_type = st.radio("Y轴类型:", ['log', 'linear'])

# 绘制股票收盘价的图表
fig = px.line(combined_data, x='trade_date', y='close', color='company', title='股票收盘价')
if y_axis_type == 'log':
    fig.update_yaxes(type='log')
else:
    fig.update_yaxes(type='linear')

st.plotly_chart(fig)