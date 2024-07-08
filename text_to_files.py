def file_to_barcodes(file_path, file_number):
    file_path = os.path.join(DIR_PATH, file_path)
    file_format = os.path.splitext(file_path)[1]
    with open(file_path, 'rb') as file:
        text = file.read()
        text = text.decode('latin1')
        # split text into chunks of 100 characters

        chunks = []
        chunk_size = 100
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            chunks.append(chunk)

        # generate QR codes for each chunk
        qr_codes = []
        start_file = "file_format:"+file_format+"end"
        start_barcode = generate_qr_code_from_text(start_file, f"start_barcode{file_number}.png")
        qr_codes.append(start_barcode)
        for i, chunk in enumerate(chunks):
            output_file = f"qr_code_{file_number}_{i}.png"
            image_path = generate_qr_code_from_text(chunk, output_file)
            # convert data type to png
            qr_codes.append(image_path)
        end_barcode = generate_qr_code_from_text("end_of_file", f"end_barcode{file_number}.png")
        qr_codes.append(end_barcode)
        return qr_codes