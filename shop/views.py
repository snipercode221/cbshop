#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
# from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import datetime
from datetime import datetime, timedelta

from django.db.models import Q
from .models import *
from .forms import *

from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage


# def handler404(request):
#     return render(request, "erreur/404.html", {}, status=404)

def handler404(request, exception):
    return render(request, "erreur/404.html")


def handler500(request):
    return render(request, "erreur/500.html", {}, status=404)


# -- View pour les produits

def nombre_prod(request):
    nombre_p = 0
    if not request.user.is_authenticated():
        if 'cart' in request.session:
            cart = list()
            for product_id, quantity in request.session.get('cart').items():
                nombre_p += 1

    else:
        client = Userclient.objects.get(user_id=request.user.id)
        cart = Panier.objects.filter(client_id=client.id, commander=False)
        for cart_line in cart:
            nombre_p += 1
    return nombre_p


def accueil(request):
    nombre_p = nombre_prod(request)
    user = request.user
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    categorie1 = Categorie.objects.filter(categorie_mere=CategorieMere.objects.filter(id=1))
    boutique1 = Boutique.objects.filter(type_de_vente=CategorieMere.objects.filter(id=1))
    categorie2 = Categorie.objects.filter(categorie_mere=CategorieMere.objects.filter(id=2))
    boutique2 = Boutique.objects.filter(type_de_vente=CategorieMere.objects.filter(id=2))
    categorie3 = Categorie.objects.filter(categorie_mere=CategorieMere.objects.filter(id=3))
    boutique3 = Boutique.objects.filter(type_de_vente=CategorieMere.objects.filter(id=3))
    categorie4 = Categorie.objects.filter(categorie_mere=CategorieMere.objects.filter(id=4))
    boutique4 = Boutique.objects.filter(type_de_vente=CategorieMere.objects.filter(id=4))
    categorie5 = Categorie.objects.filter(categorie_mere=CategorieMere.objects.filter(id=5))
    boutique5 = Boutique.objects.filter(type_de_vente=CategorieMere.objects.filter(id=5))
    boutique_m = Boutique.objects.filter(type_de_vente=CategorieMere.objects.filter(id=6))

    promoss = Promo.objects.all().order_by('-date')
    today = datetime.now().day
    for prom in promoss:
        if (prom.date_fin.day <= today):
            for produit in Produit.objects.all():
                if prom.produit == produit:
                    produit.prix = produit.prix_normal
                    produit.produit_normal = 0
                    produit.save()
                    prom.delete()

    paginator = Paginator(promoss, 28)
    promos = paginator.page(1)

    if request.user.is_authenticated:
        client = Userclient.objects.filter(user=request.user)
        abonners = Abonnement.objects.filter(client=client)
    return render(request, "produit/accueil.html", locals())


def categorie(request, id, page=1):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    nombre_p = nombre_prod(request)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    categorie = get_object_or_404(Categorie, id=id)
    produits = Produit.objects.filter(categorie=categorie).order_by('-date_creat')

    paginator = Paginator(produits, 40)

    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
        minis = paginator.page(page)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        minis = paginator.page(paginator.num_pages)
    return render(request, "produit/categorie.html", locals())


def categorie_mere(request, id, page=1):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    nombre_p = nombre_prod(request)
    marques = Marque.objects.all()
    categoriem = CategorieMere.objects.get(id=id)
    categories = Categorie.objects.filter(categorie_mere=categoriem)
    produits = Produit.objects.filter(categorie__categorie_mere=categoriem).order_by('-date_creat')

    paginator = Paginator(produits, 40)  # 5 liens par page

    try:
        minis = paginator.page(page)
    except EmptyPage:
        minis = paginator.page(paginator.num_pages)

    return render(request, "produit/categorie_mere.html", locals())


def marque(request, id, page=1):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    nombre_p = nombre_prod(request)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    marque = get_object_or_404(Marque, id=id)
    produits = Produit.objects.filter(marque=marque).order_by('-date_creat')

    paginator = Paginator(produits, 40)

    try:

        minis = paginator.page(page)
    except EmptyPage:

        minis = paginator.page(paginator.num_pages)
    return render(request, "produit/marque.html", locals())


