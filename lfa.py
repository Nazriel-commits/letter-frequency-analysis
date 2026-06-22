###########################################################################
#lfa.py - Letter Frequency Analysis for Substitution Cipher
#
#Overview:
# This program performs letter frequency analysis on ciphertext to help break a substitution cipher. 
# It compares frequencies against standard English and suggests possible letter mappings.
#
#What it does:
#  - Counts frequency of each letter in the ciphertext
#  - Generates a frequency table and bar chart visualization
#  - Compares ciphertext frequencies with standard English frequencies
#  - Performs bigram analysis for additional pattern recognition
#  - Suggests initial substitution mappings based on frequency ranking
#  - Allows manual refinement of the substitution table
#  - Decrypts the ciphertext using both automated and manual mappings
#
#Author: Nazriel Al-Hafidz
###########################################################################

import sys
from collections import Counter
import matplotlib.pyplot as plt

#More accurate English letter frequencies (from 4.5 billion chars i referenced source in my report)
ENGLISH_FREQ = {
    'A': 8.55, 'B': 1.60, 'C': 3.16, 'D': 3.87, 'E': 12.10,
    'F': 2.18, 'G': 2.09, 'H': 4.96, 'I': 7.33, 'J': 0.22,
    'K': 0.81, 'L': 4.21, 'M': 2.53, 'N': 7.17, 'O': 7.47,
    'P': 2.07, 'Q': 0.10, 'R': 6.33, 'S': 6.73, 'T': 8.94,
    'U': 2.68, 'V': 1.06, 'W': 1.83, 'X': 0.19, 'Y': 1.72,
    'Z': 0.11
}

#Common English bigrams (for additional analysis)
COMMON_BIGRAMS = {
    'TH': 2.71, 'HE': 2.33, 'IN': 2.03, 'ER': 1.78, 'AN': 1.61,
    'RE': 1.41, 'ES': 1.32, 'ON': 1.32, 'ST': 1.25, 'NT': 1.17,
    'EN': 1.13, 'AT': 1.12, 'ED': 1.08, 'ND': 1.07, 'TO': 1.07,
    'OR': 1.06, 'EA': 1.00, 'TI': 0.99, 'AR': 0.98, 'TE': 0.98
}

#Load ciphertext from file
def load_ciphertext(filename):
    with open(filename, 'r') as f:
        return f.read()

#Count frequency of each letter in text"""
def frequency_analysis(text):
    letters_only = [c.upper() for c in text if c.isalpha()]
    total = len(letters_only)
    counter = Counter(letters_only)
    
    freq = {}
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        freq[letter] = (counter.get(letter, 0) / total) * 100 if total > 0 else 0
    
    return freq, total, counter

#Count frequency of bigrams (pairs of letters) in text
def bigram_analysis(text):

    letters_only = [c.upper() for c in text if c.isalpha()]
    bigrams = [''.join(letters_only[i:i+2]) for i in range(len(letters_only)-1)]
    bigram_counts = Counter(bigrams)
    total = len(bigrams)
    
    bigram_freq = {}
    for bigram, count in bigram_counts.most_common(20):
        bigram_freq[bigram] = (count / total) * 100 if total > 0 else 0
    
    return bigram_freq, total

#Suggest possible substitutions based on frequency ranking
def suggest_mappings(cipher_freq, english_freq):
    cipher_sorted = sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True)
    english_sorted = sorted(english_freq.items(), key=lambda x: x[1], reverse=True)
    
    mappings = {}
    for i, (cipher_letter, _) in enumerate(cipher_sorted):
        if i < len(english_sorted):
            mappings[cipher_letter] = english_sorted[i][0]
    
    return mappings

#Apply substitution mapping to text
def apply_substitution(text, mapping):
    result = []
    for ch in text:
        if ch.upper() in mapping:
            mapped = mapping[ch.upper()]
            result.append(mapped if ch.isupper() else mapped.lower())
        else:
            result.append(ch)
    return ''.join(result)

#Generate bar chart of letter frequencies
def plot_frequency_chart(cipher_freq, filename):

    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    frequencies = [cipher_freq[letter] for letter in letters]
    
    plt.figure(figsize=(14, 6))
    bars = plt.bar(letters, frequencies, color='blue', edgecolor='black')
    
    #Add value labels on top of bars
    for bar, freq in zip(bars, frequencies):
        if freq > 0:
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                     f'{freq:.2f}%', ha='center', va='bottom', fontsize=8)
    
    plt.xlabel('Letters', fontsize=12)
    plt.ylabel('Relative Frequency (%)', fontsize=12)
    plt.title(f'Letter Frequency Analysis of {filename}', fontsize=14)
    plt.ylim(0, max(frequencies) * 1.15)
    plt.grid(axis='y', alpha=0.3)
    
    #Save the chart
    plt.savefig('letter_frequency_chart.png', dpi=150, bbox_inches='tight')
    plt.show()

