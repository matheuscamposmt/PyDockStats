import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from smtplib import SMTPRecipientsRefused, SMTPConnectError
import streamlit as st
import matplotlib.pyplot as plt
import scienceplots
from utils.app_utils import get_plt_from_plotly
from components.charts import Chart
import os
import plotly.graph_objects as go

class EmailSender:
    def __init__(self, smtp_server, smtp_port):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.__sender_email = st.secrets['email']['address']
        self.__password = st.secrets['email']['password']

    def send_email_with_images(self, receiver_email, subject, image_paths: list):
        message = MIMEMultipart()
        message['From'] = self.__sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        message.attach(
            MIMEText("Here are the performance metric figures generated by PyDockStats.", 'plain')
        )

        for image_path in image_paths:
            with open(image_path, 'rb') as f:
                image = MIMEImage(f.read())
                image.add_header('Content-ID', f'<{image_path}>')
                image.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
                message.attach(image)

        text = message.as_string()

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.__sender_email, self.__password)
                server.sendmail(self.__sender_email, receiver_email, text)
                return dict(status="success", message="Email sent successfully")

        except SMTPRecipientsRefused:
            return dict(status="SMTPRecipientsRefused", message=f"The email address \"{receiver_email}\" is not valid")
        
        except SMTPConnectError:
            return dict(status="SMTPConnectError", message="Could not connect to the server")




class FigureDownloader:
    def __init__(self, save_dir, engine='plotly'):
        if engine not in ['plotly', 'matplotlib']:
            raise ValueError(f"Invalid engine '{engine}'")
            
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.mkdir(self.save_dir)
        self.engine = engine
        
    def save_plotly_figure_as_image(self, fig):
        parent = f"{self.save_dir}/plotly"

        if not os.path.exists(parent):
            os.mkdir(parent)

        path = f"{parent}/{fig.name}.png"
        fig.write_image(path)

        return path
    
    def save_fig(self, name, dir, fig: go.Figure):
        if not os.path.exists(dir):
            os.mkdir(dir)

        img_path = f"{dir}/{name}.png"

        paths_cache: dict = st.session_state['paths']
        if paths_cache.get(name):
            return img_path

        fig = get_plt_from_plotly(fig)
        fig.savefig(img_path, dpi=200)
        plt.close()

        st.session_state['paths'][name] = img_path

        return img_path

    
    def read_image(self, path):
        with open(path, 'rb') as f:
            return f.read()

    def download(self, curve: Chart):
        plotly_fig = curve.get_figure()

        if self.engine == 'matplotlib':
            parent = f"{self.save_dir}/{self.engine}"

            return self.save_fig(curve.name, parent, plotly_fig)
        
        elif self.engine == 'plotly':
            return self.save_plotly_figure_as_image(plotly_fig)


            