#Function to count frequency of characters
def char_count(s):
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    return freq
val = char_count("sarrroj")
print(val)
