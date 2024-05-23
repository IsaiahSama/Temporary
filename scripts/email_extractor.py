import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from json import dumps

from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

class EmailExtractor:
    def __init__(self):
        """
        Initializes the EmailExtractor class.

        This function sets the `creds` attribute to None and calls the `get_credentials` method to retrieve the user's credentials for accessing the Gmail API.

        Parameters:
            None

        Returns:
            None
        """
        self.creds: Credentials = self.get_credentials()
    
    def get_credentials(self) -> Credentials:
        """
        Retrieves the user's credentials for accessing the Gmail API.

        This function checks if the "credentials.json" file exists and raises an exception if it does not. It then checks if the "token.json" file exists and loads the credentials from it if it does. If the credentials are not available or expired, the user is prompted to log in and the new credentials are saved to the "token.json" file.

        Returns:
            Credentials: The user's credentials for accessing the Gmail API.

        Raises:
            Exception: If the "credentials.json" file is not found.
        """
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        if not os.path.exists("credentials.json"):
            raise Exception("credentials.json not found")

        creds: Credentials = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds
    
    def get_last_n_emails(self, n: int) -> list:
        """
        Retrieves the last `n` emails from the user's inbox.

        This function retrieves the `n` most recent emails from the user's inbox using the Gmail API. The `n` parameter specifies the number of emails to retrieve.

        Parameters:
            n (int): The number of emails to retrieve.

        Returns:
            list: A list of dictionaries containing information about the retrieved emails. Each dictionary contains the following keys:
                - `sender`: The email address of the sender.
                - `subject`: The subject of the email.
                - `body`: The body of the email.
                - `attachments`: The attachments on the email
        """

        service = build("gmail", "v1", credentials=self.creds)
        results = service.users().messages().list(userId="me", maxResults=n).execute()

        filtered = []

        for result in results["messages"]:
            msg = service.users().messages().get(userId="me", id=result["id"]).execute()

            payload = msg['payload']
            headers = payload['headers']

            body = payload['body']

            subject = [h['value'] for h in headers if h['name'] == 'Subject'][0]
            if "QB Checks" in subject:
                filtered.append(payload)
            
        chosen = filtered[0]
        attachments = [part for part in chosen['parts'] if part['mimeType'] == 'text/csv']
        print(dumps(attachments, indent=4))

        filenames = []

        for attachment in attachments:
            filename = '-'.join([word.strip() for word in attachment['filename'].split("-")]).split("-")
            temp = {
                "KEY": filename[0],
                "MODE": filename[1],
                "DATE": filename[2].split(".")[0]
            }      

            temp["DATE"] = datetime.strptime(temp['DATE'], "%Y%m%d").strftime("%d_%m_%Y")

            print(temp)

        print(filenames)
            # internal_date = datetime.fromtimestamp(int(msg['internalDate'])/1000)
            # print(subject, internal_date.strftime("%a, %d %b %Y %H:%M:%S"))

if __name__ == "__main__":
    extractor = EmailExtractor()
    extractor.get_last_n_emails(20)