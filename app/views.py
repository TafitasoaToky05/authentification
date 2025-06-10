from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from app.models import Material
import csv


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        username = username.strip() if username else ''

        if not username or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('admin_page')
            else:
                return redirect('user_page')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return render(request, 'login.html', {'username': username})

    return render(request, 'login.html')


@login_required
def user_page(request):
    materials = Material.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        materials = materials.filter(
            Q(name__icontains=search_query) |
            Q(reference__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    context = {
        'materiels': materials,
        'search_query': search_query,
        'users': request.user
    }
    return render(request, 'base.html', context)


@login_required
def admin_page(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('user_page')

    search_query = request.GET.get('search', '')
    materiels = Material.objects.all()
    if search_query:
        materiels = materiels.filter(
            Q(name__icontains=search_query) |
            Q(reference__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    users = User.objects.all()
    context = {
        'materiels': materiels,
        'search_query': search_query,
        'users': users
    }
    return render(request, 'admin.html', context)


@login_required
def add_admin_materiel(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        reference = request.POST.get('reference')
        category = request.POST.get('category')
        stat = request.POST.get('stat') == 'on'
        repere = request.POST.get('repere') == 'on'

        if not (name and reference and category):
            return render(request, 'add_admin.html', {'error': "Tous les champs obligatoires doivent être remplis."})

        if Material.objects.filter(reference=reference).exists():
            return render(request, 'add_admin.html', {'error': "Un matériel avec cette référence existe déjà."})

        try:
            materiel = Material(
                name=name,
                reference=reference,
                category=category,
                stat=stat,
                repere=repere
            )
            materiel.full_clean()
            materiel.save()
            return redirect('admin_page')
        except ValidationError as e:
            return render(request, 'add_admin.html', {'error': e.messages})
    return render(request, 'add_admin.html')


@login_required
def edit_view(request, id):
    materiel = get_object_or_404(Material, id=id)
    if request.method == 'POST':
        materiel.name = request.POST.get('name')
        materiel.reference = request.POST.get('reference')
        materiel.category = request.POST.get('category')
        materiel.stat = request.POST.get('stat') in ['on', 'True', 'true', '1']
        materiel.repere = request.POST.get('repere') in ['on', 'True', 'true', '1']
        try:
            materiel.full_clean()
            materiel.save()
            return redirect('user_page')
        except ValidationError as e:
            return render(request, 'edit.html', {'materiel': materiel, 'errors': e.messages})
    return render(request, 'edit.html', {'materiel': materiel})


@login_required
def voir_plus(request, id):
    materiel = get_object_or_404(Material, id=id)
    return render(request, 'voirMateriel.html', {'materiel': materiel})


@login_required
def delete(request, id):
    materiel = get_object_or_404(Material, id=id)
    try:
        materiel.delete()
        return redirect('home')
    except Exception as e:
        return HttpResponse(f"Erreur lors de la suppression : {str(e)}", status=500)


@login_required
def add_materiel(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        reference = request.POST.get('reference')
        category = request.POST.get('category')
        stat = request.POST.get('stat') == 'on'
        repere = request.POST.get('repere') == 'on'

        if not (name and reference and category):
            return render(request, 'ajoutMateriel.html', {'error': "Tous les champs obligatoires doivent être remplis."})

        if Material.objects.filter(reference=reference).exists():
            return render(request, 'ajoutMateriel.html', {'error': "Un matériel avec cette référence existe déjà."})

        try:
            materiel = Material(
                name=name,
                reference=reference,
                category=category,
                stat=stat,
                repere=repere
            )
            materiel.full_clean()
            materiel.save()
            return redirect('user_page')
        except ValidationError as e:
            return render(request, 'ajoutMateriel.html', {'error': e.messages})
    return render(request, 'ajoutMateriel.html')


@login_required
def voir_plus_admin(request, id):
    materiel = get_object_or_404(Material, id=id)
    return render(request, 'voir_plus_admin.html', {'materiel': materiel})


@login_required
def edit_view_admin(request, id):
    materiel = get_object_or_404(Material, id=id)
    if request.method == 'POST':
        materiel.name = request.POST.get('name')
        materiel.reference = request.POST.get('reference')
        materiel.category = request.POST.get('category')
        materiel.stat = request.POST.get('stat') in ['on', 'True', 'true', '1']
        materiel.repere = request.POST.get('repere') in ['on', 'True', 'true', '1']
        try:
            materiel.full_clean()
            materiel.save()
            return redirect('admin_page')
        except ValidationError as e:
            return render(request, 'modif_admin.html', {'materiel': materiel, 'errors': e.messages})
    return render(request, 'modif_admin.html', {'materiel': materiel})


@login_required
def delete_admin(request, id):
    materiel = get_object_or_404(Material, id=id)
    try:
        materiel.delete()
        return redirect('admin_page')
    except Exception as e:
        return HttpResponse(f"Erreur lors de la suppression : {str(e)}", status=500)



@login_required
def recherche(request):
  query = request.GET.get('q', '')
  materiels = Material.objects.all()
  if query:
    materiels = materiels.filter(
      Q(name__icontains=query) |
      Q(reference__icontains=query) |
      Q(category__icontains=query)
    )
  return render(request, 'base.html', {
    'materiels': materiels,
    'request': request,  # Pour {{ request.GET.q }} dans le template
  })


@login_required
def recherche_admin(request):
    query = request.GET.get('q', '')
    materiels = Material.objects.all()
    if query:
        materiels = Material.objects.filter(
            Q(name__icontains=query) |
            Q(reference__icontains=query) |
            Q(category__icontains=query)
        )
    else:
        materiels = Material.objects.all()
    users = User.objects.all()
    return render(request, 'admin.html', {
        'materiels': materiels,
        'query': query,
        'users': users
    })

@login_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('firstname', '').strip()
        last_name = request.POST.get('lastname', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not (first_name and last_name and email and password1 and password2):
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, 'add_user.html')

        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'add_user.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Un utilisateur avec ce nom d'utilisateur existe déjà.")
            return render(request, 'add_user.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Un utilisateur avec cet email existe déjà.")
            return render(request, 'add_user.html')

        try:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1
            )
            user.full_clean()
            user.save()
            # Ne pas connecter le nouvel utilisateur, rester sur l'admin
            return redirect('admin_page')

        except Exception as e:
            messages.error(request, f"Erreur lors de l'inscription : {e}")
            return render(request, 'add_user.html')

    return render(request, 'add_user.html')




def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('firstname', '').strip()
        last_name = request.POST.get('lastname', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not (first_name and last_name and email and password1 and password2):
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, 'register.html')

        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Un utilisateur avec cet nom utilisateur existe déjà.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Un utilisateur avec cet email existe déjà.")
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1
            )
            login(request, user)
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Erreur lors de l'inscription : {e}")
            return render(request, 'register.html')

    return render(request, 'register.html')


@login_required
def to_block(request, id):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "Accès refusé")
        return redirect('user_page')

    user = get_object_or_404(User, pk=id)
    if user == request.user:
        messages.error(request, "Vous ne pouvez pas bloquer ou débloquer votre propre compte.")
        return redirect('admin_page')

    user.is_active = not user.is_active
    action = "bloqué" if not user.is_active else "débloqué"
    try:
        user.save()
        messages.success(request, f"L'utilisateur {user.username} a été {action}.")
    except Exception as e:
        messages.error(request, f"Erreur lors de la modification : {e}")

    return redirect('admin_page')

@login_required 
def delete_user(request, id):
    user = get_object_or_404(User, pk=id)
    try:
        user.delete()
        return redirect('admin_page')
    except Exception as e:
        return redirect(f"Erreur lors de la suppression : {str(e)}", status=500)
    
@login_required
def export(request):
    # Création d'une réponse HTTP avec un type de contenu CSV
    response = HttpResponse(content_type='text/csv')
    
    # Indique au navigateur que la réponse est un fichier à télécharger
    # et définit le nom du fichier téléchargé comme 'listes_materiels.csv'
    response['Content-Disposition'] = 'attachment; filename="listes_materiels.csv"'

    # Création d'un objet writer pour écrire dans le fichier CSV
    writer = csv.writer(response)

    # Écriture de la première ligne (en-têtes des colonnes) dans le CSV
    writer.writerow(['Nom', 'Référence', 'Catégorie', 'Disponible', 'Repéré'])

    # Parcours de tous les objets Material dans la base de données
    for material in Material.objects.all():
        writer.writerow([
            material.name,
            material.reference,
            material.category,
            'Oui' if material.stat else 'Non',
            'Oui' if material.repere else 'Non'
        ])

    # Retourne la réponse HTTP contenant le fichier CSV à télécharger
    return response
