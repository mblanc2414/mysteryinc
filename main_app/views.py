from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Character, Unmasked, Photo
from .forms import UnmaskedForm

import uuid 
import boto3

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'mysteryincapp'


def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def characters_index(request):
  characters = Character.objects.filter(user=request.user)
  return render(request, 'characters/index.html', { 'characters': characters })

@login_required
def characters_detail(request, characters_id):
  characters = Character.objects.get(id=characters_id)
  unmasked_form = UnmaskedForm()
  
  return render(request, 'characters/detail.html', {
    'characters': characters, 'unmasked_form': unmasked_form,
   
  })

@login_required
def add_unmasked(request, characters_id):
  # create the ModelForm using the data in request.POST
  form = UnmaskedForm(request.POST)
  # validate the form
  if form.is_valid():
   
    new_unmasked = form.save(commit=False)
    new_unmasked.characters_id = characters_id
    new_unmasked.save()
  return redirect('detail', characters_id=characters_id)



@login_required
def add_photo(request, characters_id):
  # attempt to collect the photo file data
  photo_file = request.FILES.get('photo-file', None)
  # use conditional logic to determine if file is present
  if photo_file:
  # if it's present, we will create a reference the the boto3 client
    s3 = boto3.client('s3')
    # create a unique id for each photo file
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    # funny_cat.png = jdbw7f.png
    # upload the photo file to aws s3
    try:
    # if successful
      s3.upload_fileobj(photo_file, BUCKET, key)
      # take the exchanged url and save it to the database
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
     
      photo = Photo(url=url, characters_id=characters_id)
      
      photo.save()
    except Exception as error:
      print("Error uploading photo: ", error)
      return redirect('detail', characters_id=characters_id)
    # print an error message
  return redirect('detail', characters_id=characters_id)
  # redirect the user to the origin 


def signup(request):
  error_messages = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_messages = 'Invalid Info - Please Try Again'
  form = UserCreationForm()
  context = {
    'form': form, 
    'error_messages': error_messages
  }
  return render(request, 'registration/signup.html', context)



class CharacterCreate(LoginRequiredMixin, CreateView):
  model = Character
  fields = ['name', 'description', 'alias', 'origin']
  success_url = '/characters/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class CharacterUpdate(LoginRequiredMixin, UpdateView):
  model = Character

  fields = [ 'name', 'description', 'alias', 'origin']

class CharacterDelete(LoginRequiredMixin, DeleteView):
  model = Character
  success_url = '/characters/'

