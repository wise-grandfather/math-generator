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

def drobi(n: int, sign: str):
    examples_drobi = {}

    while len(examples_drobi) < n:
        a = randint(1,9)
        b = choice([i for i in range(2, 10) if a % i != 0])
        c = randint(1,9)
        d = choice([i for i in range(2, 10) if c % i != 0])

        fr1 = Fraction(a, b)
        fr2 = Fraction(c, d)

        example: str = f"{fr1} {sign} {fr2}"
        result: float = ops[sign](fr1, fr2)

        if example not in examples_drobi and fr1 != fr2:
            examples_drobi[example] = result

    return examples_drobi


def power(n: int, sign: str):
    examples_powers = {}

    while len(examples_powers) < n:
        example: str = ''

        if sign == 'root':
            b = randint(2, 4)
    
            if b == 3:
                valid = [i for i in range(-9, 10) if i not in (-1, 0, 1)]
                a = choice(valid)
                underRoot = a ** b
                result = a
                example = f"³√{underRoot}"
            else:
                valid = [i for i in range(2, 10)]
                a = choice(valid)
                underRoot = a ** b
                result = a 
                example = f"√{underRoot}" if b == 2 else f"⁴√{underRoot}"
        
        elif sign == '^':
            a = randint(-9, 9)
            b = randint(2,4)
            example = f"{a}^{b}"
            result = ops[sign](a, b)

        if example not in examples_powers:
            examples_powers[example] = result

    return examples_powers

def powerOperation(n: int, sign: str):
    examples = {}
    
    while len(examples) < n:
        a = randint(1, 9)
        d = choice([a, a*2, a*3])
        b = randint(-10, 10)
        c = randint(-10, 10)

        example = f"{a}^{b} {sign} {d}^{c}"
        result = ops[sign](a**b, d**c)

        if example not in examples:
            examples[example] = result

    return examples


skobkiTemplates = {
    "{a}(x {sign} {b})": lambda a, b, sign: f"{a}x {sign} {b*a}",
    "{a}({b} {sign} x)": lambda a, b, sign: f"{b*a} {sign} {a}x",
    "({a} {sign} x){b}": lambda a, b, sign: f"{b*a} {sign} {b}x",
    "(x {sign} {a}){b}": lambda a, b, sign: f"{b}x {sign} {b*a}"
}

def skobki(n: int, sign: str):
    examples = {}

    while len(examples) < n:
        T = choice(list(skobkiTemplates.keys()))
        F = skobkiTemplates[T]

        a = randint(-10, 10)
        b = randint(-10, 10)

        example = T.format(a=a, b=b, sign=sign)
        if example not in examples:
            examples[example] = F(a, b, sign)

    return examples



linearFnTemplates = {
    "{a}x {sign} {b} = {c}": lambda a, b, x, sign: ops[sign](a*x, b),
    "{b} {sign} {a}x = {c}": lambda a, b, x, sign: ops[sign](b, a*x),
    "{a}x {sign} {b}x = {c}": lambda a, b, x, sign: ops[sign](a*x, b*x),
    "({a} {sign} x)·{b} = {c}": lambda a, b, x, sign: ops[sign](a, x) * b,
    "{b}·({a} {sign} x) = {c}": lambda a, b, x, sign: ops[sign](a, x) * b,
}

def linearFuncs(n: int, sign: str):
    examples = {}

    while len(examples) < n:
        T = choice(list(linearFnTemplates.keys()))
        F = linearFnTemplates[T]

        a = randint(1,9)
        b = choice([i for i in range(1, 9) if i != a])
        x = randint(-10, 10)
        c = F(a, b, x, sign)

        example = T.format(a=a, b=b, c=c, sign=sign)

        if example not in examples:
            examples[example] = x

    return examples


GENERATORS = {
    'drobi': drobi,
    'power': power,
    'powerOp': powerOperation,
    'skobki': skobki,
    'linear': linearFuncs
}

def get_examples(config):
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