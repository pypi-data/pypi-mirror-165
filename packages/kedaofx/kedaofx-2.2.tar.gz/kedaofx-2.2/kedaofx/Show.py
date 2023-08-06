def show_null(self, ops_int=None, ops_str=None):
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.commons.utils import JsCode
    import numpy as np

    null = self.isnull().sum().tolist()

    null_int = (self == ops_int).sum().tolist()
    null_str = (self == ops_str).sum().tolist()
    if max(null) + max(null_int) + max(null_str) == 0:
        print('无空值')
    else:

        null_all = np.sum([null, null_int, null_str], axis=0).tolist()
        null_end = []
        x_columns = []
        x_i = self.columns
        for i in range(0, len(self.columns)):
            if null_all[i] == 0:
                pass
            else:
                null_end.append(null_all[i])
                x_columns.append(x_i[i])
        max_all = len(self)
        line_null = []
        for i in range(0, len(null_end)):
            line_null.append(float("%.2f" % ((null_end[i] / max_all) * 100)))

        X = x_columns
        colors = ['#8A54B6', '#5F7FC8', '#E4002C']
        values = line_null
        # 指定柱子颜色的js代码
        color_function = """
                function (params) {
                    if (params.value < 30) 
                        return '#00B642';
                    else if (params.value > 30 && params.value < 70) 
                        return '#FF8A00';
                    else return '#E4002C';
                }
                """

        bar = (
            Bar()
                .add_xaxis(X)
                .add_yaxis(""
                           , values
                           , category_gap="40%"
                           , itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function))

                           )

                .set_series_opts(markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=30, name="30%"),
                                                                       opts.MarkLineItem(y=70, name="70%"),
                                                                       opts.MarkLineItem(y=50, name="50%")],
                                                                 label_opts=opts.LabelOpts(formatter="{c}%")),
                                 label_opts=opts.LabelOpts(formatter="{c}%")
                                 )

                .set_global_opts(title_opts=opts.TitleOpts(title="各个商品销量比较"))
                .set_global_opts(
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    name="",
                    min_=0,
                    max_=100,
                    position="left",
                    offset=0,

                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(color=colors[0])
                    ),
                    axislabel_opts=opts.LabelOpts(formatter=("{value}%")),
                ),

                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),

                # 坐标轴显示不全处理
                xaxis_opts=opts.AxisOpts(name_rotate=60, axislabel_opts={"rotate": 45},
                                         name_textstyle_opts=opts.TextStyleOpts(font_size=100))
            )
                .set_global_opts(title_opts=opts.TitleOpts(title="空值查看"))

        )

        return bar.render_notebook()