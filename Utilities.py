import os

blacklist = [
    "",
]

def write_strings_to_file(file_name, strings):
    try:
        directory = os.path.join(os.getcwd(), "")
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'w') as file:
            for string in strings:
                file.write(f"{string}\n")
        print(f"Strings written to {file_name} in directory successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def append_strings_to_file(file_name, string):
    try:
        directory = os.path.join(os.getcwd(), "")
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'a') as file:
               file.write(f"{string}\n")
        print(f"Strings appended to {file_name} in directory successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def append_string_to_file(file_name, string):
    try:
        directory = os.path.join(os.getcwd(), "")  # Current working directory
        os.makedirs(directory, exist_ok=True)  # Create directory if it doesn't exist
        file_path = os.path.join(directory, file_name)  # Create the complete file path
        with open(file_path, 'a', encoding='utf-8') as file:  # Open file in append mode with 'utf-8' encoding
            file.write(f"{string}\n")  # Write the string to the file
        print(f"String appended to {file_name} in directory successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Remove newline characters and leading/trailing whitespace from each line
            cleaned_lines = [line.strip() for line in lines]
            return cleaned_lines
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []

def remove_first_n_elements(lst, n):
    if n >= len(lst):
        return []  # If n is greater than or equal to the length of the list, return an empty list
    else:
        return lst[n:]

# sorted name asc
def get_files_in_directory(directory_path):
    try:
        # Check if the directory exists
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            # Get a list of all files in the directory and sort them by name in ascending order
            files = sorted([f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))])
            return files
        else:
            print("Directory does not exist or is not a valid directory path.")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def remove_duplicates(input_list):
    # Use a set to keep track of unique elements
    unique_elements = set()
    result_list = []

    # Iterate through the input list
    for item in input_list:
        # If the item is not in the set, add it to both the set and result list
        if item not in unique_elements:
            unique_elements.add(item)
            result_list.append(item)

    return result_list