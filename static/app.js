var http = new HTTP();
var app = new Vue({
    el: '#app',
    data: {
        expression: "exp(y) * cos(x) + exp(x) * sin(y)",
        expression_parsed: "",
        expression_latex: "",
        expression_error: false,
        expression_equality: false,
        expression_inequality: false,
        variables: [],
        parsed: false,
        plot_show: false,
        plot_base64: "",
        plot_error: "",
        plot_xlim: [-5, 5],
        plot_ylim: [-5, 5],
        action_show: false,
        action_in: "",
        action_out: "",
        action_error: ""
    },
    methods: {
        expr: function() {

            let castedExpression = replaceAll(this.expression, '[\\^]', '**');
            castedExpression = replaceAll(castedExpression, 'abs', 'Abs');

            if(castedExpression.indexOf('>') >= 0 || castedExpression.indexOf('<') >= 0)
                this.expression_inequality = true;

            if(!this.expression_inequality && castedExpression.indexOf('=') >= 0) {
                let parts = castedExpression.split('=');
                castedExpression = 'Eq(' + parts[0] + ',' + parts[1] + ')';
                this.expression_equality = true;
            }

            return castedExpression;
        },
        parse: function() {
            this.reset(); 
            this.setUrl();
            http.post('/expression', {'expression': this.expr() }, 
                (result) => {
                    app.expression_parse = result.expression;
                    app.expression_latex = replaceAll(result.expression_latex, 'frac', 'dfrac');
                    app.variables = result.variables;
                    app.parsed = true;
                    this.latex();
                    if((app.variables.length == 2 || app.variables.length == 1) && !app.expression_equality && !app.expression_inequality)
                        app.plot();
                },
                (error) => { console.log(error); app.expression_error = true; }
            );
        },
        simplify: function() {
            this.resetAction();
            http.post('/simplify', { 'expression': this.expr() }, 
                (result) => {
                    this.action_in = 'The simplification of $' + result.in + '$ is:';
                    this.action_out = '$$' + result.out + '$$';
                    this.latex();
                },
                (error) => this.actionError(error)
            );
        },
        expand: function(trig = false) {
            this.resetAction();
            http.post('/expand', { 'expression': this.expr(), 'trig': trig }, 
                (result) => {
                    this.action_in = 'The expansion of $' + result.in + '$ is:';
                    this.action_out = '$$' + result.out + '$$';
                    this.latex();
                },
                (error) => this.actionError(error)
            );
        },
        factor: function() {
            this.resetAction();
            http.post('/factor', { 'expression': this.expr() }, 
                (result) => {
                    this.action_in = 'The factorization of $' + result.in + '$ is:';
                    this.action_out = '$$' + result.out + '$$';
                    this.latex();
                },
                (error) => this.actionError(error)
            );
        },
        factors: function() {
            this.resetAction();
            http.post('/factors', { 'expression': this.expr() }, 
                (result) => {
                    this.action_in = 'The factors of $' + result.in + '$ are:';
                    this.action_out = '$$' + result.out + '$$';
                    this.latex();
                },
                (error) => this.actionError(error)
            );
        },
        primitive: function() {
            this.resetAction();
            http.post('/primitive', { 'expression': this.expr() }, 
                (result) => {
                    this.action_in = 'The primitive of $' + result.in + '$ is:';
                    this.action_out = '$$' + result.out + '$$';
                    this.latex();
                },
                (error) => this.actionError(error)
            );
        },
        diff: function(to) {
            this.resetAction();
            http.post('/diff', { 'expression': this.expr(), 'var': to }, 
                (result) => {
                    this.action_in = 'The derivative of $' + result.in + '$ with respect to $' + result.var + '$ is:';
                    this.action_out = '$$' + result.out + '$$';
                    this.latex();
                },
                (error) => this.actionError(error)
            );
        },
        diff2: function(to) {
            this.resetAction();
            http.post('/diff2', { 'expression': this.expr(), 'var': to }, 
                (result) => {
                    this.action_in = 'The second derivative of $' + result.in + '$ with respect to $' + result.var + '$ is:';
                    this.action_out = '$$' + result.out + '$$';
                    this.latex();
                },
                (error) => this.actionError(error)
            );
        },
        grad: function(to) {
            this.resetAction();
            http.post('/grad', { 'expression': this.expr() }, 
                (result) => {
                    this.action_in = 'The gradient $\\nabla f$ of $' + result.in + '$ is:';
                    this.action_out = '$$' + result.out + '$$';
                    this.latex();
                },
                (error) => this.actionError(error)
            );
        },
        hessian: function(to) {
            this.resetAction();
            http.post('/hessian', { 'expression': this.expr() }, 
                (result) => {
                    this.action_in = 'The hessian matrix $H$ of $' + result.in + '$ is:';
                    this.action_out = '$$' + result.out + ',$$ where the determinant $\\textrm{det}(H)$ is:$$' + result.hessian + '$$';
                    this.latex();
                },
                (error) => this.actionError(error)
            );
        },
        integrate: function(v, from='', to='') {
            this.resetAction();
            http.post('/integrate', { 'expression': this.expr(), 'var': v, 'from': from, 'to': to }, 
                (result) => {
                    let limits = to ? '_{' + from.replace('oo', '\\infty') + '}^{' + to.replace('oo', '+\\infty') + '}' : '';
                    this.action_in = 'The integral of $\\int ' + limits + result.in + '\\ d' + result.var + '$ is:';
                    this.action_out = '$$' + result.out + (result.out.indexOf('int') < 0 && !to ? ' + C$$' : '$$');
                    this.latex();
                },
                (error) => this.actionError(error)
            );
        },
        solveFor: function(v) {
            this.resetAction();
            http.post('/solvefor', { 'expression': this.expr(), 'var': v }, 
                (result) => {
                    this.action_in = 'Solving $' + result.in + '$ for $' + result.var + '$ gives:';
                    append_var = !app.expression_inequality ? result.var + '=' : '';
                    this.action_out = '$$' + append_var + result.out + '$$';
                    this.latex();
                },
                (error) => this.actionError(error)
            );
        },
        plot: function() {
            this.resetPlot();
            http.post('/plot', { 'expression': this.expr(), 'xlim': this.plot_xlim, 'ylim': this.plot_ylim }, 
                (result) => { app.plot_base64 = result.img; },
                (error) => { console.warn(error); app.plot_error = error; }
            );
        },
        cplot: function() {
            this.resetPlot();
            http.post('/cplot', { 'expression': this.expr(), 'xlim': this.plot_xlim, 'ylim': this.plot_ylim }, 
                (result) => { app.plot_base64 = result.img; },
                (error) => { console.warn(error); app.plot_error = error; }
            );
        },
        gplot: function() {
            this.resetPlot();
            http.post('/gplot', { 'expression': this.expr(), 'xlim': this.plot_xlim, 'ylim': this.plot_ylim }, 
                (result) => { app.plot_base64 = result.img; },
                (error) => { console.warn(error); app.plot_error = error; }
            );
        },
        actionError: function(e) {
            this.action_error = e;
            console.warn(error);
        },
        reset: function() {
            this.expression_error = false;
            this.expression_equality = false;
            this.expression_inequality = false;
            this.parsed = false;
            this.expression_parsed = false;
            this.expression_latex = false;
            this.variables = [];
            this.plot_show = false;
            this.plot_base64 = "";
            this.plot_error = "";
            this.resetAction();
            this.action_show = false;
        },
        resetAction: function() {
            this.action_show = true;
            this.action_in = "";
            this.action_out = "";
            this.action_error = "";
            if(this.action_out)
                document.getElementById('action-result').innerHTML = "{{action_in}}<hr/>{{action_out}}";
        },
        resetPlot: function() {
            this.plot_show = true;
            this.plot_base64 = "";
            this.plot_error = "";
        },
        setUrl: function() {
            window.history.pushState({page: "index"}, "expression", "?expr=" + encodeURIComponent(this.expression));
        },
        readUrl: function() {
            let url = new URL(window.location.href);
            let expr = url.searchParams.get('expr');
            if(expr) 
                this.expression = expr;
        },
        latex: function() {
            this.$nextTick(function() {
                MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
            });
        }
    }
})

app.readUrl();
app.parse();

window.onpopstate = function(e) {
    if(e.state) {
        app.readUrl();
        app.parse();
    }
}