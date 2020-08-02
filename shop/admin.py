from django.contrib import admin
from shop.models import *
from django.contrib.admin import AdminSite



titre = "Administrateur Cbshop"
admin.AdminSite.site_header = titre



admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Marque)
admin.site.register(Boutique)
admin.site.register(User)
admin.site.register(Userclient)
admin.site.register(Uservendeur)
# Register your models here.
admin.site.register(Panier)
admin.site.register(Commande_for_shop)
admin.site.register(Message_for_vendeur)
admin.site.register(CategorieMere)
admin.site.register(Commission)
admin.site.register(Abonnement)
admin.site.register(Pays)
admin.site.register(Region)
admin.site.register(Localite)
admin.site.register(Address)
admin.site.register(Promo)


