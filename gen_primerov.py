from random import randint, choice
from fractions import Fraction
import operator

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '^': operator.pow,
    'root': lambda a, b: a ** (1 / b)
}

linearFnTemplates = {
    "{a}x {sign} {b} = {c}": lambda a, b, x, sign: ops[sign](a*x, b),
    "{b} {sign} {a}x = {c}": lambda a, b, x, sign: ops[sign](b, a*x),
    "{a}x {sign} {b}x = {c}": lambda a, b, x, sign: ops[sign](a*x, b*x),
    "({a} {sign} x)·{b} = {c}": lambda a, b, x, sign: ops[sign](a, x) * b,
    "{b}·({a} {sign} x) = {c}": lambda a, b, x, sign: ops[sign](a, x) * b,
}

def drobi(n: int, sign: str):
    examples_drobi = {}

    while len(examples_drobi) < n:
        a = randint(1,9)
        b = randint(2,9)
        c = randint(1,9)
        d = randint(2,9)

        fr1 = Fraction(a, b)
        fr2 = Fraction(c, d)

        example: str = f"{fr1} {sign} {fr2}"
        result: float = ops[sign](fr1, fr2)

        if example not in examples_drobi:
            examples_drobi[example] = result

    return examples_drobi

def power(n: int, sign: str):
    examples_powers = {}

    while len(examples_powers) < n:
        a = randint(-9, 9)
        b = randint(2,4)

        example: str = ''

        if sign == 'root':
            valid = [i for i in range(-9, 10) if i not in (-1, 0, 1)]
            a = choice(valid)
            underRoot = a ** b

            if b == 2:
                example = f"√{underRoot}"
            elif b == 3:
                example = f"³√{underRoot}"
            else:
                example = f"⁴√{underRoot}"
            
            result = a

        elif sign == '^':
            example = f"{a}^{b}"
            result = ops[sign](a, b)

        if example not in examples_powers:
            examples_powers[example] = result

    return examples_powers

def linearFuncs(n: int, sign: str):
    examples = {}

    while len(examples) < n:
        T = choice(list(linearFnTemplates.keys()))
        F = linearFnTemplates[T]

        a = randint(1,9)
        b = randint(1,9)
        x = randint(-10, 10)
        c = F(a, b, x, sign)

        example = T.format(a=a, b=b, c=c, sign=sign)

        if example not in examples:
            examples[example] = x

    return examples


GENERATORS = {
    'drobi': drobi,
    'power': power,
    'linear': linearFuncs
}

def get_examples(config): #config = {drobi: [[10, '-'], [10, '+']], power: [[10, '^'], [10, 'root']], linear: [[10, '-'], [10, '+']]}
    result = {}
    
    for gen_name, tasks in config.items():
        if gen_name not in GENERATORS:
            continue
            
        gen_func = GENERATORS[gen_name]
        
        for task in tasks:
            n, sign = task[0], task[1]
            examples = gen_func(n, sign)
            result.update(examples)
    
    return result