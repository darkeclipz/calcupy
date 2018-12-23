# Calcupy

Calculus powered graphical calculator with Python.

The app has been deployed to [`https://calcupy.herokuapp.com/`](https://calcupy.herokuapp.com/). It may take some time initially, because the server has to wake up if it has not been used.

# Usage

Enter an expression to get started. The calculator will evaluate the expression and determine if it is an expression, equality or inequality. If it is an expression with one variable, a line plot, and single variable calculus is available. If the expression has two variables, a surface, contour and gradient plot are available, as well as multivariable calculus functions. Otherwise there are basic algebra methods available, such as solving for one variable, expanding, factoring, finding factors, and trigonometric expansions.

Based on what type of expression and how many variables there are, the following functionality is available:

|Variables|Type|Action|
|--|--|--|
|0|Expression|Evaluate|
|1+|Expression, equality, inequality|Simplify|
|1+|Expression, equality, inequality|Expand|
|1+|Expression, equality, inequality|Expand trig|
|1+|Expression, equality, inequality|Factor|
|1+|Expression|Factors|
|1|Expression|Line plot|
|1|Expression|Derivative|
|1|Expression|Second derivative|
|1|Expression|Indefinite integral|
|1|Expression|Integrate from 0 to T|
|1|Expression|Integrate from -inf to inf|
|2|Expression|Surface plot|
|2|Expression|Contour plot|
|2|Expression|Gradient plot|
|2+|Expression|Partial derivatives|
|2+|Expression|Second partial derivatives|
|2+|Expression|Gradient|
|2|Expression|Hessian matrix|
|1+|Equality, inequality|Solve for variable|
|0+|Matrix|Transpose|
|0+|Square matrix|Inverse|
|0+|Square matrix|Determinant|
|0+|Square matrix|Eigenvectors and values|
|1|Column vector|Line plot of vectors|
|1|Matrix 2x1|Parametric plot 2D|
|1|Matrix 3x1|Parametric plot 3D|
|1|Matrix NxM where M,N >= 2|Matrix plot|
|0|Symmetric square matrix|Undirected graph|
|0|Square matrix|Directed graph|
|0|Simple graph|Graph complement|
|0|Graph|Degree matrix|
|0|Undirected graph|Minimum spanning tree (MST)|
|1|Expression|Polar plot|
|1|Matrix|Polar plot|

Not what you want? Submit what you are missing, as an issue, on Github.

# Examples

The following are examples of expressions that are understood:

 * Constants (evaluate):
   * [`exp((sqrt(-1)*pi))`](https://calcupy.herokuapp.com/?expr=exp((sqrt(-1)*pi)))
   * [`32!`](https://calcupy.herokuapp.com/?expr=32!)
 * One variable: 
   * [`1 / (1 + x^2)`](https://calcupy.herokuapp.com/?expr=1%20%2F%20(1%20%2B%20x%5E2))
 * Two variables: 
   * [`x*y`](https://calcupy.herokuapp.com/?expr=x*y) 
   * [`sin(1/2*x*y)`](https://calcupy.herokuapp.com/?expr=sin(1%2F2*x*y))
   * [`1 / (1 + x^2 + y^2)`](https://calcupy.herokuapp.com/?expr=1%20%2F%20(1%20%2B%20x%5E2%20%2B%20y%5E2))
   * [`sqrt(x^2 + y^2)`](https://calcupy.herokuapp.com/?expr=sqrt(x%5E2%20%2B%20y%5E2))
   * [`(-3*x) / (x^2 + y^2 + 1)`](https://calcupy.herokuapp.com/?expr=(-3*x)%2F(x%5E2%2By%5E2%2B1))
   * [`exp(y) * cos(x) + exp(x) * sin(y)`](https://calcupy.herokuapp.com/?expr=exp(y)%20*%20cos(x)%20%2B%20exp(x)%20*%20sin(y))
   * [`sqrt(4*x^2 + y^2) + cos(4*x) * y`](https://calcupy.herokuapp.com/?expr=sqrt(4*x%5E2%20%2B%20y%5E2)%20%2B%20cos(4*x)*y)
 * Equalities: 
   * [`z^3 + z^2 + z^1 + z = 0`](https://calcupy.herokuapp.com/?expr=z%5E3%20%2B%20z%5E2%20%2B%20z%5E1%20%2B%20z%20%3D%200)
   * [`a*x^2 + b*x + c = 0`](https://calcupy.herokuapp.com/?expr=a*x%5E2%2Bb*x%2Bc%3D0)
   * [`x^2 + p*x + q = 0`](https://calcupy.herokuapp.com/?expr=x%5E2%2Bp*x%2Bq%3D0)
 * Inequalities: 
   * [`x^2 < 5`](https://calcupy.herokuapp.com/?expr=x%5E2%20%3C%3D%205)
   * [`sqrt(x) < x`](https://calcupy.herokuapp.com/?expr=sqrt(x)%20%3C%20x)
 * Matrices:
   * [`[1,2,3]`](https://calcupy.herokuapp.com/?expr=Matrix(%5B1%2C2%2C3%5D))
   * [`[[1,2],[3,4]]`](https://calcupy.herokuapp.com/?expr=Matrix(%5B%5B1%2C2%5D%2C%5B3%2C4%5D%5D))
 * Parametric:
   * [`[sin(2*t), cos(3*t)]`](https://calcupy.herokuapp.com/?expr=Matrix(%5Bsin(2*t)%2C%20cos(3*t)%5D))
   * [`[cos(3*t), sin(3*t), t]`](https://calcupy.herokuapp.com/?expr=Matrix(%5Bcos(3*t)%2C%20sin(3*t)%2C%20t%5D))
   * [`[cos(13*t), 0, sin(7*t)]`](https://calcupy.herokuapp.com/?expr=Matrix(%5Bcos(13*t)%2C%200%2C%20sin(7*t)%5D)&xlima=-5&xlimb=5&ylima=-5&ylimb=5)
   * [`[cos(5*t), 0, t]`](https://calcupy.herokuapp.com/?expr=Matrix(%5Bcos(5*t)%2C%200%2C%20t%5D)%20&xlima=-5&xlimb=5&ylima=-5&ylimb=5)
 * Polar:
   * [`cos(phi)`](http://calcupy.herokuapp.com/?expr=cos(phi)&xlima=-5&xlimb=5&ylima=-5&ylimb=5)
   * [`cos(6*phi)+2`](http://calcupy.herokuapp.com/?expr=cos(6*phi)%2B2&xlima=-5&xlimb=5&ylima=-5&ylimb=5)
   * [`0.5*phi + sin(3*phi)`](http://calcupy.herokuapp.com/?expr=0.5*phi%20%2B%20sin(3*phi)&xlima=-5&xlimb=5&ylima=-5&ylimb=5)
 * Graphs:
   * [`8x8 weighted graph`](http://calcupy.herokuapp.com/?expr=Matrix(%5B%5B%200.0%2C%20%206.0%2C%2016.0%2C%2042.0%2C%2072.0%2C%20%200.0%2C%20%207.0%2C%2018.0%5D%2C%5B%206.0%2C%20%200.0%2C%2036.0%2C%2028.0%2C%2024.0%2C%2045.0%2C%20%209.0%2C%2042.0%5D%2C%5B16.0%2C%2036.0%2C%20%200.0%2C%20%200.0%2C%2054.0%2C%20%200.0%2C%2032.0%2C%2054.0%5D%2C%5B42.0%2C%2028.0%2C%20%200.0%2C%20%200.0%2C%2056.0%2C%2063.0%2C%2010.0%2C%2014.0%5D%2C%5B72.0%2C%2024.0%2C%2054.0%2C%2056.0%2C%20%200.0%2C%2072.0%2C%2072.0%2C%2018.0%5D%2C%5B%200.0%2C%2045.0%2C%20%200.0%2C%2063.0%2C%2072.0%2C%20%200.0%2C%2032.0%2C%2010.0%5D%2C%5B%207.0%2C%20%209.0%2C%2032.0%2C%2010.0%2C%2072.0%2C%2032.0%2C%20%200.0%2C%2063.0%5D%2C%5B18.0%2C%2042.0%2C%2054.0%2C%2014.0%2C%2018.0%2C%2010.0%2C%2063.0%2C%20%200.0%5D%5D)&xlima=-5&xlimb=5&ylima=-5&ylimb=5)

There is no UI component yet to change the plot limits. However, it can be done manually by opening the console and entering `app.plot_xlim = app.plot_ylim = [-10,10]; app.plot()`.

# SymPy syntax

**Algebra** `simplify`, `factor`, `expand`, `cancel`, `apart`, `trigsimp`, `expand_trig`, `ln`, `expand_log`, `logcombine`, `expr.rewrite(sin)`, `expr.rewrite(gamma)`, `expr.rewrite(exp)`.

**Calculus** `diff(expr, x)`, `diff(expr, x, 2)`, `expr.diff((x, n))`, `integrate(expr, x)`, `integrate(expr, (x, 0, oo))`, `integrate(expr, (x, -oo, oo), (y, -oo, oo))`, `limit(expr x, 0)`, `limit(expr, x, oo)`, `limit(1/x, x, 0, '+')`, `expr.series(x, 0, 4)`, `expr.series(x, 0, 4).removeO()`.

**Matrices:** `M.T`, `eye(n)`, `zeros(n)`, `ones(n)`, `diag(1, 2, 3)`, `M.det()`, `M.charpoly(t)`.

# Contributions

Feel free to contribute! Also, if you have an idea, please let me know (or submit it as an issue on Github)!

# Thanks

Made possible by:

 * SymPy for computer algebra capabilities.
 * Matplotlib for plotting.
 * Graphviz for drawing graphs.
 * Flask as back-end.
 * Vue.js as front-end.
 * Mathjax for equation typesetting.

Hosted on Heroku with gUnicorn.