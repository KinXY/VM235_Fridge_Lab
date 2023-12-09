"""
script for processing experimental data of VM235 Fridge Lab
"""

def readData():
    filename = 'data.lvm'
    data_dict = {}
    with open(filename, 'r') as file:
        # Read the header line and split the keys by tabs
        headers = file.readline().strip().split('\t')
        
        # Initialize a list for each header in the dictionary
        for header in headers:
            data_dict[header] = []
        
        # Iterate over each data line in the file
        for line in file:
            # Split the values by tabs
            values = line.strip().split('\t')
            
            # Iterate over each header and corresponding value
            for header, value in zip(headers, values):
                # If the value is missing or empty, use 0, otherwise convert string to the appropriate type (assuming all numeric values)
                formatted_value = 0 if value == '' else float(value)
                
                # Append the value to the correct list in the dictionary
                data_dict[header].append(formatted_value)
            
            # If there are missing values at the end of the line, add zeroes for them
            for i in range(len(values), len(headers)):
                data_dict[headers[i]].append(0)
    return data_dict

def get_average_data(data_dict):
    average_data_dict = {}
    # choose a random time period from the data
    for key in data_dict:
        data_len = len(data_dict[key])
        break
    start_index = 100
    end_index = 300

    for key in data_dict:
        values = data_dict[key][start_index:end_index]
        sum = 0
        legal_len = 0
        for value in values:
            if value != 0:
                sum += value
                legal_len += 1
        if legal_len != 0:
            average_data_dict[key] = sum / legal_len
        else:
            average_data_dict[key] = 0
    
    return average_data_dict

if __name__ == '__main__':
    data_dict = readData()
    result = get_average_data(data_dict)
    # output the result to a file
    with open('result.txt', 'w') as file:
        for key in result:
            file.write(key + ': ' + str(result[key]) + '\n')
