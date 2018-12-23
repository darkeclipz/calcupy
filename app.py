from flask import Flask, render_template, request, jsonify
app = Flask(__name__, static_url_path = "/static", static_folder = "static")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d, Axes3D
import matplotlib

from matplotlib import cm

from io import BytesIO
import base64
import numpy as np
from sympy import symbols, sympify, latex, integrate, solve, solveset, Matrix, expand, factor, primitive, simplify, factor_list
from sympy.parsing.sympy_parser import parse_expr
from scipy.stats import scoreatpercentile
import graph as graphplot

font = {'size': 12}
matplotlib.rc('font', **font)
colormap = cm.magma

from matplotlib.patches import FancyArrowPatch
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs
    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

@app.route('/')
def index():
    return render_template("index.html"), 404

def is_sqr_matrix(M):
    if not 'Matrix' in str(type(M)): return False
    if M.shape[0] != M.shape[1]: return False
    return True

@app.route('/expression', methods=['POST'])
def expression():
    try:
        print('expression: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        symbols = [str(s) for s in ps.free_symbols]
        symbols_latex = [latex(s) for s in ps.free_symbols]
        symbols.sort()
        symbols_latex.sort()
        return jsonify({
            'expression': str(ps),
            'expression_latex': latex(ps),
            'variables': symbols,
            'is_constant':   'Integer' in str(type(ps)) 
                          or 'Float' in str(type(ps))
                          or 'Rational' in str(type(ps)),
            'is_equality':   'Equality' in str(type(ps)),
            'is_inequality': 'Inequality' in str(type(ps)) 
                          or 'Greater' in str(type(ps)) 
                          or 'Less' in str(type(ps)),
            'is_matrix':     'Matrix' in str(type(ps)),
            'dimension':     list(ps.shape) if 'Matrix' in str(type(ps)) else [0, 0],
            'is_ugly':       True if 'Matrix' in str(type(ps)) and (ps.shape[0] > 10 or ps.shape[1] > 10) else False,
            'is_weighted':   graphplot.is_weighted(ps) if is_sqr_matrix(ps) else False,
            'is_directed':   graphplot.is_directed(ps) if is_sqr_matrix(ps) else False
        })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/simplify', methods=['POST'])
def simplifyexpr():
    try:
        print('simplify: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        result = expand(ps)
        return jsonify({ 'in': latex(ps), 'out': latex(result), 'out_expression': str(result) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/expand', methods=['POST'])
def expandexpr():
    try:
        print('expand: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        result = expand(ps, trig=request.json['trig'])
        return jsonify({ 'in': latex(ps), 'out': latex(result), 'out_expression': str(result) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/factor', methods=['POST'])
def factorexpr():
    try:
        print('factor: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        result = factor(ps)
        return jsonify({ 'in': latex(ps), 'out': latex(result), 'out_expression': str(result) })

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
        result = ps.diff(var)
        return jsonify({ 'in': latex(ps), 'out': latex(result), 'var': var, 'out_expression': str(result) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/diff2', methods=['POST'])
def diff2():
    try:
        print('diff2: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = request.json['var']
        result = ps.diff(var).diff(var)
        return jsonify({ 'in': latex(ps), 'out': latex(result), 'var': var, 'out_expression': str(result) })

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
        return jsonify({ 'in': latex(ps), 'out': latex(grad), 'out_expression': str(grad) })

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
        return jsonify({ 'in': latex(ps), 'out': latex(hessian), 'hessian': latex(hessian.det()), 'out_expression': str(hessian) })

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
        result = integrate(ps, limits)
        return jsonify({ 'in': latex(ps), 'out': latex(result), 'var': str(var), 'out_expression': str(result) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/solvefor', methods=['POST'])
def solve_for():
    try:
        print('solve for: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = request.json['var']
        result = solve(ps, var)
        return jsonify({ 'in': latex(ps), 'out': latex(result), 'var': var, 'out_expression': str(result) })

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

            X = np.linspace(request.json['xlim'][0], request.json['xlim'][1], 512)
            Y = np.array([ps.subs(list(ps.free_symbols)[0], x) for x in X]).astype('float')

            ax = fig.add_subplot(111)
            ax.plot(X,list(Y), c='purple', lw=3)
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
            zs = np.array([expand(ps).subs(var[0], x).subs(var[1], y).evalf() for x, y in zip(np.ravel(X), np.ravel(Y))]).astype('float')
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

        detail = 24
        fig = plt.figure(figsize=(6.15,5))
        fig.clf()

        xs = np.linspace(request.json['xlim'][0], request.json['xlim'][1], 32)
        ys = np.linspace(request.json['ylim'][0], request.json['ylim'][1], 32)
        X, Y = np.meshgrid(xs, ys)
        zs = np.array([expand(ps).subs(var[0], x).subs(var[1], y).evalf() for x, y in zip(np.ravel(X), np.ravel(Y))]).astype('float')
        Z = zs.reshape(X.shape)
                    
        ax = fig.add_subplot(111)
        CS = ax.contourf(X, Y, Z, detail*2, cmap=colormap)
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
        zs = np.array([expand(ps).subs(var[0], x).subs(var[1], y).evalf() for x, y in zip(np.ravel(X), np.ravel(Y))]).astype('float')
        Z = zs.reshape(X.shape)
        plt.contourf(X, Y, Z, detail*2, cmap=colormap)

        # vector field
        xs = np.linspace(request.json['xlim'][0], request.json['xlim'][1], np.floor(detail/arrows))
        ys = np.linspace(request.json['ylim'][0], request.json['ylim'][1], np.floor(detail/arrows))
        X, Y = np.meshgrid(xs, ys)
        dzs = np.array([grad.subs(var[0], x).subs(var[1], y).evalf() for x, y in zip(np.ravel(X), np.ravel(Y))]).astype('float')

        dZx = np.array([z[0] for z in dzs])
        dZy = np.array([z[1] for z in dzs])

        dZz = np.array([np.sqrt(np.dot(z,z)) for z in dzs])

        #unitX = dZx / dZz
        #unitY = dZy / dZz

        #dZx = np.min(dZx, unitX)
        #dZy = np.min(dZy, unitY)

        quiv = plt.quiver(X,Y,dZx,dZy,dZz,cmap=colormap, pivot="middle")
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

@app.route('/pplot', methods=["POST"])
def pplot():
    try:

        print('pplot: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = [str(s) for s in ps.free_symbols]
        var.sort()
        if len(ps.free_symbols) != 1: 
            raise ValueError('Parametric plot requires a function of one variable.')
        if not 'Matrix' in str(type(ps)):
            raise ValueError('Parametric plot requires a matrix.')
        
        a = 24
        fig = plt.figure(figsize=(5,5))
        fig.clf()

        if ps.shape == (2, 1):
            ax = fig.add_subplot(111)
            ts = np.linspace(request.json['xlim'][0], request.json['xlim'][1], a**2)
            Y = np.array([ps.subs(var[0], t).evalf() for t in ts]).astype('float')
            xs = [x[0] for x in Y]
            ys = [x[1] for x in Y]
            plt.plot(xs, ys, c="purple", lw=3)
            plt.grid(ls='dashed',alpha=0.5)
        elif ps.shape == (3, 1):
            ts = np.linspace(request.json['xlim'][0], request.json['xlim'][1], a**2)
            Y = np.array([expand(ps).subs(var[0], t).evalf() for t in ts]).astype('float')
            xs = [x[0] for x in Y]
            ys = [x[1] for x in Y]
            zs = [x[2] for x in Y]
            ax = fig.add_subplot(111, projection='3d')
            plt.plot(xs, ys, zs, c="purple",lw=3)
            ax.set_xlabel('${}$'.format(latex(ps[0])))
            ax.set_ylabel('${}$'.format(latex(ps[1])))
            ax.set_zlabel('${}$'.format(latex(ps[2])))
        else:
            raise ValueError('Parametric plot requires a 3x1 or 2x1 matrix.')

        plt.title('Parametric plot of $\\left< {} \\right>$'.format( ', '.join([latex(p) for p in ps] )))

        data = BytesIO()
        fig.savefig(data)
        data.seek(0)
        encoded_img = base64.b64encode(data.read())
        return jsonify({ 'expression': str(ps), 'latex': latex(ps), 'img': 'data:image/png;base64,' + str(encoded_img)[2:-1] })  
 
    except Exception as e:
        print(e)
        return str(e), 400  

@app.route('/tplot', methods=["POST"])
def tplot():
    try:

        print('tplot: {}'.format(request.json))
        raise ValueError('not implemented.')
 
    except Exception as e:
        print(e)
        return str(e), 400  

@app.route('/vplot', methods=["POST"])
def vplot():
    try:

        print('vplot: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = [str(s) for s in ps.free_symbols]
        var.sort()
        if len(ps.free_symbols) > 0: 
            raise ValueError('Vector plot requires scalars.')
        if not 'Matrix' in str(type(ps)):
            raise ValueError('Vector plot requires a matrix.')
        if not (ps.shape[1] == 2 or ps.shape[1] == 3 or ps.shape[0] == 2 or ps.shape[0] == 3):
            raise ValueError('Vector plot requires a MxN matrix where M > 0 and N is [2, 3].')

        fig = plt.figure(figsize=(5,5))
        fig.clf()

        U = np.array(ps).astype('float')

        if U.shape == (1, 2): U = U.T
        elif U.shape == (1, 3): U = U.T

        if U.shape == (2, 1): U = np.array([U])
        elif U.shape == (3, 1): U = np.array([U])
        
        if U.shape[1] == 3:

            ax = fig.add_subplot(111, projection='3d')
            plt.xlim([-1,1])
            plt.ylim([-1,1])

            plt.axis('equal')
            X = np.array([np.cos(x) for x in np.linspace(0, 2*np.pi, 64)])
            Y = np.array([np.sin(y) for y in np.linspace(0, 2*np.pi, 64)])
            zeros = np.zeros(X.shape)

            plt.plot(X,zeros,zeros,c='darkgray', lw=2, alpha=0.33, ls='dashed')
            plt.plot(zeros,X,zeros,c='darkgray', lw=2, alpha=0.33, ls='dashed')

            plt.plot(zeros,zeros,X,c='darkgray', lw=2, alpha=0.33, ls='dashed')

            for i in range(U.shape[0]):
                x = U[i][0]; y = U[i][1]; z = U[i][2]
                magn = np.sqrt(x**2+y**2+z**2)
                ax.add_artist(Arrow3D([0, x/magn], [0, y/magn], [0,z/magn], mutation_scale=15, lw=3, arrowstyle="-|>", color="purple"))
                ax.add_artist(Arrow3D([0, x/magn], [0, y/magn], [0,0], mutation_scale=8, lw=2, arrowstyle="-|>", color="darkgray", alpha=0.5))

            plt.plot(X,Y,zeros,c='darkgray', lw=3, alpha=0.33)
            plt.plot(zeros,X,Y,c='darkgray', lw=3, alpha=0.33)
            plt.axis('off')
            fig.tight_layout()

        elif U.shape[1] == 2:
            plt.xlim([-1,1])
            plt.ylim([-1,1])

            plt.axis('equal')
            X = [np.cos(x) for x in np.linspace(0, 2*np.pi, 64)]
            Y = [np.sin(y) for y in np.linspace(0, 2*np.pi, 64)]

            plt.plot(X,Y, c='darkgray', lw=3)

            for i in range(U.shape[0]):
                x = U[i][0]; y = U[i][1]
                magn = np.sqrt(x**2 + y**2)
                plt.annotate("", xy=(x/magn, y/magn), xytext=(0, 0),arrowprops=dict(arrowstyle="->", color="purple", lw=4))

            plt.axhline(0, ls='dashed', alpha=0.33, c='gray', lw=3)
            plt.axvline(0, ls='dashed', alpha=0.33, c='gray', lw=3)
            plt.axis('off')

        else:
            raise ValueError('vplot requires the columns to be 3 or 2 dimensional.')

        data = BytesIO()
        fig.savefig(data, bbox_inches='tight')
        data.seek(0)
        encoded_img = base64.b64encode(data.read())
        return jsonify({ 'expression': str(ps), 'latex': latex(ps), 'img': 'data:image/png;base64,' + str(encoded_img)[2:-1] })  
 
    except Exception as e:
        print(e)
        return str(e), 400  

@app.route('/mplot', methods=["POST"])
def mplot():
    try:

        print('mplot: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = [str(s) for s in ps.free_symbols]
        var.sort()
        if len(ps.free_symbols) > 0: 
            raise ValueError('Matrix plot requires scalars.')
        if not 'Matrix' in str(type(ps)):
            raise ValueError('Matrix plot requires a matrix.')

        fig = plt.figure(figsize=(5,5))
        fig.clf()

        M = np.array(ps).astype('float')
        im = plt.imshow(M, cmap=colormap)
        plt.colorbar(im, shrink=0.6, aspect=8)

        data = BytesIO()
        fig.savefig(data, bbox_inches='tight')
        data.seek(0)
        encoded_img = base64.b64encode(data.read())
        return jsonify({ 'expression': str(ps), 'latex': latex(ps), 'img': 'data:image/png;base64,' + str(encoded_img)[2:-1] })  
 
    except Exception as e:
        print(e)
        return str(e), 400  

@app.route('/graph', methods=["POST"])
def graph():
    try:

        print('graph: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        var = [str(s) for s in ps.free_symbols]
        var.sort()
        if len(ps.free_symbols) > 0: 
            raise ValueError('Graph plot requires scalars.')
        if not 'Matrix' in str(type(ps)):
            raise ValueError('Graph plot requires a matrix.')
        if ps.shape[0] != ps.shape[1]:
            raise ValueError('Graph plot requires square matrix.')
 
        M = np.array(ps).astype('float')
        G = graphplot.plot(M)

        encoded_img = graphplot.to_base64_png(G.pipe())
        return jsonify({ 'expression': str(ps), 'latex': latex(ps), 'img': encoded_img })  
 
    except Exception as e:
        print(e)
        return str(e), 400 

@app.route('/transpose', methods=['POST'])
def la_transpose():
    try:
        print('transpose: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        if not 'Matrix' in str(type(ps)):
            raise ValueError('Requires a matrix.')
        ps = parse_expr(request.json['expression'], locals())
        return jsonify({ 'in': latex(ps), 'out': latex(ps.T), 'out_expression': str(ps.T) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/inverse', methods=['POST'])
def la_inverse():
    try:
        print('inverse: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        if not 'Matrix' in str(type(ps)):
            raise ValueError('Requires a matrix.')
        if ps.shape[0] != ps.shape[1]:
            raise ValueError('Requires a square matrix.')
        ps = parse_expr(request.json['expression'], locals())
        return jsonify({ 'in': latex(ps), 'out': latex(ps.inv()), 'out_expression': str(ps.inv()) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/det', methods=['POST'])
def la_det():
    try:
        print('det: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        if not 'Matrix' in str(type(ps)):
            raise ValueError('Requires a matrix.')
        if ps.shape[0] != ps.shape[1]:
            raise ValueError('Requires a square matrix.')
        ps = parse_expr(request.json['expression'], locals())
        det = ps.det()
        result = latex(det)
        if len(det.free_symbols) == 1:

            var = list(det.free_symbols)[0]
            sln = solve(det, var)
            result += ' \\implies {} = {}'.format(latex(var), latex(sln[0]))

        return jsonify({ 'in': latex(ps), 'out': result, 'out_expression': str(det) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/eigen', methods=['POST'])
def la_eigen():
    try:
        print('det: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        if not 'Matrix' in str(type(ps)):
            raise ValueError('Requires a matrix.')
        if ps.shape[0] != ps.shape[1]:
            raise ValueError('Requires a square matrix.')
        ps = parse_expr(request.json['expression'], locals())

        return jsonify({ 'in': latex(ps), 'vectors': latex([v[2][0][0] for v in ps.eigenvects()]), 'values': latex(ps.eigenvals()) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/vlength', methods=['POST'])
def la_vlength():
    try:
        print('vlength: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())
        if not 'Matrix' in str(type(ps)):
            raise ValueError('Requires a matrix.')
        if not (ps.shape[0] > 1 and ps.shape[1] == 1):
            raise ValueError('Requires a MxN matrix where M > 1 and N = 1.')

        product = sum([ps[i]**2 for i in range(ps.shape[0])])
        result = simplify( product**0.5 )

        return jsonify({ 'in': latex(ps), 'out': latex(result), 'out_expression': str(result) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/graph_complement', methods=['POST'])
def graph_complement():
    try:
        print('graph complement: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())

        if len(ps.free_symbols) > 0: 
            raise ValueError('Graph plot requires scalars.')
        if not 'Matrix' in str(type(ps)):
            raise ValueError('Graph plot requires a matrix.')
        if ps.shape[0] != ps.shape[1]:
            raise ValueError('Graph plot requires square matrix.')
 
        G = np.array(ps).astype('float')
        GC = Matrix(graphplot.complement(G))

        return jsonify({ 'in': latex(ps), 'out': latex( GC ), 'out_expression': str(GC) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/graph_degree', methods=['POST'])
def graph_degree():
    try:
        print('graph degree: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())

        if len(ps.free_symbols) > 0: 
            raise ValueError('Graph plot requires scalars.')
        if not 'Matrix' in str(type(ps)):
            raise ValueError('Graph plot requires a matrix.')
        if ps.shape[0] != ps.shape[1]:
            raise ValueError('Graph plot requires square matrix.')
 
        G = np.array(ps).astype('float')
        GC = Matrix(np.array(graphplot.degree_matrix(G)).astype('int'))

        return jsonify({ 'in': latex(ps), 'out': latex( GC ), 'out_expression': str(GC) })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/graph_mst', methods=['POST'])
def graph_mst():
    try:
        print('graph mst: {}'.format(request.json))
        ps = parse_expr(request.json['expression'], locals())

        if len(ps.free_symbols) > 0: 
            raise ValueError('Graph plot requires scalars.')
        if not 'Matrix' in str(type(ps)):
            raise ValueError('Graph plot requires a matrix.')
        if ps.shape[0] != ps.shape[1]:
            raise ValueError('Graph plot requires square matrix.')
 
        G = ps #np.array(ps).astype('float')

        mst, weight = graphplot.mst(G)
        mst = Matrix(mst)
        print(mst)

        img = graphplot.plot_mst(np.array(G).astype('float'), mst)
        encoded_img = graphplot.to_base64_png(img.pipe())

        return jsonify({ 'in': latex(ps), 'out': latex( mst ), 'out_expression': str(mst), 'weight': str(float(weight)), 'image': encoded_img })

    except Exception as e:
        print(e)
        return str(e), 400

@app.route('/test')
def test():
    return "This is a test endpoint!"