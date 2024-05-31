from scripts.email_extractor import EmailExtractor

# Extract last 4 emails
extractor = EmailExtractor(".")
extractor.get_last_n_emails(4)