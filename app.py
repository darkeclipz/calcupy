from flask import Flask, render_template, request, jsonify
app = Flask(__name__, static_url_path = "/static", static_folder = "static")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d, Axes3D
import matplotlib

from matplotlib import cm as cm

from io import BytesIO
import base64
import numpy as np
from sympy import symbols, sympify, latex, integrate, solve, solveset, Matrix, expand, factor, primitive, simplify, factor_list
from sympy.parsing.sympy_parser import parse_expr

font = {'size': 12}
matplotlib.rc('font', **font)
colormap = cm.magma

@app.route('/')
def index():
    return render_template("index.html"), 404

@app.route('/expression', methods=['POST'])
def expression():
    try:
        print('expression: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        symbols = [str(s) for s in ps.free_symbols]
        symbols.sort()
        return jsonify({ 'expression': str(ps), 'expression_latex': latex(ps), 'variables': symbols })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/simplify', methods=['POST'])
def simplifyexpr():
    try:
        print('simplify: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        result = expand(ps)
        return jsonify({ 'in': latex(ps), 'out': latex(result) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/expand', methods=['POST'])
def expandexpr():
    try:
        print('expand: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        return jsonify({ 'in': latex(ps), 'out': latex(expand(ps, trig=request.json['trig'])) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/factor', methods=['POST'])
def factorexpr():
    try:
        print('factor: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        return jsonify({ 'in': latex(ps), 'out': latex(factor(ps)) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/factors', methods=['POST'])
def factorlist():
    try:
        print('factor list: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        return jsonify({ 'in': latex(ps), 'out': latex(factor_list(ps)) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/primitive', methods=['POST'])
def primitives():
    try:
        print('primitive: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        return jsonify({ 'in': latex(ps), 'out': latex(primitive(ps)) })

    except Exception as e:
        print(e)
        return str(e), 400
    
@app.route('/diff', methods=['POST'])
def diff():
    try:
        print('diff: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = request.json['var']
        return jsonify({ 'in': latex(ps), 'out': latex(ps.diff(var)), 'var': var })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/diff2', methods=['POST'])
def diff2():
    try:
        print('diff2: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = request.json['var']
        return jsonify({ 'in': latex(ps), 'out': latex(ps.diff(var).diff(var)), 'var': var })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/grad', methods=['POST'])
def grad():
    try:
        print('grad: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        symbols = [str(s) for s in ps.free_symbols]
        symbols.sort()
        grad = Matrix([ps.diff(v) for v in symbols])
        return jsonify({ 'in': latex(ps), 'out': latex(grad) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/hessian', methods=['POST'])
def hessian():
    try:
        print('hessian: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        symbols = [str(s) for s in ps.free_symbols]
        symbols.sort()
        x = symbols[0]
        y = symbols[1]
        hessian = Matrix([[ps.diff(x).diff(x), ps.diff(x).diff(y)],[ps.diff(y).diff(x), ps.diff(y).diff(y)]])
        return jsonify({ 'in': latex(ps), 'out': latex(hessian), 'hessian': latex(hessian.det()) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/integrate', methods=['POST'])
def integration():
    try:
        print('integrate: {}'.format(request.json))
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
        print('solve for: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = request.json['var']
        return jsonify({ 'in': latex(ps), 'out': latex(solve(ps, var)), 'var': var })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/plot', methods=['POST'])
def plot():

    try:

        print('plot: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        fig = plt.figure(figsize=(6.15,5))
        fig.clf()
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
            xs = np.linspace(request.json['xlim'][0], request.json['xlim'][1], 32)
            ys = np.linspace(request.json['ylim'][0], request.json['ylim'][1], 32)
            X, Y = np.meshgrid(xs, ys)
            zs = np.array([ps.subs(var[0], x).subs(var[1], y).evalf() for x, y in zip(np.ravel(X), np.ravel(Y))]).astype('float')
            Z = zs.reshape(X.shape)

            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z, cmap=colormap)

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

@app.route('/cplot', methods=['POST'])
def cplot():
    try:

        print('cplot: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = [str(s) for s in ps.free_symbols]
        var.sort()
        if len(ps.free_symbols) != 2: 
            raise ValueError('Contour plots requires a function of two variables.')

        fig = plt.figure(figsize=(6.15,5))
        fig.clf()

        xs = np.linspace(request.json['xlim'][0], request.json['xlim'][1], 32)
        ys = np.linspace(request.json['ylim'][0], request.json['ylim'][1], 32)
        X, Y = np.meshgrid(xs, ys)
        zs = np.array([ps.subs(var[0], x).subs(var[1], y).evalf() for x, y in zip(np.ravel(X), np.ravel(Y))]).astype('float')
        Z = zs.reshape(X.shape)
                    
        ax = fig.add_subplot(111)
        CS = ax.contourf(X, Y, Z, 24, cmap=colormap)
        fig.colorbar(CS, shrink=0.5, aspect=5)
        plt.title('Contour plot of ${}$'.format(latex(ps)))
        ax.set_xlabel(str(var[0]))
        ax.set_ylabel(str(var[1]))

        data = BytesIO()
        fig.savefig(data)
        data.seek(0)
        encoded_img = base64.b64encode(data.read())
        return jsonify({ 'expression': str(ps), 'latex': latex(ps), 'img': 'data:image/png;base64,' + str(encoded_img)[2:-1] })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/gplot', methods=["POST"])
def gplot():
    try:

        print('gplot: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = [str(s) for s in ps.free_symbols]
        var.sort()
        if len(ps.free_symbols) != 2: 
            raise ValueError('Contour plots requires a function of two variables.')

        fig = plt.figure(figsize=(6.15,5))
        fig.clf()
        ax = fig.add_subplot(111)

        detail = 24
        arrows = 1.5

        # contour plot
        grad = Matrix([ps.diff(var[0]), ps.diff(var[1])])
        xs = np.linspace(request.json['xlim'][0], request.json['xlim'][1], detail)
        ys = np.linspace(request.json['ylim'][0], request.json['ylim'][1], detail)
        X, Y = np.meshgrid(xs, ys)
        zs = np.array([ps.subs('x', x).subs('y', y).evalf() for x, y in zip(np.ravel(X), np.ravel(Y))]).astype('float')
        Z = zs.reshape(X.shape)
        plt.contourf(X, Y, Z, detail*2, cmap=colormap)

        # vector field
        xs = np.linspace(request.json['xlim'][0], request.json['xlim'][1], np.floor(detail/arrows))
        ys = np.linspace(request.json['ylim'][0], request.json['ylim'][1], np.floor(detail/arrows))
        X, Y = np.meshgrid(xs, ys)
        dzs = np.array([grad.subs('x', x).subs('y', y).evalf() for x, y in zip(np.ravel(X), np.ravel(Y))]).astype('float')
        dZx = [z[0] for z in dzs]
        dZy = [z[1] for z in dzs]
        dZz = [np.sqrt(np.dot(z,z)) for z in dzs]
        quiv = plt.quiver(X,Y,dZx,dZy,dZz,cmap=colormap, pivot="tip")
        plt.colorbar(quiv, shrink=0.8)

        plt.title('Gradient plot of ${}$'.format(latex(ps)))
        ax.set_xlabel(str(var[0]))
        ax.set_ylabel(str(var[1]))

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