def main():
    if len(sys.argv) != 2:
        print("Usage: python task1.py <ciphertext_file>")
        print("Example: python task1.py intercepted_message.txt")
        return
    
    filename = sys.argv[1]
    
    try:
        ciphertext = load_ciphertext(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return
    
    #Perform analyses
    freq, total_letters, counter = frequency_analysis(ciphertext)
    bigram_freq, total_bigrams = bigram_analysis(ciphertext)
    
    print("=" * 70)
    print("Letter Frequency Analysis")
    print("=" * 70)
    print(f"Ciphertext file: {filename}")
    print(f"Total letters analyzed: {total_letters}")
    print(f"Total bigrams analyzed: {total_bigrams}\n")
    
    #Frequency table
    print("=" * 70)
    print("Letter Frequency Table")
    print("=" * 70)
    print(f"{'Letter':<8} {'Cipher Freq%':<15} {'English Freq%':<15} {'Difference':<12}")
    print("-" * 55)
    
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        cipher_pct = freq[letter]
        english_pct = ENGLISH_FREQ[letter]
        diff = cipher_pct - english_pct
        print(f"{letter:<8} {cipher_pct:>12.2f}%    {english_pct:>12.2f}%    {diff:>+9.2f}%")
    
    #Generate and show chart
    print("\n" + "=" * 70)
    print("Creating the frequency chart...")
    print("=" * 70)
    plot_frequency_chart(freq, filename)
    
    #Bigram analysis (for additional insight)
    print("\n" + "=" * 70)
    print("Top 15 bigrams identified")
    print("=" * 70)
    print(f"{'Bigram':<10} {'Frequency %':<15} {'Common English Bigram':<20}")
    print("-" * 50)
    
    for i, (bigram, pct) in enumerate(sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)[:15]):
        common_pct = COMMON_BIGRAMS.get(bigram, 0)
        if common_pct > 0:
            print(f"{bigram:<10} {pct:>12.2f}%    {bigram} = {common_pct:.2f}%")
        else:
            print(f"{bigram:<10} {pct:>12.2f}%    (not in top 20 common)")
    
    #Suggested mapping based on frequency
    print("\n" + "=" * 70)
    print("Suggested substitution mapping (by frequency ranking)")
    print("=" * 70)
    mappings = suggest_mappings(freq, ENGLISH_FREQ)
    
    print("\nCiphertext Letter -> Suggested Plaintext:")
    for cipher_letter, plain_letter in sorted(mappings.items()):
        print(f"      {cipher_letter}      ->        {plain_letter}")
    
    #Apply suggested mapping
    decrypted = apply_substitution(ciphertext, mappings)
    print("\n" + "=" * 70)
    print("PARTIAL DECRYPTION USING FREQUENCY-BASED MAPPING")
    print("=" * 70)
    print(decrypted[:800])
    if len(decrypted) > 800:
        print("...")
    
    #Munal Mapping (added this after manual analysis)
    print("\n" + "=" * 70)
    print("Manual substititon table (from manual analysis)")
    print("=" * 70)
    
    manual_mapping = {
        'A': 'U', 'B': None, 'C': 'V', 'D': None, 'E': 'P',
        'F': 'N', 'G': 'O', 'H': 'P', 'I': 'H', 'J': None,
        'K': 'R', 'L': 'S', 'M': 'Y', 'N': None, 'O': None,
        'P': None, 'Q': 'I', 'R': 'D', 'S': 'L', 'T': 'E',
        'U': 'G', 'V': None, 'W': 'B', 'X': 'A', 'Y': 'F',
        'Z': 'T'
    }
    
    print("\nCiphertext Letter -> Plaintext Letter:")
    for cipher_letter in sorted(manual_mapping.keys()):
        plain = manual_mapping[cipher_letter]
        if plain:
            print(f"      {cipher_letter}      ->        {plain}")
        else:
            print(f"      {cipher_letter}      ->        ?")
    
    #Apply manual mapping (only for letters I know)
    manual_decrypted = apply_substitution(ciphertext, {k: v for k, v in manual_mapping.items() if v is not None})
    
    print("\n" + "=" * 70)
    print("Decrypted Text Using Manual Mapping")
    print("=" * 70)
    print(manual_decrypted)

if __name__ == "__main__":
    main()