def cat_marque(request, idm, idc, page=1):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    nombre_p = nombre_prod(request)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    marque = get_object_or_404(Marque, id=idm)
    categorie = get_object_or_404(Categorie, id=idc)
    produits = Produit.objects.filter(Q(marque=marque), Q(categorie=categorie)).order_by('-date_creat')

    paginator = Paginator(produits, 40)  # 5 liens par page

    try:

        minis = paginator.page(page)
    except EmptyPage:

        minis = paginator.page(paginator.num_pages)
    return render(request, "produit/categorie-marque.html", locals())


def tou_prod(request, page=1):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    nombre_p = nombre_prod(request)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    produits = Produit.objects.all().order_by('-date_creat')

    paginator = Paginator(produits, 40)

    try:

        minis = paginator.page(page)
    except EmptyPage:

        minis = paginator.page(paginator.num_pages)

    return render(request, "produit/tou-prod.html", locals())


def detailprod(request, id):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    page = 1
    nombre_p = nombre_prod(request)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    produit = get_object_or_404(Produit, id=id)
    produits = Produit.objects.filter(categorie=produit.categorie).order_by('-date_creat')

    paginator = Paginator(produits, 16)

    try:

        minis = paginator.page(page)
    except EmptyPage:

        minis = paginator.page(paginator.num_pages)

    form = Quantite(request.POST or None)

    if form.is_valid():
        quantite = form.cleaned_data['quantite']
        if (int(quantite) < 1):
            return redirect(request.META.get('HTTP_REFERER'))

        mis_panier = True
        return redirect(ajouter_panier, product_id=id, qty=quantite)

    return render(request, "produit/detail-prod.html", locals())


def image(request, id):
    produit = get_object_or_404(Produit, id=id)
    return render(request, "produit/image.html", locals())


def reparation(request):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    nombre_p = nombre_prod(request)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    return render(request, "produit/reparation.html", locals())


def boutique(request, id, page=1):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    nombre_p = nombre_prod(request)
    if request.user.is_authenticated:
        client = Userclient.objects.get(user=request.user)

    boutique = Boutique.objects.get(id=id)
    marques = Marque.objects.filter(boutique=boutique)
    categories = Categorie.objects.filter(boutique=boutique)

    produits = Produit.objects.filter(boutique=boutique).order_by('-date_creat')

    paginator = Paginator(produits, 40)
    try:

        minis = paginator.page(page)
    except EmptyPage:

        minis = paginator.page(paginator.num_pages)

    return render(request, "produit/boutique.html", locals())


# Fonction de recherche avec postgres SQL

from django.contrib.postgres.operations import TrigramExtension
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.operations import UnaccentExtension, TrigramExtension
from django.db.models.functions import Lower
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


def recherche(request, page=1):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    nombre_p = nombre_prod(request)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    produits = Produit.objects.all().order_by('-date_creat')

    query = request.GET['q']

    if (query == ""):

        paginator = Paginator(produits, 40)  # 5 liens par page
        try:
            minis = paginator.page(page)
        except EmptyPage:
            minis = paginator.page(paginator.num_pages)

        return render(request, "produit/tou-prod.html", locals())
    else:

        vector = SearchVector('nom', 'categorie__nom', 'marque__nom')
        quer = SearchQuery(query)
        produit_trouver = Produit.objects.annotate(rank=SearchRank(vector, quer)).order_by('-rank')
        paginator = Paginator(produit_trouver, 40)  # 5 liens par page

        try:

            minis = paginator.page(page)
        except EmptyPage:
            minis = paginator.page(paginator.num_pages)

        return render(request, "produit/recherche.html", locals())


#######################################################################################
#######################################################################################
#############     ************************************************        #############
#############           PANIER POUR CLIENT CONNECTER OU NON               #############
#############     ************************************************        #############
#######################################################################################
#######################################################################################


