from controller import GeneratorController
from scripts.email_extractor import EmailExtractor

# Extract last 4 emails
extractor = EmailExtractor(".")
first_date = extractor.get_last_n_emails(4)

companies = ["TIDES", "BISTRO", "CLIFF", "CAFE"]

# Generate reports
controller = GeneratorController()
for company in companies:
    controller.set_generator(company, first_date.strftime("%m/%d/%Y"))
    controller.generate_report()