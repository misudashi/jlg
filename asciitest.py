left_text = "Left Text"
right_text = "Right Text"

total_length = 100
space_count = total_length - len(left_text) - len(right_text)

# Calculate the number of spaces needed for each side


# Construct the final string with the desired length
final_string = left_text + " " * space_count + right_text

print(final_string)
print("=" * 100)