import csv

import pandas
from pyecharts import options as opts
from pyecharts.charts import Map, Bar, Pie, Grid
from pyecharts.globals import ThemeType

"""打开文件读取数据"""
provinces_data = pandas.read_excel(r'./data/总人口.xls')
provinces = list(provinces_data['地区'])
data_list = []
for province in provinces:
    with open(rf'./data/txt/{province}.txt', 'r', encoding='utf-8') as f:
        data = csv.reader(f)
        for row in data:
            data_list.append(row)
'''数据格式装换'''
temp_data = []
data_dict = {}
list = []
for index in data_list:
    if len(index) > 2:
        for row in range(0, len(index), 2):
            city = index[row]
            population = int(index[row + 1])
            print(f'city:{index[row]},population:{int(index[row + 1])}')
            list.append((city, population))
    else:
        list.append((index[0], int(index[1])))
    temp_data.append(list)
    list = []

for index in temp_data:
    province = index[1:]
    data_dict.setdefault(index[0][0][:-1], province)
'''Map地图'''
for k, v in data_dict.items():
    province = k
    if k[:2] in ['新疆', '广西', '西藏', '宁夏']:
        province = k[:2]
    elif k[:2] == '内蒙':
        province = k[:3]
    data_pair = v
    map = (
        Map()
        .add(
            '',
            data_pair=data_pair,
            maptype=province,
            is_map_symbol_show=False,
            itemstyle_opts={
                "normal": {"areaColor": "#323c48", "borderColor": "#404a59"},
            },
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(formatter="{b}:{c}人"),
            title_opts=opts.TitleOpts(
                title=f'{province}2020年人口数据',
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25,
                    color="rgba(255,255,255, 0.9)"
                )
            ),
            visualmap_opts=opts.VisualMapOpts(
                max_=10000000,
                range_color=["lightskyblue", "yellow", "orangered"],
                is_show=False,
                is_piecewise=False
            )
        )
    )
    bar_x_data = []
    bar_y_data = []
    v.sort(key=lambda x: x[1], reverse=True)
    for x in v:
        bar_x_data.append(x[0])
        bar_y_data.append(x[1])
    bar = (
        Bar()
        .add_xaxis(bar_x_data)
        .add_yaxis(
            '',
            bar_y_data,
            label_opts=opts.LabelOpts(
                is_show=True, position="right", formatter="{b}:{c}人"
            ),
        ).reversal_axis()
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                max_=13000000, axislabel_opts=opts.LabelOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                is_show=False,
                is_piecewise=True,
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                max_=13000000,
            )
        )
    )
    # bar_x_data.clear()
    # bar_y_data.clear()  # 清空x轴和y轴的数据
    pie = (
        Pie()
        .add(
            '',
            data_pair=v,
            radius=["15%", "35%"],
            center=["80%", "82%"],
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=1, border_color="rgba(0,0,0,0.3)"
            ),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    grid = (
        Grid(init_opts=opts.InitOpts(width="1600px", height="800px", theme=ThemeType.DARK))
        .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left="10", pos_right="45%", pos_top="50%", pos_bottom="5"
            ),
        )
        .add(pie, grid_opts=opts.GridOpts(pos_left="45%", pos_top="60%"))
        .add(map, grid_opts=opts.GridOpts())
    ).render(fr'D:\PyPRo\Demo_flask\templates/city/{province}.html')