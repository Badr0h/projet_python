from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.conf import settings

from .models import Item, Category, UserProfile, ItemImage
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm

User = get_user_model()

class RegisterView(FormView):
    template_name = 'rental/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        messages.success(self.request, 'Compte créé avec succès !')
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Créer un compte'
        return context

class LoginView(FormView):
    template_name = 'rental/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, f'Bienvenue, {user.first_name} !')
        return super().form_valid(form)
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else str(self.success_url)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Connexion'
        return context

def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Vous avez été déconnecté avec succès.')
    return redirect('home')

class ProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'rental/profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def form_valid(self, form):
        messages.success(self.request, 'Profil mis à jour avec succès !')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mon Profil'
        return context

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email__iexact=email, is_active=True)
        except User.DoesNotExist:
            messages.error(self.request, 'Aucun compte n\'est associé à cette adresse email.')
            return self.form_invalid(form)
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(*args, **kwargs)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    form_class = SetPasswordForm
    token_generator = default_token_generator
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
            
        # Check if the user exists and token is valid
        try:
            uid = force_str(urlsafe_base64_decode(kwargs['uidb64']))
            self.user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            self.user = None
            
        if self.user is not None and not self.token_generator.check_token(self.user, kwargs['token']):
            self.user = None
            
        if self.user is None:
            messages.error(self.request, 'Le lien de réinitialisation est invalide ou a expiré.')
            return redirect('password_reset')
            
        return super().dispatch(*args, **kwargs)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(*args, **kwargs)

class HomeView(ListView):
    model = Item
    template_name = 'rental/home.html'
    context_object_name = 'items'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Item.objects.filter(available=True)
        category_slug = self.request.GET.get('category')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ItemDetailView(DetailView):
    model = Item
    template_name = 'rental/item_detail.html'
    context_object_name = 'item'

class AddItemView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['title', 'description', 'price_per_day', 'category', 'condition']
    template_name = 'rental/add_item.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        
        # Handle image uploads
        images = self.request.FILES.getlist('images')
        if not images:
            form.add_error(None, 'Veuillez ajouter au moins une photo.')
            return self.form_invalid(form)
            
        try:
            for i, img in enumerate(images):
                if i == 0:  # First image is the main one
                    ItemImage.objects.create(item=self.object, image=img, is_main=True)
                else:
                    if i >= 5:  # Limit to 5 images
                        break
                    ItemImage.objects.create(item=self.object, image=img)
            
            messages.success(self.request, 'Annonce publiée avec succès !')
            return super().form_valid(form)
            
        except Exception as e:
            # If there's an error with image upload, delete the created item
            self.object.delete()
            form.add_error(None, f'Une erreur est survenue lors du téléchargement des images: {str(e)}')
            return self.form_invalid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Votre annonce a été publiée avec succès !')
        return reverse('home')

@login_required
def dashboard(request):
    user_items = Item.objects.filter(owner=request.user).order_by('-created_at')
    context = {
        'user_items': user_items,
    }
    return render(request, 'rental/dashboard.html', context)


def reservation_view(request, pk):
    """View for handling item reservations."""
    item = get_object_or_404(Item, pk=pk)
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        message = request.POST.get('message', '')
        
        # Calculate duration and total price
        if start_date and end_date:
            from datetime import datetime
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            duration = (end - start).days + 1
            total_price = duration * item.price_per_day
            
            # In a real application, you would save the reservation to the database here
            # For example:
            # reservation = Reservation.objects.create(
            #     item=item,
            #     renter=request.user,
            #     start_date=start_date,
            #     end_date=end_date,
            #     total_price=total_price,
            #     status='pending',
            #     message=message
            # )
            
            context = {
                'item': item,
                'start_date': start_date,
                'end_date': end_date,
                'duration': duration,
                'total_price': total_price,
                'message': message,
            }
            return render(request, 'rental/reservation_confirmation.html', context)
        
        messages.error(request, 'Veuillez sélectionner des dates valides.')
        return redirect('item-detail', pk=pk)
        
    return render(request, 'rental/reservation.html', {'item': item})
