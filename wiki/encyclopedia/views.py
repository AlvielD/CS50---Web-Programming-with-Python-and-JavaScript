from logging import exception
import random
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
    formType = forms.CharField(label="", widget=forms.HiddenInput())


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
            "form": SearchForm(),
            "error_message": "The requested entry does not have a page or was not found. Please check the URL and try again."
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

# TODO You can only edit once, because the url is not redirected.
def create_newpage(request):

    if request.method == 'POST':
        # If the request comes from the entry, it needs to be edited.
        if request.META['HTTP_REFERER'].find('create') == -1:
            # Get the entry name from the HTML form
            entry = request.POST.get('name')

            # Get the markdown version of the page's content
            with open(f"entries/{entry}.md") as f:
                # Read the first two lines to skip the title
                f.readline()
                f.readline()
                md_content = f.read()

            # render the entry with the existing content
            return render(request, "encyclopedia/create.html", {
                "form": SearchForm(),
                "entryForm": NewEntry(initial={'entryName': entry, 'entryBody': md_content, "formType": "edit"})
            })
        else:
            # The entry is being created
            form = NewEntry(request.POST)

            if form.is_valid():

                # Get the data from the form
                name = form.cleaned_data['entryName']
                body = form.cleaned_data['entryBody']
                entryType = form.cleaned_data['formType']

                if name in util.list_entries() and entryType != "edit":

                    # The entry already exists and is not asking to be edited
                    return render(request, "encyclopedia/error.html", {
                        "form": SearchForm(),
                        "error_message": "You tried to create an entry that already exists in the encyclopedia."
                    })
                else:
                    # Write the entry as an .md file
                    with open(f'entries/{name}.md', 'w') as f:
                        f.write(f'#{name}\n\n{body}')
                    
                    return render_entry(request, name)
            else:
                # If the form is invalid, re-render the page with the existing information.
                return render(request, "encyclopedia/create.html", {
                    "form": SearchForm(),
                    "entryForm": NewEntry(initial={"entryName": name, "entryBody": body})
                })

    # This is only if the request method is GET
    return render(request, "encyclopedia/create.html", {
        'form': SearchForm(),
        'entryForm': NewEntry()
    })


def random_page(request):

    entries = util.list_entries()
    entry = random.choice(entries)

    return render_entry(request, entry)