import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import streamlit as st
import matplotlib.pyplot as plt
import scienceplots
from app_utils import get_matplotlib_ROC_plot, get_matplotlib_PC_plot
import os

class EmailSender:
    def __init__(self, smtp_server, smtp_port):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.__sender_email = "matheuscamposmattos@id.uff.br"
        self.__password = "jdehlcenifasfjmb"

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
                message.attach(image)

        text = message.as_string()
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.__sender_email, self.__password)
            server.sendmail(self.__sender_email, receiver_email, text)

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

    def save_matplotlib_as_images(self):
        plt.style.use('science')
        pc_fig, roc_fig = get_matplotlib_ROC_plot(), get_matplotlib_PC_plot()
        parent = f"{self.save_dir}/matplotlib"
        if not os.path.exists(parent):
            os.mkdir(parent)

        pc_fig.savefig(f"{parent}/pc.png", dpi=200)
        roc_fig.savefig(f"{parent}/roc.png", dpi=200)

        paths = [f"{parent}/pc.png", f"{parent}/roc.png"]

        return paths

    def download(self, figures):
        if len(figures) > 0:

            if self.engine == 'matplotlib':
                return self.save_matplotlib_as_images()
            
            elif self.engine == 'plotly':
                paths = []

                for fig in figures:
                    paths.append(self.save_plotly_figure_as_image(fig))

                return paths


            