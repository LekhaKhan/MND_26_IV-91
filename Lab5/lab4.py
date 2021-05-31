from random import randint
from scipy.stats import t
import csv
from Lab5 import main5


def write_data(filename, data):
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(('X0', 'X1', 'X2', 'X3', 'X1X2', 'X1X3', 'X2X3', 'X1X2X3', 'Y1', 'Y2', 'Y3', 'Y_avg'))
        for i in range(8):
            writer.writerow([data[0][i], data[1][i], data[2][i], data[3][i], data[4][i], data[5][i],
              data[6][i], data[7][i], data[8][i], data[9][i], data[10][i], data[11][i]])


def naturalize(matrix_of_plan, min_max_arr):
    result = []
    for i in matrix_of_plan:
        result.append(min_max_arr[1]) if i == 1 else result.append(min_max_arr[0])
    return result


def cocharans_test(y_arr, y_avg, m, N):
    # Перевірка однорідності дисперсії за критерієм Кохрена
    dispersion = []
    for i in range(len(y_arr[0])):
        current_sum = 0
        for j in range(len(y_arr)):
            current_sum += (y_arr[j][i] - y_avg[j]) ** 2
        dispersion.append(current_sum / len(y_arr))

    print('dispersion:', dispersion)

    gp = max(dispersion) / sum(dispersion)
    print('Gp =', gp)

    # Рівень значимості q = 0.05
    # f1 = m - 1
    # f2 = N

    # За таблицею Gт = 0.5157
    if gp < 0.5157:
        print('Дисперсія однорідна')
        return dispersion
    else:
        print('Дисперсія неоднорідна')
        return None


def students_test(x0_plan1, x1_plan1, x2_plan1, x3_plan1, y_avg_arr, dispersion, m):
    # Оцінка значимості коефіцієнтів регресії згідно критерію Стьюдента
    s2b = sum(dispersion) / 8
    s2bs_avg = s2b / 8 * m
    sb = s2bs_avg ** (1 / 2)

    beta_arr = [
        sum([y_avg_arr[i] * x0_plan1[i] for i in range(8)]) / 8,
        sum([y_avg_arr[i] * x1_plan1[i] for i in range(8)]) / 8,
        sum([y_avg_arr[i] * x2_plan1[i] for i in range(8)]) / 8,
        sum([y_avg_arr[i] * x3_plan1[i] for i in range(8)]) / 8,
        sum([y_avg_arr[i] * x1_plan1[i] * x2_plan1[i] for i in range(8)]) / 8,
        sum([y_avg_arr[i] * x1_plan1[i] * x3_plan1[i] for i in range(8)]) / 8,
        sum([y_avg_arr[i] * x2_plan1[i] * x3_plan1[i] for i in range(8)]) / 8,
        sum([y_avg_arr[i] * x1_plan1[i] * x2_plan1[i] * x3_plan1[i] for i in range(8)]) / 8,
    ]

    print('beta:', beta_arr)
    t_arr = [abs(beta_arr[i]) / sb for i in range(8)]
    print('t:', t_arr)

    # f3 = f1*f2 = 2*8 = 16
    f1 = m - 1
    f2 = 8
    f3 = f1 * f2

    b_arr = []
    for i in range(len(t_arr)):
        if t_arr[i] > t.ppf(q=0.975, df=f3):
            b_arr.append(t_arr[i])
        else:
            print(f'Коефіцієнт b{i} приймаємо не значним')
            b_arr.append(0)

    return b_arr, s2b


def fishers_test(b_arr, s2b, y_avg, y_res, m):
    # Критерій Фішера
    d = len([i for i in b_arr if i != 0])  # кількість значимих коефіцієнтів
    print(f'd = {d}')
    s2_ad = m * sum([(y_res[i] - y_avg[i]) ** 2 for i in range(8)]) / 8 - d
    fp = s2_ad / s2b
    print(f'Fp = {fp}')


    # Fт = 2.7
    if fp > 2.7:
        print('Рівняння регресії неадекватно оригіналу при рівні значимості 0.05')
        return False
    else:
        print('Рівняння регресії адекватно оригіналу при рівні значимості 0.05')
        return True


