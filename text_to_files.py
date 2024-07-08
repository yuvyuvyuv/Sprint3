def text_to_file(text_data, output_file):
    start_marker = "file_format:"
    end_marker = "end"
    
    # Find the start and end positions of the file format
    start_pos = text_data.find(start_marker) + len(start_marker)
    end_pos = text_data.find(end_marker, start_pos)
    
    # if start_pos != -1 and end_pos != -1:
    #     # Extract the file format
    file_format = text_data[start_pos:end_pos]
    
    bytes_data = text_data[end_pos+1:].encode('latin1')

    
