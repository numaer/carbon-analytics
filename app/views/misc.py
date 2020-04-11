"""
Old code that may or may not be used.
"""


# Selectors, main graph -> pie graph
"""
@app.callback(
    Output("pie_graph", "figure"),
    [
        Input("well_statuses", "value"),
        Input("well_types", "value"),
        Input("year_slider", "value"),
    ],
)
"""
def make_pie_figure(well_statuses, well_types, year_slider):

    layout_pie = copy.deepcopy(layout)

    dff = filter_dataframe(df, well_statuses, well_types, year_slider)

    selected = dff["API_WellNo"].values
    index, gas, oil, water = produce_aggregate(selected, year_slider)

    aggregate = dff.groupby(["Well_Type"]).count()

    data = [
        dict(
            type="pie",
            labels=["Gas", "Oil", "Water"],
            values=[sum(gas), sum(oil), sum(water)],
            name="Production Breakdown",
            text=[
                "Total Gas Produced (mcf)",
                "Total Oil Produced (bbl)",
                "Total Water Produced (bbl)",
            ],
            hoverinfo="text+value+percent",
            textinfo="label+percent+name",
            hole=0.5,
            marker=dict(colors=["#fac1b7", "#a9bb95", "#92d8d8"]),
            domain={"x": [0, 0.45], "y": [0.2, 0.8]},
        ),
        dict(
            type="pie",
            labels=[WELL_TYPES[i] for i in aggregate.index],
            values=aggregate["API_WellNo"],
            name="Well Type Breakdown",
            hoverinfo="label+text+value+percent",
            textinfo="label+percent+name",
            hole=0.5,
            marker=dict(colors=[WELL_COLORS[i] for i in aggregate.index]),
            domain={"x": [0.55, 1], "y": [0.2, 0.8]},
        ),
    ]
    layout_pie["title"] = "Production Summary: {} to {}".format(
        year_slider[0], year_slider[1]
    )
    layout_pie["font"] = dict(color="#777777")
    layout_pie["legend"] = dict(
        font=dict(color="#CCCCCC", size="10"), orientation="h", bgcolor="rgba(0,0,0,0)"
    )

    figure = dict(data=data, layout=layout_pie)
    return figure


# Selectors, main graph -> aggregate graph
"""
@app.callback(
    Output("aggregate_graph", "figure"),
    [
        Input("well_statuses", "value"),
        Input("well_types", "value"),
        Input("year_slider", "value"),
        Input("main_graph", "hoverData"),
    ],
)
"""
def make_aggregate_figure(well_statuses, well_types, year_slider, main_graph_hover):

    layout_aggregate = copy.deepcopy(layout)

    if main_graph_hover is None:
        main_graph_hover = {
            "points": [
                {"curveNumber": 4, "pointNumber": 569, "customdata": 31101173130000}
            ]
        }

    chosen = [point["customdata"] for point in main_graph_hover["points"]]
    well_type = dataset[chosen[0]]["Well_Type"]
    dff = filter_dataframe(df, well_statuses, well_types, year_slider)

    selected = dff[dff["Well_Type"] == well_type]["API_WellNo"].values
    index, gas, oil, water = produce_aggregate(selected, year_slider)

    data = [
        dict(
            type="scatter",
            mode="lines",
            name="Gas Produced (mcf)",
            x=index,
            y=gas,
            line=dict(shape="spline", smoothing="2", color="#F9ADA0"),
        ),
        dict(
            type="scatter",
            mode="lines",
            name="Oil Produced (bbl)",
            x=index,
            y=oil,
            line=dict(shape="spline", smoothing="2", color="#849E68"),
        ),
        dict(
            type="scatter",
            mode="lines",
            name="Water Produced (bbl)",
            x=index,
            y=water,
            line=dict(shape="spline", smoothing="2", color="#59C3C3"),
        ),
    ]
    layout_aggregate["title"] = "Aggregate: " + WELL_TYPES[well_type]

    figure = dict(data=data, layout=layout_aggregate)
    return figure



"""
html.Div(
    [
        html.Div(
            [dcc.Graph(id="pie_graph")],
            className="pretty_container seven columns",
        ),
        html.Div(
            [dcc.Graph(id="aggregate_graph")],
            className="pretty_container five columns",
        ),
    ],
    className="row flex-display",
),


@app.callback(
    Output("aggregate_data", "data"),
    [
        #Input("well_statuses", "value"),
        #Input("well_types", "value"),
        #Input("year_slider", "value"),
    ],
)
def update_production_text():#(well_statuses, well_types, year_slider):

    #dff = filter_dataframe(df, well_statuses, well_types, year_slider)
    #selected = dff["API_WellNo"].values
    #index, gas, oil, water = produce_aggregate(selected, year_slider)
    #return [human_format(sum(gas)), human_format(sum(oil)), human_format(sum(water))]
    return [2000,2000,2000,2000]
"""