def __move_session_cart_to_database_cart(request, client):
    """
    Cette fonction permet de copier le panier stocké en session d'un utilisateur non identifé vers la base de données
    juste avant son identification et supprime ensuite le panier stocké en session.
    :param request: l'objet request transmis depuis la fonction parent pour accéder à la session courante
    :param client_id: l'id du client
    :return:
    """
    if 'cart' in request.session:
        for product_id, qty in request.session['cart'].items():
            produit = Produit.objects.get(id=product_id)
            if Panier.objects.filter(Q(produit=produit), Q(client=client), Q(commander=False)).exists():

                cart_line = Panier.objects.get(Q(produit=produit), Q(client=client), Q(commander=False))
                cart_line.quantite += int(qty)
            else:
                cart_line = Panier(client=client, produit=produit, quantite=qty)
            cart_line.save()
        del request.session['cart']
    return


def ajouter_panier(request, product_id, qty):
    nombre_p = nombre_prod(request)
    """
    Cette fonction permet d'ajouter un produit au panier. Si l'utilisateur n'est pas connecté, le produit est ajouté
    dans un panier virtuel géré grâce au système de sessions ; sinon, il est persisté en BDD.
    :type request:
    :param request:
    :param product_id: Id du produit à ajouter au panier
    :param qty: Nombre d'exemplaire du produit à ajouter au panier
    :return:
    """

    if not request.user.is_authenticated():
        if 'cart' not in request.session:
            cart = dict()
        else:
            cart = request.session['cart']

        if product_id in cart:
            cart[product_id] = int(cart[product_id]) + int(qty)
        else:
            cart[product_id] = qty

        request.session['cart'] = cart
    else:
        client = Userclient.objects.get(user=request.user)
        produit = Produit.objects.get(id=product_id)
        if Panier.objects.filter(Q(produit=produit), Q(client=client), Q(commander=False)).exists():
            cart_line = Panier.objects.get(Q(produit_id=product_id), Q(client_id=client.id), Q(commander=False))
            cart_line.quantite += int(qty)
        else:
            cart_line = Panier(produit=produit, client=client, quantite=qty)
        cart_line.save()

    if request.META.get('HTTP_REFERER'):
        return redirect(my_cart)
    else:
        return redirect(accueil)


def suppr_panier(request):
    """
    Cette fonction permet de vider le panier. Si l'utilisateur n'est pas connecté, la fonction vide le panier virtuel
    stocké en session ; sinon, les objets précédemment persistés en BDD sont supprimés.
    :param request:
    :return:
    """
    if not request.user.is_authenticated() and 'cart' in request.session:
        del request.session['cart']
    else:
        client = Userclient.objects.get(user=request.user)
        Panier.objects.filter(client_id=client.id, commander=False).delete()

    return


def supprime_panier(request):
    suppr_panier(request)

    return redirect(request.META.get('HTTP_REFERER'))


def suppr_produit(request, id, quantity):
    product_id = str(int(id) + int(quantity))
    if not request.user.is_authenticated() and 'cart' in request.session:

        del request.session['cart'][id]
        request.session.modified = True

    else:
        client = Userclient.objects.get(user=request.user)
        Panier.objects.get(client_id=client.id, produit_id=id, commander=False).delete()

    return


def supprime_produit(request, id, quantity):
    suppr_produit(request, id, quantity)
    return redirect(request.META.get('HTTP_REFERER'))


def modifie_produit(request, id, quantity):
    suppr_produit(request, id, quantity)

    return redirect(detailprod, id=id)


def my_cart(request):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    nombre_p = nombre_prod(request)
    total = 0
    form = Quantite(request.POST or None)

    if form.is_valid():
        quantite = form.cleaned_data[quantite]

    if not request.user.is_authenticated():
        if 'cart' in request.session:
            cart = list()
            for product_id, quantity in request.session.get('cart').items():
                cart_line = Panier(produit_id=product_id, quantite=quantity)
                total += cart_line.total()
                list.append(cart, cart_line)
        else:
            cart = None
    else:
        client = Userclient.objects.get(user_id=request.user.id)
        cart = Panier.objects.filter(client_id=client.id, commander=False)
        for cart_line in cart:
            total += cart_line.total()
    return render(request, "produit/panier.html", locals())


