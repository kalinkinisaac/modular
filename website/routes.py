from . import app
from flask import render_template, request, session, g
from api import Api, ClassicalSubgroups
import random
import string

import mpld3
from matplotlib import pyplot as plt, figure
import json

# api = Api()
# api.set_subgroup(ClassicalSubgroups.GammaBotOne, 2)
# api.calc_graph()
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# api.plot_graph_on_axes(ax)


def users_data():
    if 'users_data' not in g:
        g.users_data = dict()
    return g.users_data


@app.route('/')
def index():
    if 'username' not in session:
        session['username'] = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        print(session['username'])
    return render_template('index.html')


@app.route('/digest', methods=['POST'])
def digest():
    if 'username' not in session:
        return 'bad request!', 400
    print(session)
    data = json.loads(request.data)

    if session['username'] not in users_data():
        users_data()[session['username']] = Api()

    user_api = users_data()[session['username']]
    user_api.set_subgroup(ClassicalSubgroups.GammaBotOne, 2)
    user_api.calc_graph()
    user_api.calc_domain()
    graph_fig = plt.figure()
    graph_ax = graph_fig.add_subplot(1, 1, 1)
    domain_fig = plt.figure()
    domain_ax = domain_fig.add_subplot(1, 1, 1)

    user_api.plot_graph_on_axes(graph_ax)
    user_api.plot_domain_on_axes(domain_ax)
    plt.show()

    graph_plot = mpld3.fig_to_html(graph_fig)
    print(graph_plot)
    domain_plot = mpld3.fig_to_html(domain_fig, template_type='simple')

    response = {"graph": graph_plot, "domain": domain_plot}
    print(response)
    return json.dumps(response)


@app.route('/decompose', methods=['POST'])
def decompose():
    if 'username' not in session:
        return 'bad request!', 400

    print(request.data)
    return "[1 0]\n[0 1]"
