import os

dir_path = os.getcwd() + '/test'

while True:
    file_number = int(input('Enter a file number: '))

    file_list = []
    with os.scandir(dir_path) as it:
        for entry in it:
            file_list.append(entry.name)

    if file_number >= 0 and file_number < len(file_list):
        selected_file = file_list[file_number]
        print(selected_file)
    else:
        print('Invalid file number')

    choice = input("Do you want to select another file? (y/n) ")
    if choice.lower() == 'n':
        break