# -- View pour les utilisateurs

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def vente(request):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    nombre_p = nombre_prod(request)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    return render(request, "compte/vente.html", locals())


def connexion(request):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    nombre_p = nombre_prod(request)
    error = False
    form = ConnexionForm(request.POST or None)
    connect = False

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            client = Userclient.objects.get(user=user)
            connect = True
            __move_session_cart_to_database_cart(request, client)
            login(request, user)
            error = False
            if request.GET.get('next', False):
                return redirect(request.GET['next'])
            else:
                return redirect(compte_client)
        else:
            error = True
    return render(request, 'compte/connexion.html', locals())


def inscription(request):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    nombre_p = nombre_prod(request)
    inscri = False
    marques = Marque.objects.all()
    categories = Categorie.objects.all()

    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = InscriptionForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    probleme = False
    if form.is_valid():
        # Ici nous pouvons traiter les données du formulaire
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        username = form.cleaned_data['username']
        users = User.objects.all()
        # Nous allons vérifier si le nom d'utilisateur existe déja
        for user in users:
            if user.username in username and username in user.username:
                probleme = True

        if probleme:
            envoi = False
        else:

            user = User.objects.create_user(username, email, password)
            client = Userclient()
            client.user = user
            client.save()
            inscri = True
            __move_session_cart_to_database_cart(request, client)
            login(request, user)

            # Nous pourrions ici envoyer l'e-mail grâce aux données 
            # que nous venons de récupérer
            envoi = True

    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'compte/inscription.html', locals())


def inscription_vendeur(request):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    nombre_p = nombre_prod(request)
    inscri = False
    marques = Marque.objects.all()
    categories = Categorie.objects.all()

    form = VendeurForm(request.POST or None)

    probleme = False
    if form.is_valid():
        # Ici nous pouvons traiter les données du formulaire

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        username = form.cleaned_data['username']
        users = User.objects.all()
        # Nous vérifions si le nom d'utilisateur existe déja
        for user in users:
            if user.username in username and username in user.username:
                probleme = True

        if probleme:
            envoi = False
        else:
            user = User.objects.create_user(username, email, password)
            vendeur = Uservendeur()
            vendeur.numero = form.cleaned_data['numero']
            vendeur.user = user
            vendeur.save()
            inscri = True
            login(request, user)

            # Nous pourrions ici envoyer l'e-mail grâce aux données 
            # que nous venons de récupérer
            envoi = True

    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'compte/inscription-vendeur.html', locals())


@login_required
def compt_admin(request):
    pass


"""

def commande_shop(request , cart , tel , lieu):
    commande = Commande_for_shop()
    commande.panier = cart 
    commande.boutique = cart.produit.boutique
    commande.numero_client = tel
    commande.lieu_de_livraison = lieu
    commande.save()


    return



def commande_client(request , cart):
    commande = Commande_for_client()
    commande.panier = cart 
    commande.client = Userclient.objects.get(user=request.user)
    commande.save()

    return   


"""


@login_required
def confirm_achat(request):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()

    nombre_p = nombre_prod(request)
    envoi = False
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    client = Userclient.objects.get(user_id=request.user.id)
    carts = Panier.objects.filter(client_id=client.id, commander=False)
    form = CommandeForm(request.POST or None)
    address = client.address
    if form.is_valid():
        numero = form.cleaned_data['numero']
        default_address = form.cleaned_data['default_address']

        for panier in carts:

            commande_shop = Commande_for_shop()
            commande_shop.numero_client = numero

            commande_shop.panier = panier

            commande_shop.boutique = panier.produit.boutique

            if (commande_shop.save()):
                commande_save = True

            panier.commander = True
            panier.save()

            if (address == None):
                default_address = False

            if (default_address == True):
                envoi = True
                return render(request, "compte/confirm-achat.html", locals())

            return redirect(pays)

    return render(request, "compte/confirm-achat.html", locals())


