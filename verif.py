# -*- coding: utf8 -*-
from lxml import html
import urllib2, urllib

class Entreprise(object):

    raison_sociale = None
    fiche = None
    ville = None
    code_postal = None
    adresse = None
    siren = None
    siret = None
    ape_naf = None
    
    def __init__(self, raison_sociale, fiche, ville, code_postal, adresse, siren, siret, ape_naf):
        self.raison_sociale = raison_sociale
        self.fiche = fiche
        self.ville = ville
        self.code_postal = code_postal
        self.adresse = adresse
        self.siren = siren
        self.siret = siret
        self.ape_naf = ape_naf
    
    
    def __str__(self):
        return self.raison_sociale
    
class Verif(object):
    base_url = "http://www.verif.com/"
    cherche_url = base_url + "recherche/?search=v/1/ca/d"
    fiche_url = base_url + "societe/"
    
    def _get_fiche(self, siren):
        data = {'i_siren':siren}
        data_encode = urllib.urlencode(data)
        requete = urllib2.Request(self.cherche_url)
        requete.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=ISO-8859-1')
        requete.add_data(data_encode)
        page = (urllib2.urlopen(requete).read())
        document = html.fromstring(page)
        fiche = document.xpath("//div[@id='fiche_entreprise']")[0]
        return fiche
    
    
    def get_entreprise(self, siren):
        fiche = self._get_fiche(siren)
        # Verifier si entreprise radiée
        radiee = fiche.xpath("//p[@class='radiee']/text()")
        if len(radiee) == 0:
            # Raison sociale
            raison_sociale = fiche.xpath("//td[contains(text(), 'Raison sociale')]")[0].getnext().xpath("text()")[0]
            # Adresse
            adresse = fiche.xpath("//span[@itemprop='streetAddress']/text()")[0]
            # Code postal
            code_postal = fiche.xpath("//span[@itemprop='postalCode']/text()")[0]
            # Ville
            ville = fiche.xpath("//span[@itemprop='addressLocality']/text()")[0]
            # Code APE
            ape = fiche.xpath("//span[@id='verif_fiche.code.naf']/text()")[0][:-2]
            # SIRET
            siret = fiche.xpath("//td[contains(text(), 'SIRET')]")[0].getnext().xpath("text()")[0]
            # Lien de la fiche
            id_fiche = fiche.xpath("//div[@class='nav-tabs']/a[1]/@href")[0].split('/')[-2]
            lien_fiche =  self.fiche_url + id_fiche
            
            return Entreprise(raison_sociale, lien_fiche, ville, code_postal, adresse, siren, siret, ape)