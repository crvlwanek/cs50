text = input("Text: ")
# 0.0588 * L - 0.296 * S - 15.8
letters, words, sentences = 0, 1, 0
for char in text:
    if char.isalpha():
        letters += 1
    elif char.isspace():
        words += 1
    elif char in ['.', '!', '?']:
        sentences += 1

L = letters / words * 100
S = sentences / words * 100
index = 0.0588 * L - 0.296 * S - 15.8
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {round(index)}")
