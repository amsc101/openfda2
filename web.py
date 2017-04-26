#Copyright (C) Practica Ana Sollars & Co.

#Permission is granted to copy, distribute and/or modify this document
#under the terms of the GNU Free Documentation License, Version 1.3
#or any later version published by the Free Software Foundation;
#with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
#A copy of the license is included in the section entitled "GNU
#Free Documentation License"

#<Authors: Ana Mª Sollars Castellanos>

#lista de compañias
#compañia--> lista de drugs

import http.server
import json
import http.client

class OpenFDAClient():

    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"

    def get_event(self, limit): #--> conectado a ***
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit=" + limit)
        r1 = conn.getresponse()

        data1 = r1.read()
        data2 = data1.decode("utf8") #bytes a string
        event = data2
        return event

    def get_search(self, drug):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct='+drug+'&limit=10')
        r1 = conn.getresponse()

        data1 = r1.read()
        data2 = data1.decode("utf8")
        event = data2
        return event

    def get_company_drug(self, comp):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=companynumb='+comp+'&limit=10')
        r1 = conn.getresponse()

        data1 = r1.read()
        data2 = data1.decode("utf8")
        event = data2
        return event

class OpenFDAParser():

    def get_medicinalproduct(self,limit):
        client = OpenFDAClient()
        event = client.get_event(limit)
        event2= json.loads(event)
        results= event2["results"]

        for i in results:
            patient= i["patient"]
            drug= patient["drug"]
        med_list= []

        for i in range(int(limit)):
            patient= results[i]["patient"]
            medicinal= patient["drug"][0]["medicinalproduct"]
            med_list.append(medicinal)
        return med_list

    def get_company_list(self, limit):
        client= OpenFDAClient()
        event = client.get_event(limit)
        event2= json.loads(event)
        results= event2["results"]

        med_list= []
        for i in results:
            companynumb= i["companynumb"]
            med_list.append(companynumb)
        return med_list

    def parser_get_search(self,event):
        event2= json.loads(event)
        results= event2["results"]

        company_list= []
        for i in results:
            company= i["companynumb"]
            company_list.append(company)
        return company_list

    def get_gender_list(self, limit):
        client = OpenFDAClient()
        event = client.get_event(limit)
        event2= json.loads(event)
        results= event2["results"]

        sex_list=[]
        listGender=[]
        for i in results:
            patient = i["patient"]
            patient_sex= patient["patientsex"]
            sex_list.append(patient_sex)

        for i in sex_list:
            if i == "1":
                listGender.append("Female")
            elif i == "2":
                listGender.append("Male")
        return listGender

    def parser_get_company_drug(self,event):
        event2= json.loads(event)
        results= event2["results"]

        drug_list=[]
        for i in results:
            companynumb = i["companynumb"]
            patient=  i["patient"]
            medicinal= patient["drug"][0]["medicinalproduct"]
            drug_list.append(medicinal)
        return drug_list

