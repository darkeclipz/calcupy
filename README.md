# MathPy

Calculus powered graphical calculator.

![Example](screenshots/ex1.png)

# Usage

The app has been deployed to [`https://pymath-api-heroku.herokuapp.com/`](https://pymath-api-heroku.herokuapp.com/).

The app will automatically detect how many variables there are in the expression. It is also possible to give an equality as expression.

The following options are available:

|Variables|Type|Action|
|--|--|--|
|0 - constants|Expression|It wil evaluate the expression.|
|1|Expression|Line plot|
|1|Expression|Derivative|
|1|Expression|Second derivative|
|1|Expression|Indefinite integral|
|1|Expression|Integrate from 0 to T|
|1|Expression|Integrate from -inf to inf|
|2|Expression|Surface plot|
|2+|Expression|Partial derivatives|
|2+|Expression|Second partial derivatives|
|1+|Equality|Solve for variable|

# Examples

The following are examples of functions that are understood:

 * 1 variable: `1 / (1 + x^2)`.
 * 2 variables: `1 / (1 + x^2 + y^2)`, `x*y`, `sqrt(x^2 + y^2)`, `exp(y) * cos(x) + exp(x) * sin(y)`.
 * equalities: `z^3 + z^2 + z^1 + z = 0`, `x^2 + x + 3 = 0`.

It is also possible to construct matrices with `Matrix([[1,2],[3,4]])`. It is also possible to create multiple line plots with the following matrix: `Matrix([x,x^2,x^3,x^4])`. Imaginairy numbers can be declared with `im(x)`.

# Thanks to

 * Matplotlib
 * Sympy
 * Flask
 * Vue.js

Hosted on Heroku with gUnicorn.