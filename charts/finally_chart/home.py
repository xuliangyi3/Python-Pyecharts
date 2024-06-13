import pandas
from pyecharts import options as opts
from pyecharts.charts import Map, Timeline, Bar, Pie, Grid, Line
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

time_list = ['2022年', '2022年', '2021年', '2019年', '2018年', '2017年', '2016年', '2015年', '2014年', '2013年',
             '2012年', '2011年', '2010年', '2009年', '2008年', '2007年', '2006年', '2005年', '2004年']
time_list = list(reversed(time_list))
line_data = {
    '人口出生率(‰)': [6.77, 7.52, 10.41, 10.86, 12.64, 13.57, 11.99, 13.83, 13.03, 14.57, 13.27, 11.9, 11.95, 12.14,
                      12.1, 12.09, 12.4, 12.29],
    '人口死亡率(‰)': [7.37, 7.18, 7.09, 7.08, 7.06, 7.04, 7.07, 7.12, 7.13, 7.13, 7.14, 7.11, 7.08, 7.06, 6.93, 6.81,
                      6.51, 6.42],
    '人口自然增长率(‰)': [-0.6, 0.34, 3.32, 3.78, 5.58, 6.53, 4.93, 6.71, 5.9, 7.43, 6.13, 4.79, 4.87, 5.08, 5.17, 5.28,
                          5.89, 5.87
                          ]
}


def chart(year: str):
    """Map地图"""
    pop = pandas.read_excel('./data/总人口.xls')
    map_data = [(row['地区'], row[year]) for _, row in pop.iterrows()]
    map = (
        Map()
        .add(
            '',
            map_data,
            maptype='china',
            is_map_symbol_show=False,
            itemstyle_opts={
                "normal": {"areaColor": "#323c48", "borderColor": "#404a59"},
                "emphasis": {
                    "label": {"show": Timeline},
                    "areaColor": "rgba(255,255,255, 0.5)",
                },
            },
            label_opts=opts.LabelOpts(
                is_show=False
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f'中国{year}总人口数据统计',
                subtitle='单位：万人',
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25, color="rgba(255,255,255, 0.9)"
                ),
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter='{b}:{c}万人'
            ),
            visualmap_opts=opts.VisualMapOpts(
                max_=13000,
                is_show=False,
                is_piecewise=False,
                range_color=["lightskyblue", "yellow", "orangered"],
            )
        )
    )
    """簇状图"""
    pop_sorted = pop.sort_values(by=year, ascending=False)
    bar_x_data = [str(i['地区']) for _, i in pop_sorted.iterrows()]
    bar_y_data = pop_sorted[str(year)].tolist()
    bar = (
        Bar()
        .add_xaxis(bar_x_data)
        .add_yaxis(
            '',
            bar_y_data,
            label_opts=opts.LabelOpts(
                is_show=True, position="right", formatter="{b}:{c}万"
            ),
        ).reversal_axis()
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                max_=13000, axislabel_opts=opts.LabelOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                is_show=False,
                is_piecewise=True,
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                max_=13000,
            )
        )
    )
    '''饼图'''
    pie_data = [(row['地区'], row[year]) for _, row in pop_sorted.iterrows()]
    pie = (
        Pie()
        .add(
            '',
            pie_data,
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
    """折线图"""
    line = (
        Line(init_opts=opts.InitOpts(width="80%", height="80%"))
        .add_xaxis(time_list)
        .add_yaxis(
            '人口出生率(‰)',
            line_data['人口出生率(‰)'],
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
            itemstyle_opts=opts.ItemStyleOpts(color='red')
        )
        .add_yaxis(
            '人口死亡率(‰)',
            line_data['人口死亡率(‰)'],
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
            itemstyle_opts=opts.ItemStyleOpts(color='green'),
        )
        .add_yaxis(
            '人口自然增长率(‰)',
            line_data['人口自然增长率(‰)'],
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
            itemstyle_opts=opts.ItemStyleOpts(color='blue')
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(pos_left="65%", pos_right="80", pos_top="5%"),
            # yaxis_opts=opts.AxisOpts(min_=1,max_interval=1)
        )
    )
    grid = (
        Grid()
        .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left="10", pos_right="45%", pos_top="50%", pos_bottom="5"
            ),
        )

        .add(
            line,
            grid_opts=opts.GridOpts(
                pos_left="65%", pos_right="80", pos_top="10%", pos_bottom="50%"
            ),

        )
        .add(pie, grid_opts=opts.GridOpts(pos_left="45%", pos_top="60%"))
        .add(map, grid_opts=opts.GridOpts())

    )

    return grid


if __name__ == '__main__':
    timeline = Timeline(
        init_opts=opts.InitOpts(width="1600px", height="900px", theme=ThemeType.DARK)
    )
    for y in time_list:
        g = chart(y)
        timeline.add(g, time_point=y)
    timeline.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=5000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="60",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
    )

    timeline.render("home.html")
