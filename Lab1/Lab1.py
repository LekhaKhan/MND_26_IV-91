from random import randint
import time


start_time = time.time()

def function():
    factor = [randint(0, 20) for _ in range(8)]
    x0 = (max(factor) + min(factor)) / 2
    dx = x0 - min(factor)
    x_n = [(factor[i] - x0) / dx for i in range(8)]
    return factor, x0, dx, x_n


def main():
    a0 = randint(0, 20)
    a1 = randint(0, 20)
    a2 = randint(0, 20)
    a3 = randint(0, 20)

    print(f'Y = {a0} + {a1}*X1 + {a2}*X2 + {a3}*X3')
    print('-' * 28)

    x1_factor, x01, dx1, x1_n = function()
    x2_factor, x02, dx2, x2_n = function()
    x3_factor, x03, dx3, x3_n = function()

    print(f'X1: {x1_factor}\nX01 = {x01}\nDX1 = {dx1}\nX1n: {x1_n}')
    print('-' * 50)

    print(f'X2: {x2_factor}\nX02 = {x02}\nDX2 = {dx2}\nX2n: {x2_n}')
    print('-' * 50)

    print(f'X3: {x3_factor}\nX03 = {x03}\nDX3 = {dx3}\nX3n: {x3_n}')
    print('-' * 50)

    y = [a0 + a1 * x1_factor[i] + a2 * x2_factor[i] + a3 * x3_factor[i] for i in range(8)]
    y_et = a0 + a1 * x01 + a2 * x02 + a3 * x03

    print(f'Y: {y}')
    print(f'Yet = {y_et}')
    print('-' * 50)

    res = [(y[i] - y_et) ** 2 for i in range(8)]
    print(f'(Y-Yet)^2: {res}')
    print(f'max((Y-Yet)^2) = {max(res)}')
    index = res.index(max(res))
    print(f'Шуканий експеримент: X1 = {x1_factor[index]}, X2 = {x2_factor[index]}, X3 = {x3_factor[index]}')
    print(f'Y = {a0} + {a1}*{x1_factor[index]} + {a2}*{x2_factor[index]} + {a3}*{x3_factor[index]}')
    print('Y =', a0 + a1*x1_factor[index] + a2*x2_factor[index] + a3*x3_factor[index])


if __name__ == '__main__':
    main()

    print("--- %s seconds ---" % (time.time() - start_time))