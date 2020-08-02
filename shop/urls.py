#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include, handler404, handler500
from shop import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # -- Pour les produits

    url(r'^categorie/(?P<id>\d+)/$', views.categorie, name="categorie"),
    url(r'^categorie/(?P<id>\d+)/(?P<page>\d+)/$', views.categorie, name="categorie"),
    url(r'^categorie_mere/(?P<id>\d+)/$', views.categorie_mere, name="categorie_mere"),
    url(r'^categorie_mere/(?P<id>\d+)/(?P<page>\d+)/$', views.categorie_mere, name="categorie_mere"),
    url(r'^marque/(?P<id>\d+)/$', views.marque, name="marque"),
    url(r'^marque/(?P<id>\d+)/(?P<page>\d+)/$', views.marque, name="marque"),
    url(r'^detail-prod/(?P<id>\d+)/$', views.detailprod, name="detail-prod"),
    url(r'^image/(?P<id>\d+)/$', views.image, name="image"),
    url(r'^tout-prod/$', views.tou_prod, name="tou-prod"),
    url(r'^tout-prod/(?P<page>\d+)/$', views.tou_prod, name="tou-prod"),
    url(r'^reparation/$', views.reparation, name="reparation"),
    url(r'^categorie_marque/(?P<idm>\d+)/(?P<idc>\d+)/$', views.cat_marque, name="categorie-marque"),
    url(r'^categorie_marque/(?P<idm>\d+)/(?P<idc>\d+)/(?P<page>\d+)/$', views.cat_marque, name="categorie-marque"),
    url(r'^boutique/(?P<id>\d+)/$', views.boutique, name="boutique"),
    url(r'^boutique/(?P<id>\d+)/(?P<page>\d+)/$', views.boutique, name="boutique"),

    url(r'^mesmarque/$ ', views.mesmarque, name="mesmarque"),

    url(r'^add_in_cart/(?P<product_id>\d+)/(?P<qty>\d+)/$', views.ajouter_panier, name="ajouter_panier"),
    url(r'^produit-promo/$', views.produit_promo, name="produit-promo"),
    url(r'^produit-promo/(?P<page>\d+)/$', views.produit_promo, name="produit-promo"),
    url(r'^categorie_promo/(?P<id>\d+)/$', views.categorie_promo, name="categorie-promo"),
    url(r'^categorie_promo/(?P<id>\d+)/(?P<page>\d+)/$', views.categorie_promo, name="categorie-promo"),
    url(r'^recherche/$', views.recherche, name="recherche"),
    url(r'^recherche/(?P<page>\d+)/$', views.recherche, name="recherche"),

    url(r'^my_cart/$', views.my_cart, name="my_cart"),
    url(r'^add_in_cart/(?P<product_id>\d+)/(?P<qty>\d+)/$', views.panier, name="panier"),
    url(r'^vider_panier/$', views.supprime_panier, name="supprime_panier"),
    url(r'^supprime_produit/(?P<id>\d+)/(?P<quantity>\d+)$', views.supprime_produit, name="supprime_produit"),
    url(r'^modifie_produit/(?P<id>\d+)/(?P<quantity>\d+)$', views.modifie_produit, name="modifie_produit"),
    url(r'^abonner/(?P<idc>\d+)/(?P<idb>\d+)$', views.abonner, name="abonner"),
    url(r'^deabonner/(?P<idc>\d+)/(?P<idb>\d+)$', views.deabonner, name="deabonner"),
    url(r'^dernier_prod/(?P<idb>\d+)/$', views.dernier_prod, name="dernier_prod"),

    # -- Pour les utiliteurs

    # On import les vues de Django, avec un nom spécifique

    url(r'^vente/$', views.vente, name="vente"),
    url(r'^connexion/$', views.connexion, name="connexion"),
    url(r'^deconnexion$', auth_views.logout_then_login, name="deconnexion"),
    url(r'^inscription/$', views.inscription, name="inscription"),
    url(r'^inscription-vendeur/$', views.inscription_vendeur, name="inscription-vendeur"),
    url(r'^compte_vendeur/$', views.compte_vendeur, name="compte_vendeur"),
    url(r'^compte_client/$', views.compte_client, name="compte_client"),
    url(r'^compt-admin/$', views.compt_admin, name="compt-admin.html"),
    url(r'^confirm-achat/$', views.confirm_achat, name="confirmer-achat"),
    url(r'^detail_commande/(?P<id>\d+)/$', views.detail_commande, name="detail_commande"),
    url(r'^livrer/(?P<id>\d+)/$', views.livrer, name="livrer"),
    url(r'^mes_produit/(?P<i>\d+)/$', views.produit, name="produit"),
    url(r'^confirm_sup/(?P<i>\d+)/(?P<id>\d+)/$', views.confirm_sup, name="confirm_sup"),
    url(r'^supprimer_element/(?P<i>\d+)/(?P<id>\d+)/$', views.supprimer_element, name="supprimer_element"),
    url(r'^ajouter_produit/$', views.ajouter_produit, name="ajouter_produit"),
    url(r'^ajouter_produit/(?P<id>\d+)/$', views.ajouter_produit, name="ajouter_produit"),
    url(r'^ajouter_promos/$', views.ajouter_promos, name="ajouter_promos"),

    url(r'^ajouter_promos/(?P<id>\d+)/$', views.ajouter_promos, name="ajouter_promos"),
    url(r'^ajouter_marque/$', views.ajouter_marque, name="ajouter_marque"),
    url(r'^ajouter_categorie/$', views.ajouter_categorie, name="ajouter_categorie"),
    url(r'^ajouter_boutique/$', views.ajouter_boutique, name="ajouter_boutique"),
    # url(r'^address_shop/$', views.address_shop , name="address_shop"),

    # L 'emplacement d'un individus
    url(r'^pays/$', views.pays, name="pays"),
    url(r'^pays_region/(?P<id>\d+)/$', views.region, name="region"),
    url(r'^pays_region_localite/(?P<id>\d+)/$', views.localite, name="localite"),
    url(r'^pays_region_localite_address/(?P<id>\d+)/$', views.address, name="address"),

]
