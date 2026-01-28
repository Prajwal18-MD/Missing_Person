import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL")
    
    def send_match_alert(
        self,
        to_emails: List[str],
        missing_person_name: str,
        confidence_score: float,
        location: str,
        timestamp: str,
        matched_image_path: Optional[str] = None
    ) -> bool:
        """Send email alert when a match is found"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = f"ALERT: Possible sighting of {missing_person_name}"
            
            # Email body
            body = f"""
            MISSING PERSON ALERT
            
            A possible match has been found for: {missing_person_name}
            
            Details:
            - Confidence Score: {confidence_score:.2%}
            - Location: {location}
            - Time: {timestamp}
            
            Please verify this match as soon as possible.
            
            This is an automated alert from the Missing Person Detection System.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach matched image if available
            if matched_image_path and os.path.exists(matched_image_path):
                with open(matched_image_path, 'rb') as f:
                    img_data = f.read()
                    image = MIMEImage(img_data)
                    image.add_header('Content-Disposition', 'attachment', filename='matched_face.jpg')
                    msg.attach(image)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.from_email, to_emails, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_case_created_notification(
        self,
        to_email: str,
        missing_person_name: str,
        case_id: int
    ) -> bool:
        """Send notification when a new case is created"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = f"Missing Person Case Created: {missing_person_name}"
            
            body = f"""
            Missing Person Case Created
            
            A new missing person case has been created:
            
            Name: {missing_person_name}
            Case ID: {case_id}
            
            The system will now monitor for potential matches and send alerts if any are found.
            
            Thank you for using the Missing Person Detection System.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.from_email, [to_email], text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_person_found_notification(
        self,
        to_emails: List[str],
        missing_person_name: str,
        case_id: int
    ) -> bool:
        """Send notification when a person is marked as found"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = f"GOOD NEWS: {missing_person_name} has been found!"
            
            body = f"""
            MISSING PERSON FOUND
            
            Great news! {missing_person_name} has been marked as found.
            
            Case ID: {case_id}
            Status: Found
            
            The case has been closed and face matching has been disabled.
            
            Thank you for using the Missing Person Detection System.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.from_email, to_emails, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False