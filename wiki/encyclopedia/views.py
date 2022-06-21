from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
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
            "entry": entry,
            "page_content": page_content
        })
    except:
        return render(request, "encyclopedia/error.html")
