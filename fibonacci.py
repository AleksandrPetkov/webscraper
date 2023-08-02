def get_fibonacci_number(arg):
    if arg == 1:
        return 0
    elif arg == 2:
        return 1
    else:
        return get_fibonacci_number(arg - 1) + get_fibonacci_number(arg - 2)


def main():
    res = get_fibonacci_number(20)
    print('The 20th number in fibonacchi line is', res)

main()
