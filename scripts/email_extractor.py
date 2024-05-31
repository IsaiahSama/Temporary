import base64
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from json import dumps
from datetime import datetime

try:
    from .utils.enums import RestaurantNames
except ImportError:
    from utils.enums import RestaurantNames

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

class EmailExtractor:
    def __init__(self, root:str=".."):
        """
        Initializes the EmailExtractor class.

        This function sets the `creds` attribute to None and calls the `get_credentials` method to retrieve the user's credentials for accessing the Gmail API.

        Parameters:
            None

        Returns:
            None
        """
        self.root = root
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

        if not os.path.exists(f"{self.root}/credentials.json"):
            raise Exception("credentials.json not found")

        creds: Credentials = None
        if os.path.exists(f"{self.root}/token.json"):
            creds = Credentials.from_authorized_user_file(f"{self.root}/token.json", SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f"{self.root}/credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(f"{self.root}/token.json", "w") as token:
                token.write(creds.to_json())

        return creds
    
    def get_last_n_emails(self, n: int) -> datetime:
        """
        Retrieves the last `n` emails from the user's inbox.

        This function retrieves the `n` most recent emails from the user's inbox
        using the Gmail API. The `n` parameter specifies the number of emails to
        retrieve.

        Args:
            n (int): The number of emails to retrieve.

        Returns:
            datetime: The date of the first email retrieved.
        """

        service = build("gmail", "v1", credentials=self.creds)
        results = service.users().messages().list(userId="me", maxResults=n).execute()

        filtered = []

        for result in results["messages"]:
            msg = service.users().messages().get(userId="me", id=result["id"]).execute()

            payload = msg['payload']
            headers = payload['headers']

            subject = [h['value'] for h in headers if h['name'] == 'Subject'][0]
            if "QB Checks" in subject:
                payload['messageID'] = result['id']
                filtered.append(payload)
            
        first_date = None
        for payload in filtered:
            attachments = [part for part in payload['parts'] if part['mimeType'] == 'text/csv']

            for attachment in attachments:
                filename = '-'.join([word.strip() for word in attachment['filename'].split("-")])
                split_filename = filename.split("-")
                file_info = {
                    "KEY": split_filename[0],
                    "MODE": split_filename[1],
                    "DATE": split_filename[2].split(".")[0],
                    "ID": attachment['body']['attachmentId'],
                    "filename": filename,
                    "messageID": payload['messageID']
                }      

                file_info["DATE"] = datetime.strptime(file_info['DATE'], "%Y%m%d").strftime("%d_%m_%Y")
                if first_date is None: 
                    first_date = datetime.strptime(file_info['DATE'], "%d_%m_%Y")

                file_id = file_info['ID']

                file = service.users().messages().attachments().get(userId="me", messageId=file_info['messageID'], id=file_id).execute()
                
                stored_filename = f"{self.root}/documents/Upload/{RestaurantNames.get_restaurant_by_abrv(file_info['KEY']).value[0].replace(' ', '_')}/{file_info['filename']}"
                with open(stored_filename, "wb") as f:
                    f.write(base64.urlsafe_b64decode(file['data'].encode('utf-8')))
                    print("Downloaded " + stored_filename)
            
        return first_date

if __name__ == "__main__":
    extractor = EmailExtractor()
    extractor.get_last_n_emails(30)