def produit_promo(request, page=1):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    nombre_p = nombre_prod(request)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    promos = Promo.objects.all().order_by('-date')

    paginator = Paginator(promos, 40)

    try:

        minis = paginator.page(page)
    except EmptyPage:

        minis = paginator.page(paginator.num_pages)

    return render(request, "produit/promo.html", locals())


def categorie_promo(request, id, page=1):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    nombre_p = nombre_prod(request)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    promos = Promo.objects.filter(produit__categorie__id=id).order_by('-date')

    paginator = Paginator(promos, 40)

    try:

        minis = paginator.page(page)
    except EmptyPage:

        minis = paginator.page(paginator.num_pages)

    return render(request, "produit/categorie_promo.html", locals())


def mesmarque(request):
    pass


def panier(request):
    pass


#######################################################################################
#######################################################################################
#############     ************************************************        #############
#############          Pour Les Vendeurs et leurs commandes               #############
#############     ************************************************        #############
#######################################################################################
#######################################################################################


@login_required
def compte_vendeur(request):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    messages = Message_for_vendeur.objects.all()
    nombre_p = nombre_prod(request)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()

    # -- Les utilisateurs clients
    user = request.user
    user_vendeur = Uservendeur.objects.filter(user=user)

    # -- Les vendeurs leurs boutiques et leurs produits
    if (user_vendeur):

        boutiques = Boutique.objects.filter(vendeur=user_vendeur)
        if (boutiques):
            boutique = Boutique.objects.get(vendeur=user_vendeur)
            commandes_n = Commande_for_shop.objects.filter(boutique=boutique, Livre=False)
            commandes_l = Commande_for_shop.objects.filter(boutique=boutique, Livre=True)
            mes_produits = Produit.objects.filter(boutique=boutique).order_by('-date_creat')

            i = 0
            for com in commandes_n:
                i += 1

            return render(request, "compte/compt-vendeur.html", locals())
        else:
            return redirect(ajouter_boutique)
    else:
        return redirect(compte_client)


@login_required
def compte_client(request):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    nombre_p = nombre_prod(request)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()

    # -- Les utilisateurs clients
    user = request.user
    user_client = Userclient.objects.get(user=user)
    mes_panier_commander = Panier.objects.filter(client=user_client, commander=True)
    commandes_n = Commande_for_shop.objects.filter(panier__client=user_client, panier__commander=True, Livre=False)
    commandes_v = Commande_for_shop.objects.filter(panier__client=user_client, panier__commander=True, vue=True,
                                                   Livre=False)
    commandes_l = Commande_for_shop.objects.filter(panier__client=user_client, panier__commander=True, Livre=True)
    commande_livre = Paginator(commandes_l, 5)
    commande_livrer = commande_livre.page(1)

    abonners = Abonnement.objects.filter(client=user_client)

    return render(request, "compte/compt-client.html", locals())


@login_required
def detail_commande(request, id):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()
    boutique = Boutique.objects.get(vendeur__user=request.user)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()

    commande = Commande_for_shop.objects.get(id=id)
    total = commande.panier.total()
    if (commande.vue == False):
        commande.vue = True
        commande.save()
    return render(request, "compte/detail_commande.html", locals())


@login_required
def livrer(request, id):
    commande = Commande_for_shop.objects.get(id=id)
    commande.Livré = True
    commande.save()
    boutique = Boutique.objects.get(vendeur__user=request.user)
    panier = commande.panier
    commission(boutique.id, panier.id)

    return redirect(compte_vendeur)


@login_required
def produit(request, i):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()

    boutique = Boutique.objects.get(vendeur__user=request.user)
    element = i
    user_vendeur = Uservendeur.objects.filter(user=request.user)
    boutiques = Boutique.objects.filter(vendeur=user_vendeur)
    boutique = Boutique.objects.get(vendeur=user_vendeur)
    produits = Produit.objects.filter(boutique=boutique).order_by('-date_creat')
    categories = Categorie.objects.filter(boutique=boutique)
    marques = Marque.objects.filter(boutique=boutique)
    promos = Promo.objects.filter(boutique=boutique)

    return render(request, "compte/ajout/mes_produit.html", locals())


