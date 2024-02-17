import os

def change(folder_path):
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  # Check if the file is a text file
            file_path = os.path.join(folder_path, filename)

            # Read the content of the file
            with open(file_path, 'r') as file:
                content = file.read()
                
      
            # Replace the first number with 0
            content = content.replace(content.split()[0], '0', 1)

            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.write(content)
          

change('test/labels')
change('train/labels')
change('valid/labels')