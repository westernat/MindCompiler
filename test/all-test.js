let a = 1
let b = a
let c = a / b * (5 % 2 ** 3)
c += 1

if (a == 1) {
    print(a)
} else if (a > 1) {
    print(b)
} else if (a < 1) {
    print(c)
} else {
    print("?")
}