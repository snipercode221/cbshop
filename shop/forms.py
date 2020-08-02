from django import forms
from .models import *


class Quantite(forms.Form):
    quantite = forms.IntegerField()


# -- Formulaire pour les produits
class ConnexionForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        exclude = ('prix_normal',)


# -- Formulaire pour les Marques
class MarqueForm(forms.ModelForm):
    class Meta:
        model = Marque
        fields = '__all__'


# -- Formulaire pour les Catgories

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = '__all__'


# -- Formulaire pour Boutiques

class BoutiqueForm(forms.ModelForm):
    class Meta:
        model = Boutique
        exclude = ('vendeur', 'address',)


class CommandeForm(forms.Form):
    numero = forms.CharField(max_length=100)
    default_address = forms.BooleanField(label="Utiliser mon adresse par défaut", required=False)

    # default_address = forms.BooleanField(default=False)


class InscriptionForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nom d'utilisateur", required=True)
    email = forms.EmailField(label="Votre address Email", required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe", required=True)


class VendeurForm(InscriptionForm):
    numero = forms.CharField(max_length=100, required=True, label="Tel ")


class PaysForm(forms.Form):
    pays = forms.ModelChoiceField(queryset=Pays.objects.all(), label="Pays ")


class LocaliteForm(forms.Form):
    localite = forms.ModelChoiceField(queryset=Localite.objects.all(), label="Localité ou Département ")


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('localite',)
