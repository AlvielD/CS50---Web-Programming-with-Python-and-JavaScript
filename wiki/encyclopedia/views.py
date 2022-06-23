from logging import exception
from turtle import width
from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from django import forms

from . import util

class SearchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewEntry(forms.Form):
    entryName = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Entry\'s Name', 'class': 'entryfield'}))
    entryBody = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Write here the body of your entry...', 'class': 'entryfield'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        # There might be a way of not creating a form everytime we call the layout (Mayber overriding render or smth)
        "form": SearchForm(),
        "path": request.path,
        "entries": util.list_entries()
    })

def render_entry(request, entry):

    # Try to render the page if it exists, otherwise, display an error page
    try:
        # Create an object to convert the markdown to HTML
        markdowner = Markdown()

        # Open file and read it, then, store in the context var
        with open(f"entries/{entry}.md") as f:
            page_content = markdowner.convert(f.read())
    
        return render(request, f"encyclopedia/entry.html", {
            "form": SearchForm(),
            "entry": entry,
            "page_content": page_content
        })
    except:
        return render(request, "encyclopedia/error.html", {
            "form": SearchForm()
        })

def show_results(request):

    # Check if the method is POST
    if request.method == "POST":
        form = SearchForm(request.POST)

        # Check if form data is valid (server-side validation)
        if form.is_valid():

            # Get the 'cleaned' version of form data
            query = form.cleaned_data['query']

            entries = util.list_entries()   # Entries in the encyclopedia
            results = []                    # List of entries that contains the query as a substring.

            # Now, process the data
            if query in entries:
                return render_entry(request, query)
            else:
                # For each entry in the encyclopedia, check if it contains the query as a substring
                for entry in entries:
                    # If the entry has the query as substring, then add it to the list of results.
                    if entry.find(query) != -1:
                        results.append(entry)
                
                # Render the page with the results of the searching.
                return render(request, "encyclopedia/results.html", {
                    'form': SearchForm(),
                    'results': results
                })

    raise Exception("Something unexpected happened...")

# TODO Code the backend for the creation of the entry. Need to receive it, store as an .md file an display it.
def create_newpage(request):
    return render(request, "encyclopedia/create.html", {
        'form': SearchForm(),
        'entryForm': NewEntry()
    })