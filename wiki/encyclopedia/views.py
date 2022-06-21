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

    # Create an object to convert the markdown to HTML
    markdowner = Markdown()

    # Open file and read it, then, store in the context var
    with open(f"entries/{entry}.md") as f:
        page_content = markdowner.convert(f.read())
    
    # Try to render the page if it exists, otherwise, display an error page
    try:
        return render(request, f"encyclopedia/entry.html", {
            "entry": entry,
            "page_content": page_content
        })
    except:
        # TODO Design an error web page for unexistence entries
        return HttpResponse("The requested page was not found")
