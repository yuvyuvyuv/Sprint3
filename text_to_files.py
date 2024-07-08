def create_all_files(big_string):
    start_marker = "file_format:"
    output_file = "out"
    i = 0
    files = big_string.split(start_marker)
    for file_text in files:
        i += 1
        text_to_file(file_text,output_file+i)


def text_to_file(text_data,output_file):
    end_marker = "end"
    end_pos = text_data.find(end_marker)
    file_format = text_data[:end_pos]
    end_of_file = text_data.find("end_of_file")
    bytes_data = text_data[end_pos+1:end_of_file].encode('latin1')
    output_file_with_format = output_file+file_format
    with open(output_file_with_format, 'wb') as file:
        file.write(bytes_data)