@login_required
def confirm_sup(request, i, id):
    categories_mere = CategorieMere.objects.all()
    boutiques = Boutique.objects.all()

    boutique = Boutique.objects.get(vendeur__user=request.user)
    if (i == "1"):
        produit = Produit.objects.get(id=id)

    if (i == "2"):
        categorie = Categorie.objects.get(id=id)
        produit_depend = Produit.objects.filter(categorie_id=categorie.id)
    if (i == "3"):
        marque = Marque.objects.get(id=id)
        produit_depend = Produit.objects.filter(marque_id=marque.id)
    if (i == "4"):
        promo = Promo.objects.get(id=id)

    element = i
    return render(request, "compte/confirm_sup.html", locals())


@login_required
def supprimer_element(request, i, id):
    if (i == "1"):
        Produit.objects.get(id=id).delete()

    if (i == "2"):
        Categorie.objects.get(id=id).delete()
    if (i == "3"):
        Marque.objects.get(id=id).delete()
    if (i == "4"):
        prom = Promo.objects.get(id=id)
        for produit in Produit.objects.all():
            if prom.produit == produit:
                produit.prix = produit.prix_normal
                produit.produit_normal = 0
                produit.save()
                prom.delete()

    return redirect(confirm_sup, i=0, id=0)


@login_required
def ajouter_produit(request, id=0):
    if (id == 0):
        bboutique = Boutique.objects.get(vendeur__user=request.user)
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            envoi = True

        return render(request, "compte/ajout/produit.html", locals())

    else:
        bboutique = Boutique.objects.get(vendeur__user=request.user)
        produit = Produit.objects.get(id=id)

        form = ProduitForm(request.POST or None, request.FILES or None, instance=produit)
        if form.is_valid():
            form.save()
            envoi = True

        return render(request, "compte/ajout/produit.html", locals())


@login_required
def ajouter_categorie(request, id=0):
    boutique = Boutique.objects.get(vendeur__user=request.user)
    if (id == 0):
        form = CategorieForm(request.POST or None)
        if form.is_valid():
            form.save()
            envoi = True
    else:

        form = CategorieForm(request.POST or None, instance=Categorie.objects.filter(id=id))
        if form.is_valid():
            form.save()
            envoi = True
    return render(request, "compte/ajout/categorie.html", locals())


@login_required
def ajouter_marque(request, id=0):
    boutique = Boutique.objects.get(vendeur__user=request.user)
    if (id == 0):
        form = MarqueForm(request.POST or None)
        if form.is_valid():
            form.save()
            envoi = True
    else:
        form = MarqueForm(request.POST or None, instance=Marque.objects.filter(id=id))
        if form.is_valid():
            form.save()
            envoi = True
    return render(request, "compte/ajout/marque.html", locals())


@login_required
def ajouter_promos(request, id=0):
    envoi = False
    boutique = Boutique.objects.get(vendeur__user=request.user)

    class PromosForm(forms.Form):
        produit = forms.ModelChoiceField(queryset=Produit.objects.filter(boutique__id=boutique.id), label="Produit ")
        nouveau_prix = forms.FloatField(label="Nouveau prix")
        duree = forms.IntegerField(label="Durée ( en jours ) ")

    form = PromosForm(request.POST or None)
    if form.is_valid():
        produit = form.cleaned_data['produit']
        nouveau_prix = form.cleaned_data['nouveau_prix']
        duree = form.cleaned_data['duree']

        promos = Promo()
        promos.boutique = boutique
        promos.produit = produit
        promos.nouveau_prix = nouveau_prix
        promos.duree = duree
        produit.prix_normal = produit.prix
        produit.prix = nouveau_prix
        produit.save()

        promos.save()

        promos.date_fin = fin_promos(request, promos.id, duree)
        promos.save()

        envoi = True

    return render(request, "compte/ajout/promos.html", locals())


def fin_promos(request, id, duree):
    return Promo.objects.get(id=id).date + timedelta(days=duree)


