from django.shortcuts import render
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    mrkdown = Markdown()
    entry = mrkdown.convert(util.get_entry(title))

    if entry:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "title": title
        })

    return render(request, "encyclopedia/error.html")