class OpenFDAHTML():

    def get_main_page(self):
        html = """
            <html>
                <head>
                    <link rel="shortcut icon" href="https://b64459531885200b3efb-5206a7b3a50a3f5974248375cd863061.ssl.cf1.rackcdn.com/favicon-new.ico">
                    <title>OpenFDA Cool App</title>
                    <DIV ALIGN=center>
                    <IMG SRC="https://pbs.twimg.com/profile_images/701113332183371776/57JHEzt7.jpg" width="400" height="200" alt="correo">
                    </DIV>
                    <style type= "text/css">


                                    .button{
                        text-decoration: none;
                        padding: 3px;
                        padding-left: 10px;
                        padding-right: 10px;
                        font-family: Helvetica Neue;
                        font-weight: 300;
                        font-size: 15px;
                        font-style: bold;
                        color: blue;
                        background-color: #99CCFF;
                        border-radius: 15px;
                        border: 3px double blue;
                      }
                      .boton_1:hover{
                        opacity: 0.6;
                        text-decoration: none;
                      }
                    </style>
                </head>

                <body>
                    <DIV ALIGN=center>
                    <h1>
                    <FONT FACE="arial" SIZE=8 COLOR=><u>OpenFDA Client</u></FONT>
                    </h1>

                    <form method="get" action="listDrugs">
                        <input class="button" type="submit" value="Drug List: Send to OpenFDA">
                        </input>
                        limit:<input type="text" name="limit">
                        </input>
                    </form>

                    <form method="get" action="listCompanies">
                        <input class="button" type="submit" value="Company List: Send to OpenFDA">
                        </input>
                        limit:<input type="text" name="limit">
                        </input>
                    </form>

                    <form method="get" action="searchDrug">
                        <input type="text" name="drug">
                        <input class="button" type="submit" value="Drug Search: Send to OpenFDA">
                        </input>
                    </form>

                    <form method="get" action="searchCompany">
                        <input type="text" name="company">
                        <input class="button" type="submit" value="Company Search: Send to OpenFDA">
                        </input>
                    </form>

                    <form method="get" action="listGender">
                        <input type="text" name="limit">
                        <input class="button" type="submit" value="Gender">
                        </input>
                    </form>
                    </DIV>

                </body>
            </html>
            """
        return html

    def get_drug(self,drug):
        client = OpenFDAClient()
        parser = OpenFDAParser()
        event = client.get_search(drug)
        items= parser.parser_get_search(event)
        list = self.write_html(items)
        return list

    def get_second_page(self,limit):
        parser = OpenFDAParser()
        items= parser.get_medicinalproduct(limit)
        list = self.write_html(items)
        return list

    def get_third_page(self,limit):
        parser = OpenFDAParser()
        items= parser.get_company_list(limit)
        list = self.write_html(items)
        return list

    def get_company_html(self,comp):
        client = OpenFDAClient()
        parser = OpenFDAParser()
        event= client.get_company_drug(comp)
        items= parser.parser_get_company_drug(event)
        list = self.write_html(items)
        return list

    def get_patient_sex(self,limit):
        parser = OpenFDAParser()
        items= parser.get_gender_list(limit)
        list= self.write_html(items)
        return list

    def get_error_page(self):
        list = """
            <html>
                <head>
                    <body>
                        <h1>Error 404</h1>
                    <body>
                </head>
                    <body>
                        Page not found
                    </body>
            </html>
        """
        return list

    def write_html(self,items):
        list = """
            <html>
                <head></head>
                <body>
                    <ol>
                        """
        for element in items:
            list += "<li>" +element+ "</li>"
        list += """
                    </ol>
                </body>
            </html>
        """
        return list


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """ class that manages the HTTP request from web clients """

    def execute(self,html):
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes(html, "utf8"))

    # GET
    def do_GET(self):

        # Write content as utf-8 data
        if self.path == "/":
            # Get main page
            HTML = OpenFDAHTML()
            self.send_response(200)
            html = HTML.get_main_page()
            self.execute(html)

        elif "/listDrugs?limit=" in self.path:
            HTML = OpenFDAHTML()
            self.send_response(200)
            web= self.path.split("=")
            limit= web[-1]
            html= HTML.get_second_page(limit)
            self.execute(html)

        elif "/listCompanies?limit=" in self.path:
            HTML = OpenFDAHTML()
            self.send_response(200)
            web= self.path.split("=")
            limit= web[-1]
            html= HTML.get_third_page(limit)
            self.execute(html)

        elif '/searchDrug?drug=' in self.path:
            HTML = OpenFDAHTML()
            self.send_response(200)
            web= self.path.split("=")
            drug= web[-1]
            html= HTML.get_drug(drug)
            self.execute(html)

        elif '/searchCompany?company=' in self.path:
            HTML = OpenFDAHTML()
            self.send_response(200)
            web= self.path.split("=")
            comp= web[-1]
            html= HTML.get_company_html(comp)
            self.execute(html)

        elif "/listGender?limit=" in self.path:
            HTML = OpenFDAHTML()
            self.send_response(200)
            web= self.path.split("=")
            limit= web[-1]
            html= HTML.get_patient_sex(limit)
            self.execute(html)

        elif "/secret" in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate','Basic realm="User Visible Realm"')
            self.end_headers()

        elif "/redirect" in self.path:
            self.send_response(302)
            self.send_header('Location', 'http://localhost:8000/')
            self.end_headers()

        else:
            HTML = OpenFDAHTML()
            self.send_response(404)
            html= HTML.get_error_page()
            self.execute(html)

        return
