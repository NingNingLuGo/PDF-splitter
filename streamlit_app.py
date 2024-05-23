import streamlit as st
from pyecharts.charts import Kline
from pyecharts import options as opts
import pandas as pd
import tushare as ts
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.charts import Kline
import streamlit_echarts


# 设置tushare的token，需要先去tushare官网注册获取
ts.set_token('937bd93c07d2b4f44bdbb7982e57148fa710ba291abdd00aace96edf')

# 获取股票数据
def get_stock_data(stock_code, start_date, end_date):
    pro = ts.pro_api()
    df_stock = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
    return df_stock

# 创建一个示例的K线图
def kline_chart(df):
    dates = df.index.strftime('%Y-%m-%d').tolist()
    data = df[['open', 'close', 'low', 'high']].values.tolist()

    # 计算5日和10日的移动平均线
    df['MA5'] = df['close'].rolling(window=5).mean()
    df['MA10'] = df['close'].rolling(window=10).mean()
    df['MA30'] = df['close'].rolling(window=30).mean()

    kline = (
        Kline()
        .add_xaxis(dates)
        .add_yaxis("K线图", data)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(is_scale=True),
            title_opts=opts.TitleOpts(title="K线图示例"),
        )
    )

    line = (
        Line()
        .add_xaxis(xaxis_data=dates)
        .add_yaxis(
            series_name="MA5",
            y_axis=df['MA5'],
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(width=2),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show=False
        )
        .add_yaxis(
            series_name="MA10",
            y_axis=df['MA10'],
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(width=2),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show=False
        )
        .add_yaxis(
            series_name="MA30",
            y_axis=df['MA30'],
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(width=2),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show=False
        )
    )

    kline.overlap(line)

    return kline


# Streamlit应用程序
def main():
    st.title('K线图展示')

    stock_code = st.text_input('请输入股票代码（例如：600519.SH）',value='600519.SH')

    default_start_date = pd.Timestamp(year=2024, month=1, day=1)

    start_date = st.date_input('开始日期', value=default_start_date)
    end_date = st.date_input('结束日期')

    data = None  # 初始化 data 变量

    if st.button('获取数据'):
        if stock_code:
            data = get_stock_data(stock_code, start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d'))
            data = data.set_index('trade_date')
            data.index = pd.to_datetime(data.index)
            data = data.sort_index()


    if data is not None:  # 只有在 data 不为 None 时才调用 kline_chart 函数
        kline = kline_chart(data)
        streamlit_echarts.st_pyecharts(kline,height=400)  # 直接渲染 Pyecharts 图表

if __name__ == '__main__':
    main()
