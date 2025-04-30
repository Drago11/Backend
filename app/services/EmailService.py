from .WaitlistService import render_template
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


async def send_email(
        subject:str, 
        recepient:str, 
        template:str,
        template_context:dict,
):
   message = MessageSchema(
      subject=subject,
      recipients=[recepient],  # List of recipients, as many as you can pass
   )