x = '''
var outer = func() {
    ret func() {
    };
};

var fn1 = outer();
print !fn1;

}'''

print(x[46])