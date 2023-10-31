import sys
import os


input_file = sys.argv[1]

def expand_accessions(entry):
    """
    Given an entry, expand it into multiple entries based on certain rules.
    @param entry - the entry to be expanded
    @return The expanded entries as a comma-separated string
    """

    parts = entry.split(',')
    expanded_entries = []
    
    for part in parts:
        part = part.replace(" ", "")
        if '-' in part:
            last_underscore_index = part.rfind('_')
            prefix = part[:last_underscore_index + 1]
            start = int(part.split('-')[0][len(prefix):])
            end = int(part.split('-')[-1])
            for i in range(start, end + 1):
                expanded_entries.append(f"{prefix}{i}")
        else:
            expanded_entries.append(part.strip())  # Remove leading/trailing spaces
    
    return ', '.join(expanded_entries)

try:
    with open(input_file, 'r') as file:
        text = file.read()

    expanded_text = expand_accessions(text).split(',')

    chunks = [expanded_text[i:i + 10000] for i in range(0, len(expanded_text), 10000)]

    # Get the base file name without the extension
    base_name, ext = os.path.splitext(input_file)

    # Create the 'data' directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    for i, chunk in enumerate(chunks, start=1):
        output_file = os.path.join('data', f"{base_name}_{i}{ext}")
        with open(output_file, 'w') as file:
            file.write(','.join(chunk))

except FileNotFoundError:
    print(f"{input_file} not found.")
except Exception as e:
    print(f"An error occurred: {e}")