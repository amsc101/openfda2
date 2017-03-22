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

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"

    ###
    # GET EVENT
    ##
    def get_event(self): #--> conectado a ***
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10" )
        r1 = conn.getresponse()

        data1 = r1.read()
        data2 = data1.decode("utf8") #bytes a string
        event = data2

        return event

    def get_medicinalproduct(self):
        event = self.get_event()

        event2= json.loads(event)
        results= event2["results"]

        for i in results:
            patient= i["patient"]
            drug= patient["drug"]

        med_list= []
        for i in range(10):
            patient= results[i]["patient"]
            medicinal= patient["drug"][0]["medicinalproduct"]
            med_list.append(medicinal)

        return med_list

    def get_search(self, drug):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct='+drug+'&limit=10')
        r1 = conn.getresponse()

        data1 = r1.read()
        data2 = data1.decode("utf8")
        event = data2

        event2= json.loads(event)
        results= event2["results"]

        lyrica_list= []
        for i in results:
            lyrica= i["companynumb"]
            lyrica_list.append(lyrica)

        return lyrica_list

    def get_company_list(self):
        event = self.get_event()

        event2= json.loads(event)
        results= event2["results"]

        med_list= []
        for i in results:
            companynumb= i["companynumb"]
            med_list.append(companynumb)

        return med_list

    def get_company_drug(self, comp):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=companynumb='+comp+'&limit=10')
        r1 = conn.getresponse()

        data1 = r1.read()
        data2 = data1.decode("utf8")
        event = data2

        event2= json.loads(event)
        results= event2["results"]

        drug_list=[]
        for i in results:
            companynumb = i["companynumb"]
            patient=  i["patient"]
            medicinal= patient["drug"][0]["medicinalproduct"]
            drug_list.append(medicinal)

        return drug_list

    def get_main_page(self):
        html = """
            <html>
                <head>
                    <title>OpenFDA Cool App</title>
                </head>
                <body>
                    <h1>OpenFDA Client</h1>
                    <form method="get" action="receive">
                        <input type="submit" value="Enviar a OpenFDA">
                        </input>
                        </form>
                    <form method="get" action="receivecompany">
                        <input type="submit" value="Company Numb">
                        </input>
                        </form>
                    <form method="get" action="search">
                        <input type="text" name="drug">
                        <input type="submit" value="Drug Search LYRICA: Send to OpenFDA">
                        </input>
                    </form>
                    <form method="get" action="searchcompany">
                        <input type="text" name="comp">
                        <input type="submit" value="Drug Search Company: Send to OpenFDA">
                        </input>
                    </form>

                </body>
            </html>
            """
        return html

    def get_lyrica(self,drug):
        items= self.get_search(drug)
        list = """
            <html>
                <head></head>
                    <body>
                        <ul>
                            """
        for drug in items:
            list += "<li>" +drug+ "</li>"
        list += """
                    </ul>
                </body>
                </html>
            """
        return list

    def get_second_page(self):
        items= self.get_medicinalproduct()
        list = """
            <html>
                <head></head>
                <body>
                    <ul>
                        """
        for drug in items:
            list += "<li>" +drug+ "</li>"
        list += """
                    </ul>
            </body>
            </html>
        """
        return list

    def get_third_page(self):
        items= self.get_company_list()
        list = """
            <html>
                <head></head>
                <body>
                    <ul>
                        """
        for drug in items:
            list += "<li>" +drug+ "</li>"
        list += """
                    </ul>
            </body>
            </html>
        """
        return list

    def get_company_html(self,comp):
        items= self.get_company_drug(comp)
        list = """
            <html>
                <head></head>
                <body>
                    <ul>
                        """
        for drug in items:
            list += "<li>" +drug+ "</li>"
        list += """
                    </ul>
            </body>
            </html>
        """
        return list


    # GET
    def do_GET(self):

        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Write content as utf-8 data
        if self.path == "/":
            # Get main page
            html = self.get_main_page()
            self.wfile.write(bytes(html, "utf8"))

        elif self.path == "/search?":
            html= self.get_lyrica()
            self.wfile.write(bytes(html, "utf8"))

        elif self.path == "/receive?":
            html= self.get_second_page()
            self.wfile.write(bytes(html, "utf8"))

        elif self.path == "/receivecompany?":
            html= self.get_third_page()
            self.wfile.write(bytes(html, "utf8"))

        elif '/search?' in self.path:
            web= self.path.split("=")
            drug= web[-1]
            html= self.get_lyrica(drug)
            self.wfile.write(bytes(html, "utf8"))

        elif '/searchcompany?' in self.path:
            web= self.path.split("=")
            comp= web[-1]
            html= self.get_company_html(comp)
            self.wfile.write(bytes(html, "utf8")) #se puede sacar y eliminar los otros repetidos



        return

        ###
