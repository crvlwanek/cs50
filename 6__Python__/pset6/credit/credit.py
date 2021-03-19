AMEX = ["34", "37"]
MASTERCARD = [str(i) for i in range(51, 56)]
VISA = ["4"]

number = "a"
while not number.isdigit():
    number = input("Number: ")
card_type = None
if number[:2] in AMEX:
    card_type = "AMEX"
elif number[:2] in MASTERCARD:
    card_type = "MASTERCARD"
elif number[0] in VISA:
    card_type = "VISA"

if card_type:
    number = int(number)
    total = 0
    mult = False
    while number:
        digit = (number % 10) * (1 + int(mult))
        while digit:
            total += digit % 10
            digit //= 10
        number //= 10
        mult = not mult
    if total % 10 == 0:
        print(card_type)
    else:
        print("INVALID")

else:
    print("INVALID")