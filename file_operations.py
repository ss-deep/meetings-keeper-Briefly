from flask import Flask, send_file, request
import pdfkit
import os

app = Flask(__name__)

# Path to wkhtmltopdf binary if it's not in PATH
# path_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'  # Adjust the path as necessary
# config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

@app.route('/download_pdf')
def download_pdf():
    url = request.args.get('url', 'https://www.google.com/')
    output_path = 'output.pdf'
    
    # Generate PDF from the URL
    pdfkit.from_url(url, output_path)
    
    # Send the generated PDF as a file download
    return send_file(output_path, as_attachment=True, attachment_filename='downloaded.pdf')

if __name__ == '__main__':
    app.run(debug=True)
