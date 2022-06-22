from turtle import width
from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from django import forms

from . import util

class SearchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

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

            # Now, process the data
            if query in util.list_entries():
                return render_entry(request, query)
            else:
                # TODO display a page with substrings as results
                pass
    
    # TODO Maybe give some feedback that the query was not correct
    return index(request)