n = int(input("Enter the number of lines for design: "))

def generate_text(length_of_text, index):
    word = "FORMULAQSOLUTIONS"
    generated_text = " "
    for count in range(length_of_text):
        generated_text += word[index % len(word)]
        index += 1
    return generated_text

def print_pattern(num_lines):
    num_lines = num_lines + (1 - num_lines % 2)
    index = 0
    for i in range(1, num_lines + 1, 2):
        space = (num_lines - i) // 2 + 1
        line = generate_text(i, index)
        index += 1
        print(" " * space + line)

    for i in range(num_lines - 2, 0, -2):
        space = (num_lines - i) // 2 + 1
        line = generate_text(i, index)
        index += 1
        print(" " * space + line)
print_pattern(n)
