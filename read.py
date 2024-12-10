import pdfplumber
from datetime import datetime

# Path to your PDF file
pdf_path = "./PY0001792072289.PDF"


def extract_payslip_data(pdf_path):
    data = {}
    with pdfplumber.open(pdf_path) as pdf:
        # Assuming the data is in the first page
        first_page = pdf.pages[0]
        text = first_page.extract_text()

        # Parsing logic
        lines = text.split("\n")
        for line in lines:
            if "Pay Date:" in line:
                pay_date_str = line.split(":")[1].strip()
                pay_date_dt = datetime.strptime(pay_date_str, "%d %b %Y")
                data["Pay Date"] = pay_date_dt.strftime("%Y-%m-%d")
            if "GROSS" in line:
                gross_line = line
                data["Gross Pay"] = gross_line.split()[1].strip()
            if "TAX" in line and "TOTAL PAY" not in line:  # Avoids the TOTAL PAY line
                tax_line = line
                data["Tax Taken"] = tax_line.split()[1].strip()
            if "NETT" in line:
                nett_line = line
                data["Net Pay"] = nett_line.split()[-4].strip()

    return data


if __name__ == "__main__":
    # Extract data from the payslip
    payslip_data = extract_payslip_data(pdf_path)
    for key, value in payslip_data.items():
        print(f"{key}: {value}")
