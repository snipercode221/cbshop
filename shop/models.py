#!/usr/local/bin/python
# -*- coding: utf-8 -*-


from django.db import models

# Les compte utilisateurs

from django.contrib.auth.models import User


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Pays(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Pays")

    def __str__(self):
        return self.nom


class Region(models.Model):
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100, verbose_name="Région")

    def __str__(self):
        return self.nom


class Localite(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100, verbose_name="Localité")

    def __str__(self):
        return self.nom


class Address(models.Model):
    localite = models.ForeignKey(Localite, on_delete=models.CASCADE)
    cite = models.CharField(max_length=100, verbose_name="Groupe de quatier , Cités")
    quartier = models.CharField(max_length=100, verbose_name="Quartier , Rue...")

    def __str__(self):
        return self.cite + " " + self.localite.nom + " à  " + self.quartier


class Userclient(User):  # La liaison OneToOne vers le modèle User
    signature = models.TextField(blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)


class Uservendeur(Userclient):
    numero = models.CharField(max_length=100)


class CategorieMere(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Boutique(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la boutique:")
    nom_abrj = models.CharField(max_length=100, verbose_name="Abréviation", null=True)

    # address = models.CharField(max_length=100 , verbose_name="Adresse")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    email_boutique = models.CharField(max_length=100, verbose_name="E-mail")
    numero_service = models.CharField(max_length=100, verbose_name="numéro service 1:")
    second_num_service = models.CharField(max_length=100, null=True, verbose_name="numéro service 2:")
    vendeur = models.ForeignKey(Uservendeur, on_delete=models.CASCADE, )
    type_de_vente = models.ForeignKey(CategorieMere, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom


# Les produits


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    categorie_mere = models.ForeignKey(CategorieMere, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom


class Marque(models.Model):
    nom = models.CharField(max_length=100)
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix_normal = models.FloatField(verbose_name="Prix normal du produit", default=0)
    prix = models.FloatField(verbose_name="Prix du produit")
    quantite = models.IntegerField(verbose_name="Quantite en stok")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    description = models.TextField()
    photo_img1 = models.ImageField(upload_to="photos/")
    photo_img2 = models.ImageField(upload_to="photos/")
    photo_img3 = models.ImageField(upload_to="photos/", null=True, blank=True)
    photo_img4 = models.ImageField(upload_to="photos/", null=True, blank=True)
    photo_img5 = models.ImageField(upload_to="photos/", null=True, blank=True)
    date_creat = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de création")

    def __str__(self):
        return self.nom


class Panier(models.Model):
    client = models.ForeignKey(Userclient, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    commander = models.BooleanField(default=False)

    def total(self):
        return float(self.produit.prix * float(self.quantite))

    def __str__(self):
        return str(self.quantite) + " " + self.produit.nom


class Commande_for_shop(models.Model):
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    numero_client = models.CharField(max_length=100)
    lieu_de_livraison = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de la commande")
    vue = models.BooleanField(default=False)
    Livre = models.BooleanField(default=False)

    def __str__(self):
        return "commande for shop " + self.boutique.nom


class Message_for_vendeur(models.Model):
    message = models.CharField(null=True, max_length=1000)


class Commission(models.Model):
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    prix = models.FloatField()

    def __str__(self):
        return "Commission de " + self.boutique.nom + "  __Numéro__  " + str(
            self.boutique.numero_service) + " / " + str(
            self.boutique.second_num_service) + " ------------------------>   Prix " + str(self.prix)


# Create your models here.

class Abonnement(models.Model):
    client = models.ForeignKey(Userclient, on_delete=models.CASCADE)
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)

    def __str__(self):
        return self.client.user.username + "  Vous etes abonner à  " + self.boutique.nom


class Promo(models.Model):
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, null=True)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    nouveau_prix = models.FloatField(verbose_name="Nouveau prix")
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Début de promo ")
    duree = models.IntegerField(verbose_name="Durée ( en jours ) ")
    date_fin = models.DateTimeField(auto_now_add=False, auto_now=False, verbose_name="fin promo", null=True)

    def __str__(self):
        return self.produit.nom


class pub(models.Model):
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, null=True)
    lien = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to="photos/", null=True, blank=True)

    def __str__(self):
        return self.description
