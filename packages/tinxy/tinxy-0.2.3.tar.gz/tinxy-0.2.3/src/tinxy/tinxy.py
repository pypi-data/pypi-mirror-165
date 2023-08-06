__all__ = ['tinxy']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['strToLongs', 'encodes', 'longsToStr'])
@Js
def PyJsHoisted_encodes_(v, k, this, arguments, var=var):
    var = Scope({'v':v, 'k':k, 'this':this, 'arguments':arguments}, var)
    var.registers(['sum', 'q', 'z', 'y', 'p', 'mx', 'v', 'k', 'delta', 'n', 'e'])
    if (var.get('v').get('length')<Js(2.0)):
        var.get('v').put('1', Js(0.0))
    var.put('n', var.get('v').get('length'))
    var.put('delta', Js(2654435769))
    var.put('q', var.get('Math').callprop('floor', (Js(6.0)+(Js(52.0)/var.get('n')))))
    var.put('z', var.get('v').get((var.get('n')-Js(1.0))))
    var.put('y', var.get('v').get('0'))
    var.put('sum', Js(0.0))
    while ((var.put('q',Js(var.get('q').to_number())-Js(1))+Js(1))>Js(0.0)):
        var.put('sum', var.get('delta'), '+')
        var.put('e', (PyJsBshift(var.get('sum'),Js(2.0))&Js(3.0)))
        #for JS loop
        var.put('p', Js(0.0))
        while (var.get('p')<var.get('n')):
            try:
                var.put('y', var.get('v').get(((var.get('p')+Js(1.0))%var.get('n'))))
                var.put('mx', (((PyJsBshift(var.get('z'),Js(5.0))^(var.get('y')<<Js(2.0)))+(PyJsBshift(var.get('y'),Js(3.0))^(var.get('z')<<Js(4.0))))^((var.get('sum')^var.get('y'))+(var.get('k').get(((var.get('p')&Js(3.0))^var.get('e')))^var.get('z')))))
                var.put('z', var.get('v').put(var.get('p'), var.get('mx'), '+'))
            finally:
                    (var.put('p',Js(var.get('p').to_number())+Js(1))-Js(1))
    return var.get('v')
PyJsHoisted_encodes_.func_name = 'encodes'
var.put('encodes', PyJsHoisted_encodes_)
@Js
def PyJsHoisted_strToLongs_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['l', 'i', 's'])
    var.put('l', var.get('Array').create(var.get('Math').callprop('ceil', (var.get('s').get('length')/Js(4.0)))))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('l').get('length')):
        try:
            var.get('l').put(var.get('i'), (((var.get('s').callprop('charCodeAt', (var.get('i')*Js(4.0)))+(var.get('s').callprop('charCodeAt', ((var.get('i')*Js(4.0))+Js(1.0)))<<Js(8.0)))+(var.get('s').callprop('charCodeAt', ((var.get('i')*Js(4.0))+Js(2.0)))<<Js(16.0)))+(var.get('s').callprop('charCodeAt', ((var.get('i')*Js(4.0))+Js(3.0)))<<Js(24.0))))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    return var.get('l')
PyJsHoisted_strToLongs_.func_name = 'strToLongs'
var.put('strToLongs', PyJsHoisted_strToLongs_)
@Js
def PyJsHoisted_longsToStr_(l, this, arguments, var=var):
    var = Scope({'l':l, 'this':this, 'arguments':arguments}, var)
    var.registers(['str', 'l', 'i'])
    var.put('str', Js(''))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('l').get('length')):
        try:
            var.put('str', var.get('String').callprop('fromCharCode', (var.get('l').get(var.get('i'))&Js(255)), (PyJsBshift(var.get('l').get(var.get('i')),Js(8.0))&Js(255)), (PyJsBshift(var.get('l').get(var.get('i')),Js(16.0))&Js(255)), (PyJsBshift(var.get('l').get(var.get('i')),Js(24.0))&Js(255))), '+')
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    return var.get('str')
PyJsHoisted_longsToStr_.func_name = 'longsToStr'
var.put('longsToStr', PyJsHoisted_longsToStr_)
pass
pass
pass
pass


# Add lib to the module scope
tinxy = var.to_python()