"""
@login_required
def address_shop(request , boutique):
    form = AddressForm(request.POST or None)


    if form.is_valid():


return render(request,"compte/ajout/address_shop.html" , locals())

"""


@login_required
def ajouter_boutique(request):
    vendeur = Uservendeur.objects.get(user=request.user)
    for boutique in Boutique.objects.all():
        if boutique.user == boutique:
            return redirect(compte_vendeur)

    produit = Produit.objects.all()
    form = BoutiqueForm(request.POST or None)
    if form.is_valid():
        boutique = form.save(commit=False)

        boutique.vendeur = vendeur
        boutique.save()
        return redirect(pays)

    return render(request, "compte/ajout/boutique.html", locals())


def commission(idb, idp):
    boutique = Boutique.objects.get(id=idb)
    panier = Panier.objects.get(id=idp)
    prix = panier.total()

    if (prix < 100000):
        commission = prix * 0.06
    else:
        commission = prix * 0.04

    Commission(boutique=boutique, panier=panier, prix=commission).save()
    return


@login_required
def abonner(request, idc, idb):
    boutique = Boutique.objects.get(id=idb)
    client = Userclient.objects.get(id=idc)
    if (Abonnement.objects.filter(client=client, boutique=boutique)):
        abonner = True
    else:
        abonner = Abonnement()
        abonner.client = client
        abonner.boutique = boutique
        abonner.save()

    return redirect(compte_client)


@login_required
def deabonner(request, idc, idb):
    boutique = Boutique.objects.get(id=idb)
    client = Userclient.objects.get(id=idc)
    if (Abonnement.objects.filter(client=client, boutique=boutique)):
        Abonnement.objects.filter(client=client, boutique=boutique).delete()

    return redirect(compte_client)


@login_required
def dernier_prod(request, idb):
    boutique = Boutique.objects.get(id=idb)
    produit = Produit.objects.filter(boutique__id=idb)
    prod = Paginator(produit, 6)
    produits = prod.page(1)
    return render(request, "produit/dernier_prod.html", locals())


def address(request, id):
    form = AddressForm(request.POST or None)
    address = Address()
    address.localite = Localite.objects.get(id=id)
    if form.is_valid():
        address.cite = form.cleaned_data['cite']
        address.quartier = form.cleaned_data['quartier']
        address.save()
        if request.user.is_authenticated():
            vendeur = Uservendeur.objects.filter(user=request.user)
            if (vendeur):
                boutique = Boutique.objects.get(vendeur=vendeur)
                boutique.address = address
                boutique.save()

                envoi_vendeur = True
            else:
                client = Userclient.objects.get(user=request.user)
                client.address = address
                client.save()

                envoi_client = True

                # for commande in commandes:
                # commande.address =

    return render(request, "compte/address.html", locals())


def localite(request, id):
    class LocaliteForm(forms.Form):
        localite = forms.ModelChoiceField(queryset=Localite.objects.filter(region__id=id),
                                          label="Localité ou Département ")

    form = LocaliteForm(request.POST or None)
    if form.is_valid():
        localite = form.cleaned_data['localite']
        return redirect(address, id=localite.id)
    return render(request, "compte/address.html", locals())


def region(request, id):
    class RegionForm(forms.Form):
        region = forms.ModelChoiceField(queryset=Region.objects.filter(pays__id=id), label="Région ")

    form = RegionForm(request.POST or None)
    if form.is_valid():
        region = form.cleaned_data['region']
        return redirect(localite, id=region.id)
    return render(request, "compte/address.html", locals())


def pays(request):
    form = PaysForm(request.POST or None)
    if form.is_valid():
        pays = form.cleaned_data['pays']
        return redirect(region, id=pays.id)

    return render(request, "compte/address.html", locals())


def redirection(request, nom):
    boutiques = Boutique.objects.all()

    for boutiqu in boutiques:
        shop = boutiqu.nom.lower()
        abrj = boutiqu.nom_abrj.lower()
        if (nom.lower() == shop or nom.lower() == abrj):
            return redirect(boutique, id=boutiqu.id)
    return render(request, "produit/mesboutiques.html", locals())
