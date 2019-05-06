from flask import render_template, request, flash
from website import app
from api import Api, ClassicalSubgroups, ApiError
from bokeh.embed import json_item
import bokeh.plotting as bk
import random
import string
import json


@app.route('/')
def index():
    return render_template('index.html')


def gen_api(subgroup, n):
    user_api = Api()
    user_api.set_subgroup(subgroup=subgroup, n=n)
    user_api.calc_graph()
    user_api.calc_domain()
    return user_api


@app.route('/digest', methods=['POST'])
def digest():
    data = json.loads(request.data)

    user_api = gen_api(ClassicalSubgroups.from_str(data["subgroup"]), data["n"])

    graph_fig = bk.figure(match_aspect=True)
    graph_fig.sizing_mode = 'stretch_both'
    domain_fig = bk.figure(match_aspect=True)
    domain_fig.width_policy = 'min'
    domain_fig.sizing_mode = 'stretch_both'

    user_api.plot_graph_on_bokeh(graph_fig)
    user_api.plot_domain_on_bokeh(domain_fig)
    generators = user_api.get_generators_str()

    graph_plot = json_item(graph_fig)
    domain_plot = json_item(domain_fig)

    response = {"graph": graph_plot, "domain": domain_plot, "generators": generators}

    return json.dumps(response)


@app.route('/decompose', methods=['POST'])
def decompose():
    data = json.loads(request.data)
    user_api = gen_api(ClassicalSubgroups.from_str(data["subgroup"]), int(data["n"]))
    decomposition = ''
    errors = ''
    try:
        user_api.decompose_matrix(data["matrix"])
    except ApiError as e:
        errors = str(e)
    else:
        decomposition = user_api.get_decomposition()

    return json.dumps({'errors': errors, 'decomposition': decomposition})
