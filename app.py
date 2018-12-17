from flask import Flask, render_template, request, jsonify
app = Flask(__name__, static_url_path = "/static", static_folder = "static")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d, Axes3D

from matplotlib import cm as cm

from io import BytesIO
import base64
import numpy as np
from sympy import symbols, sympify, latex, integrate, solve
from sympy.parsing.sympy_parser import parse_expr

@app.route('/')
def index():
    return render_template("index.html"), 404

@app.route('/expression', methods=['POST'])
def expression():
    try:
        print('Data received: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        symbols = [str(s) for s in ps.free_symbols]
        symbols.sort()
        return jsonify({ 'expression': str(ps), 'expression_latex': latex(ps), 'variables': symbols })

    except Exception as e:
        print(e)
        return str(e), 400
    
@app.route('/diff', methods=['POST'])
def diff():
    try:
        print('Data received: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = request.json['var']
        return jsonify({ 'in': latex(ps), 'out': latex(ps.diff(var)), 'var': var })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/diff2', methods=['POST'])
def diff2():
    try:
        print('Data received: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = request.json['var']
        return jsonify({ 'in': latex(ps), 'out': latex(ps.diff(var).diff(var)), 'var': var })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/integrate', methods=['POST'])
def integration():
    try:
        print('Data received: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = [s for s in ps.free_symbols if str(s) == request.json['var']][0] 
        limits = (var, request.json['from'], request.json['to']) if len(request.json['to']) > 0 else var
        return jsonify({ 'in': latex(ps), 'out': latex(integrate(ps, limits)), 'var': str(var) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/solvefor', methods=['POST'])
def solve_for():
    try:
        print('Data received: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = request.json['var']
        return jsonify({ 'in': latex(ps), 'out': latex(solve(ps, var)), 'var': var })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/plot', methods=['POST'])
def plot():

    try:

        print('Data received: {}'.format(request.json))

        ps = parse_expr(request.json['expression'], locals())

        print('Expression: {}'.format(ps))

        fig = plt.figure(figsize=(5,5))

        if len(ps.free_symbols) == 1:

            X = np.linspace(request.json['xlim'][0], request.json['xlim'][1], 64)
            Y = [ps.subs(list(ps.free_symbols)[0], x) for x in X]

            ax = fig.add_subplot(111)
            ax.plot(X,Y, c='purple', lw=2)
            ax.set_xlabel(str(list(ps.free_symbols)[0]))
            ax.set_ylabel('f({})'.format(str(list(ps.free_symbols)[0])))
            if '\\' not in latex(ps):
                plt.title('Line plot of ${}$'.format(latex(ps)))
            plt.grid(ls='dashed', alpha=.5)
        
        elif len(ps.free_symbols) == 2:

            var = [str(s) for s in ps.free_symbols]
            var.sort()
            print(var)
            xs = np.linspace(request.json['xlim'][0], request.json['xlim'][1], 32)
            ys = np.linspace(request.json['ylim'][0], request.json['ylim'][1], 32)
            X, Y = np.meshgrid(xs, ys)
            zs = np.array([ps.subs(var[0], x).subs(var[1], y).evalf() for x, y in zip(np.ravel(X), np.ravel(Y))]).astype('float')
            Z = zs.reshape(X.shape)

            ax = fig.add_subplot(111, projection='3d')
            surf = ax.plot_surface(X, Y, Z, cmap=cm.inferno)
            #fig.colorbar(surf, shrink=0.5, aspect=5)
            plt.title('Surface plot of ${}$'.format(latex(ps)))
            ax.set_xlabel(str(var[0]))
            ax.set_ylabel(str(var[1]))
            ax.set_zlabel('f({},{})'.format(str(var[0]), str(var[1])))

        else:

            return 'Too many or no variables to plot!', 400
        
        data = BytesIO()
        fig.savefig(data)
        data.seek(0)
        encoded_img = base64.b64encode(data.read())
        return jsonify({ 'expression': str(ps), 'latex': latex(ps), 'img': 'data:image/png;base64,' + str(encoded_img)[2:-1] })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/test')
def test():
    return "This is a test endpoint!"