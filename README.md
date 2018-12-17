# MathPy

Calculus powered graphical calculator.

The app has been deployed to [`https://pymath-api-heroku.herokuapp.com/`](https://pymath-api-heroku.herokuapp.com/). 

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

Not what you want? Submit what you are missing, as an issue, on Github.

# Examples

The following are examples of expressions that are understood:

 * Constants (evaluate):
   * [`exp((sqrt(-1)*pi))`](https://pymath-api-heroku.herokuapp.com/?expr=exp((sqrt(-1)*pi)))
   * [`32!`](https://pymath-api-heroku.herokuapp.com/?expr=32!)
 * One variable: 
   * [`1 / (1 + x^2)`](https://pymath-api-heroku.herokuapp.com/?expr=1%20%2F%20(1%20%2B%20x%5E2))
 * Two variables: 
   * [`1 / (1 + x^2 + y^2)`](https://pymath-api-heroku.herokuapp.com/?expr=1%20%2F%20(1%20%2B%20x%5E2%20%2B%20y%5E2))
   * [`x*y`](https://pymath-api-heroku.herokuapp.com/?expr=x*y) 
   * [`sqrt(x^2 + y^2)`](https://pymath-api-heroku.herokuapp.com/?expr=sqrt(x%5E2%20%2B%20y%5E2))
   * [`exp(y) * cos(x) + exp(x) * sin(y)`](https://pymath-api-heroku.herokuapp.com/?expr=exp(y)%20*%20cos(x)%20%2B%20exp(x)%20*%20sin(y))
   * [`sqrt(4*x^2 + y^2) + cos(4*x) * y`](https://pymath-api-heroku.herokuapp.com/?expr=sqrt(4*x%5E2%20%2B%20y%5E2)%20%2B%20cos(4*x)*y)
 * Equalities: 
   * [`z^3 + z^2 + z^1 + z = 0`](https://pymath-api-heroku.herokuapp.com/?expr=z%5E3%20%2B%20z%5E2%20%2B%20z%5E1%20%2B%20z%20%3D%200)
   * [`a*x^2 + b*x + c = 0`](https://pymath-api-heroku.herokuapp.com/?expr=a*x%5E2%2Bb*x%2Bc%3D0)
   * [`x^2 + p*x + q = 0`](https://pymath-api-heroku.herokuapp.com/?expr=x%5E2%2Bp*x%2Bq%3D0)
 * Inequalities: 
   * [`x^2 < 5`](https://pymath-api-heroku.herokuapp.com/?expr=x%5E2%20%3C%3D%205)
   * [`sqrt(x) < x`](https://pymath-api-heroku.herokuapp.com/?expr=sqrt(x)%20%3C%20x)

It is also possible to construct matrices with [`Matrix([[1,2],[3,4]]) * t`](https://pymath-api-heroku.herokuapp.com/?expr=Matrix%28%5B%5B1%2C2%5D%2C%5B3%2C4%5D%5D%29%20*%20t). Accidently, you can also create multiple line plots with the following matrix: [`Matrix([x,x^2,x^3,x^4])`](https://pymath-api-heroku.herokuapp.com/?expr=Matrix%28%5Bx%2Cx%5E2%2Cx%5E3%2Cx%5E4%5D%29).

There is no UI component yet to change the plot limits. However, it can be done manually by opening the console and entering `app.plot_xlim = app.plot_ylim = [-10,10]; app.plot()`.

# Contributions

Feel free to contribute! Also, if you have an idea, please let me know (or submit it as an issue on Github)!

# Thanks to

 * Matplotlib
 * Sympy
 * Flask
 * Vue.js
 * Mathjax

Hosted on Heroku with gUnicorn.