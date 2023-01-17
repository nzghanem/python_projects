from to_excel import excel
import yagmail


def sendto(receiver):
    yag = yagmail.SMTP("your email address", "your app password to your email")
    yag.send(
        to=receiver,
        subject="Going to Prague to study and here you have the thousand mails and one mail.",
        contents="""<h1>Dear Sir/Madam,</h1>
        
        <p style='font-family:Cavolini;font-size:30px;color:green'>Every part of this message including sending it was done with <strong>Python</strong>. 
        Excel file was scraped from the web using <strong>Python</strong>.Then, converted and formated into excel as you see it now all using <strong>Python</strong>.</p> 
        
        <p style='font-family:Cavolini;font-size:30px;font-style:italic;color:blue'>I need your help to choose the best specialization. 
        Initially, I would like to choose <strong>Software Engineering</strong> as it's better for the CV. What do you think?</p>
        
        <h3>Yours Sincerely,\nNezar Ghanem</h3>""",
        attachments="CTU FIT Bachelor Specializations.xlsx"
    )


create_file = excel()
sendto("to whom you are sending / it could be multiple persons if so use an array")
