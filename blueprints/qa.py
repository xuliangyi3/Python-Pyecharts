import pandas
from flask import blueprints, render_template
from markupsafe import Markup
from pyecharts.charts import Map
from pyecharts import options as opts

bp = blueprints.Blueprint('qa', __name__, url_prefix='/qa')


def map_china():
    """读取人口数据"""
    poplations = pandas.read_excel('./static/puplation.xls')
    pop_data = [(row['地区'], row['2022年']) for province, row in poplations.iterrows()]
    map = (
        Map()
        .add('', data_pair=pop_data, maptype='china', is_map_symbol_show=False, is_roam=False)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='中国2022年人口数量',
                pos_left='48%',
                subtitle='年末常驻人口 单位：万',
                text_align='center',
                title_textstyle_opts=opts.TextStyleOpts(
                    color='white'
                )
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_show=False,
                is_piecewise=True,
                max_=13000,
                range_color=['#031628', '#000102', '#000000', '#0b3d51', '#08304b', '#857f7f', '#022338', '#062032',
                             '#465b6c', '#022338'],
            )
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter='{b}:{c}万人')
        )
    )
    return map

@bp.route('/')
def home():
    return render_template('home.html')

