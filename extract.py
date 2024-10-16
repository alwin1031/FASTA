import pandas as pd
import requests
import time

# Read the access codes from the CSV file
data = pd.read_csv('list.csv', header=None)
access_codes = data[0].tolist()

# Open 'whole.txt' for writing all sequences
with open('whole.txt', 'w') as whole_file:
    for code in access_codes:
        url = f'https://rest.uniprot.org/uniprotkb/{code}.fasta'
        response = requests.get(url)
        
        if response.status_code == 200:
            fasta_sequence = response.text
            lines = fasta_sequence.strip().split('\n')
            header = lines[0]
            
            # Extract the words between 'OS=' and 'OX='
            os_index = header.find('OS=')
            ox_index = header.find('OX=')
            
            if os_index != -1 and ox_index != -1:
                new_header_content = header[os_index+3 : ox_index].strip()
                new_header = f'>{new_header_content}'
            else:
                new_header = header  # Keep original header if tags not found
            
            # Reconstruct the FASTA sequence with the new header
            sequence = '\n'.join(lines[1:])
            modified_sequence = f'{new_header}\n{sequence}'
            
            # Append to 'whole.txt'
            whole_file.write(modified_sequence + '\n')
            
            # Save to individual file named '[access code].txt'
            with open(f'{code}.txt', 'w') as individual_file:
                individual_file.write(modified_sequence)
        else:
            print(f'Failed to retrieve sequence for {code}')
        
        # Optional: Add delay to respect API rate limits
        time.sleep(0.5)
