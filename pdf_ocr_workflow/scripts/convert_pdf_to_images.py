"""Converts uploaded PDF to images. | Inputs: pdf_file | Outputs: images_data, pdf_name"""
"""Converts uploaded PDF to images. | Inputs: pdf_file | Outputs: images_data, pdf_name"""

def convert_pdf(pdf_input):
    import pypdfium2 as pdfium
    import io
    import os

    def get_file_path(data):
        path = None
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
        
        if isinstance(data, dict):
            path = data.get('file_path') or data.get('path')
        else:
            try:
                path = getattr(data, 'file_path', None) or getattr(data, 'path', None)
            except Exception:
                pass
        return path

    file_path = get_file_path(pdf_input)
    pdf_name = os.path.basename(file_path) if file_path else "document.pdf"
    images_data = []

    if file_path:
        pdf = pdfium.PdfDocument(file_path)
        for i in range(len(pdf)):
            page = pdf[i]
            bitmap = page.render()
            pil_image = bitmap.to_pil()
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format='PNG')
            images_data.append(img_byte_arr.getvalue())
            
    return images_data, pdf_name

# Main block: Variables defined here are GLOBAL and VISIBLE in UI
images_data, pdf_name = convert_pdf(pdf_file)
