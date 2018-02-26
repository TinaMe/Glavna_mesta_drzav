#!/usr/bin/env pyt

import os
import jinja2
import webapp2
import random


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)



class Drzava:
    def __init__(self, ime_drzave, glavno_mesto, slika):
        self.ime_drzave = ime_drzave
        self.glavno_mesto = glavno_mesto
        self.slika = slika


slovenija = Drzava(ime_drzave="Slovenija", glavno_mesto="Ljubljana", slika="/assets/images/1.jpg")
avstrija = Drzava(ime_drzave="Avstrija", glavno_mesto="Dunaj", slika="/assets/images/2.jpg")
nemcija = Drzava(ime_drzave="Nemcija", glavno_mesto="Berlin", slika="/assets/images/3.jpg")
italija = Drzava(ime_drzave="Italija", glavno_mesto="Rim", slika="/assets/images/4.jpg")
hrvaska = Drzava(ime_drzave="Hrvaska", glavno_mesto="Zagreb", slika="/assets/images/5.jpg")

drzave_seznam = [slovenija, avstrija, nemcija, italija, hrvaska]




class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))



class HomeHandler(BaseHandler):
    def get(self):

        cifra_drzave = random.randint(0, len(drzave_seznam) - 1)

        podatki = {"drzava": drzave_seznam[cifra_drzave].ime_drzave, "mesto": drzave_seznam[cifra_drzave].glavno_mesto, "slika": drzave_seznam[cifra_drzave].slika}
        return self.render_template("Home.html", podatki)


class ResultHandler(BaseHandler):
    def post(self):

        vpisano_mesto = self.request.get("mesto")
        dejanska_drzava = self.request.get("drzava")
        result = 0

        for item in drzave_seznam:
            if item.ime_drzave == dejanska_drzava:
                if item.glavno_mesto.lower() == vpisano_mesto.lower():
                    result = 1
                    break

        if result == 1:
            podatki = {"rezultat": "PRAVILEN!"}
        else:
            podatki = {"rezultat": "NEPRAVILEN!"}
        return self.render_template("Result.html", podatki)




app = webapp2.WSGIApplication([
    webapp2.Route('/', HomeHandler),
    webapp2.Route('/Result', ResultHandler),
], debug=True)