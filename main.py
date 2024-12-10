from Server import Server
import read
from datetime import datetime


pdf_path = "./payslip_09122024.PDF"
pay_data = read.extract_payslip_data(pdf_path)
date = pay_data["Pay Date"]
date = datetime.strptime(date, "%Y-%m-%d")
company = "RFDS"
gross = pay_data["Gross Pay"]
tax = pay_data["Tax Taken"]
net = pay_data["Net Pay"]
print(date, company, gross, tax, net)


query_insertPay = f"INSERT INTO payslips (date, gross, tax, net) VALUES ({date}, {gross}, {tax}, {net});"


print(date)

server = Server()
server.connect()
server.execute("SELECT * FROM payslips;")
server.print_fetch()
server.disconnect()
