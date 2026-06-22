# Letter Frequency Analysis for Substitution Cipher Cryptanalysis

A Python tool that performs statistical analysis on ciphertext to break classical substitution ciphers using letter frequency analysis.

## Overview

This program performs cryptanalysis on substitution ciphertext by:
- Counting letter frequencies in the ciphertext
- Comparing frequencies with standard English letter frequencies
- Generating frequency tables and bar chart visualizations
- Performing bigram analysis for pattern recognition
- Suggesting initial substitution mappings
- Allowing manual refinement of the substitution table

## Features

- **Frequency Analysis**: Counts and displays letter frequencies with comparison to English
- **Bigram Analysis**: Identifies common letter pairs in the ciphertext
- **Visualization**: Generates matplotlib bar charts for frequency distribution
- **Automated Mapping**: Suggests initial substitution based on frequency ranking
- **Manual Refinement**: Allows user-driven refinement of the substitution table

## Technologies Used

- Python 3
- Matplotlib
- Collections (Counter)

## Usage

```bash
python lfa.py intercepted_message.txt
