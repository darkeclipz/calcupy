function replaceAll(str, find, replace) {
    return str.replace(new RegExp(find, 'g'), replace);
}

// Parses an expression recursively, and rewrites matrix shorthand notation
// that is in the expression to expanded matrix notation that is understood
// by SymPy.
let parseMatrixShorthand = function(expr) {

    // List case where expr: 1,2,3,4, or x+y=2, x-y=1
    if(expr.indexOf(',') >= 0 && expr.indexOf('[') < 0 && expr.indexOf('(') < 0)
        return 'Matrix([' + expr + '])';
    
    // Make sure a matrix is defined.
    if(expr.indexOf('[') < 0) return expr; // No matrix defined
    
    // Find the opening tag.
    let start = expr.indexOf('[');
    let index = start + 1;

    // Make sure that the expression isn't already in
    // matrix form, e.g.: Matrix([1,2,3]) can be skipped.
    let mStart = expr.indexOf('Matrix');
    if(mStart >= 0 && mStart <= start) {

        // Make sure there is an opening tag.
        if(expr.indexOf('(', mStart) <= 0) {
            console.warn('No opening tag ( found for the matrix.');
            return expr;
        }

        // Find the closing tag, and parse the rest of the expression.
        if(expr.indexOf(')', mStart) <= 0) {
            console.warn('No closing tag ) found for the matrix.')
            return expr;
        }

        let mIndex = expr.indexOf('(', mStart) + 1;
        let mStack = 1;

        // Find the closing tag.
        while(mStack && mIndex < expr.length){
            if(expr[mIndex] == '(') mStack++;
            if(expr[mIndex] == ')') mStack--;
            mIndex++;
        }

        // Verify that an end tag is found.
        if(mStack > 0) {
            console.warn('No matching end tag ) found for the matrix.');
            return expr;
        }

        let close = mIndex + 1;
        return expr.substr(0, close) + parseMatrixShorthand(expr.substr(close));
    }

    // Make sure that there is a closing tag.
    if(expr.indexOf(']', index) <= 0) {
        console.warn('No closing tag ] found for the expression.');
        return expr;
    }

    // Find where the closing tag is, taking sub tags into account.
    let stack = 1;
    while(stack && index < expr.length) {
        if(expr[index] == '[') stack++;
        if(expr[index] == ']') stack--;
        index++;
    }

    // Make sure that the stack is empty and the expression
    // is parsed completely.
    if(stack > 0) {
        console.warn('No matching end tag ] found for the expression.');
        return expr;
    }

    // Replace the shorthand notation with the matrix notation.
    let end = index;
    let subexpr = expr.substr(start, end - start);
    return expr.substr(0, start) + 'Matrix(' + subexpr + ')' + parseMatrixShorthand(expr.substr(end));
};

// Create a matrix from a list of numbers.
// Example: 1 2 3 4 --> [1, 2, 3, 4]
let parseSeperatedDigits = function(str) {
    if(/[\d][ \t][\d]/.test(str)) {
        let digits = str.split(' ').filter(s => /^[\.\d]+$/.test(s)).map(s => Number(s));
        return '[' + digits.join(', ') + ']';
    }
    else return str;
}