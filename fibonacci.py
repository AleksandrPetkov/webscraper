def get_fibonacci_number(arg):
    if arg == 1:
        return 0
    elif arg == 2:
        return 1
    else:
        return get_fibonacci_number(arg - 1) + get_fibonacci_number(arg - 2)


def main():
    res = get_fibonacci_number(3)
    print('The 20th number in fibonacchi line is', res)


def test_fibonacci():
    assert get_fibonacci_number(1) == 0, 'the 1st number of fibonacci sequence is 0'
    assert get_fibonacci_number(2) == 1, 'the 2nd number of fibonacci sequence is 1'
    assert get_fibonacci_number(5) == 3, 'the 5th number of fibonacci sequence is 3'
    assert get_fibonacci_number(10) == 34, 'the 10th number of fibonacci sequence is 34'
    assert get_fibonacci_number(15) == 377, 'the 15th number of fibonacci sequence is 377'


test_fibonacci()
main()