def main4(m, x1, x2, x3):
    N = 8  # Кількість комбінацій

    # Рівняння регресії з ефектом взаємодії
    print('ŷ = b0 + b1*x1 + b2*x2 + b3*x3 + b12*x1*x2 + b13*x1*x3 + b23*x2*x3 + b123*x1*x2*x3')

    # x1 = [10, 60]
    # x2 = [15, 50]
    # x3 = [15, 20]

    # Матриця планування експерименту з +1,-1
    x0_plan1 = [1, 1, 1, 1, 1, 1, 1, 1]
    x1_plan1 = [-1, -1, 1, 1, -1, -1, 1, 1]
    x2_plan1 = [-1, 1, -1, 1, -1, 1, -1, 1]
    x3_plan1 = [1, -1, -1, 1, -1, 1, 1, -1]
    x12_plan1 = [x1_plan1[i] * x2_plan1[i] for i in range(len(x1_plan1))]
    x13_plan1 = [x1_plan1[i] * x3_plan1[i] for i in range(len(x1_plan1))]
    x23_plan1 = [x2_plan1[i] * x3_plan1[i] for i in range(len(x1_plan1))]
    x123_plan1 = [x1_plan1[i] * x2_plan1[i] * x3_plan1[i] for i in range(len(x1_plan1))]
    print('x0:', x0_plan1)
    print('x1:', x1_plan1)
    print('x2:', x2_plan1)
    print('x3:', x3_plan1)
    print('x12:', x12_plan1)
    print('x13:', x13_plan1)
    print('x23:', x23_plan1)
    print('x123:', x123_plan1)

    # Матриця планування з натуралізованими значеннями факторів
    x1_plan2 = naturalize(x1_plan1, x1)
    x2_plan2 = naturalize(x2_plan1, x2)
    x3_plan2 = naturalize(x3_plan1, x3)
    print()
    print('x1:', x1_plan2)
    print('x2:', x2_plan2)
    print('x3:', x3_plan2)

    x_avg_max = (max(x1_plan2) + max(x2_plan2) + max(x3_plan2)) / 3
    x_avg_min = (min(x1_plan2) + min(x2_plan2) + min(x3_plan2)) / 3
    print()
    print(f'x_avg_max = {x_avg_max}')
    print(f'x_avg_min = {x_avg_min}')

    # Діапазон y
    y_max = int(200 + x_avg_max)
    y_min = int(200 + x_avg_min)
    print()
    print(f'y_max = {y_max}')
    print(f'y_min = {y_min}')

    y_arr = [[randint(y_min, y_max) for _ in range(N)] for _ in range(m)]
    for i in range(len(y_arr)):
        print(f'y{i+1}: {y_arr[i]}')

    y_avg = []
    for i in range(len(y_arr[0])):
        current_sum = 0
        for j in range(len(y_arr)):
            current_sum += y_arr[j][i]
        y_avg.append(current_sum/len(y_arr))
    print('y average:', y_avg)

    matrix = [x0_plan1, x1_plan1, x2_plan1, x3_plan1, x12_plan1, x13_plan1,
              x23_plan1, x123_plan1, y_arr[0], y_arr[1], y_arr[2], y_avg]

    write_data('output.csv', matrix)

    b0 = sum(y_avg) / N
    b1 = sum([y_avg[i] * x1_plan1[i] for i in range(N)]) / N
    b2 = sum([y_avg[i] * x2_plan1[i] for i in range(N)]) / N
    b3 = sum([y_avg[i] * x3_plan1[i] for i in range(N)]) / N
    b12 = sum([y_avg[i] * x1_plan1[i] * x2_plan1[i] for i in range(N)]) / N
    b13 = sum([y_avg[i] * x1_plan1[i] * x3_plan1[i] for i in range(N)]) / N
    b23 = sum([y_avg[i] * x2_plan1[i] * x3_plan1[i] for i in range(N)]) / N
    b123 = sum([y_avg[i] * x1_plan1[i] * x2_plan1[i] * x3_plan1[i] for i in range(N)]) / N

    b_list = [b0, b1, b2, b3, b12, b13, b23, b123]

    print(f'y = {b0} + {b1}*x1 + {b2}*x2 + {b3}*x3 + {b12}*x1*x2 + {b13}*x1*x3 + {b23}*x2*x3 + {b123}*x1*x2*x3')
    for i in range(N):
        print(f'''ŷ = {b0 + b1 * x1_plan1[i] + b2 * x2_plan1[i] + b3 * x3_plan1[i] + b12 * x1_plan1[i] * x2_plan1[i]
                       + b13 * x1_plan1[i] * x3_plan1[i] + b23 * x2_plan1[i] * x3_plan1[i]
                       + b123 * x1_plan1[i] * x2_plan1[i] * x3_plan1[i]}''')

    dispersion = cocharans_test(y_arr, y_avg, m, N)
    if dispersion:
        t_arr, s2b = students_test(x0_plan1, x1_plan1, x2_plan1, x3_plan1, y_avg, dispersion, m)

        b_arr = []
        for i in range(len(b_list)):
            b = b_list[i] if t_arr[i] != 0 else 0
            b_arr.append(b)

        y_res = []
        for i in range(N):
            y = b_arr[0] + b_arr[1] * x1_plan1[i] + b_arr[2] * x2_plan1[i] + b_arr[3] * x3_plan1[i] \
                           + b_arr[4] * x1_plan1[i] * x2_plan1[i] \
                           + b_arr[5] * x1_plan1[i] * x3_plan1[i] + b_arr[6] * x2_plan1[i] * x3_plan1[i] \
                           + b_arr[7] * x1_plan1[i] * x2_plan1[i] * x3_plan1[i]
            print(f'ŷ = {y}')
            y_res.append(y)
        if not fishers_test(b_arr, s2b, y_avg, y_res, m):
            main5(m, x1, x2, x3)
            exit()
    else:
        main4(m+1, x1, x2, x3)
        exit()


if __name__ == '__main__':
    # main()
    pass