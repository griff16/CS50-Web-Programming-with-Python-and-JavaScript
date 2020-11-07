import random
from django.urls import reverse
from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title): 
    mrkdown = Markdown()
    result = util.get_entry(title)
    entry = mrkdown.convert(result) if result is not None else None

    if entry:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "title": title
        })

    return render(request, "encyclopedia/error.html")

def random_page(request):
    return redirect(reverse("entry",
                            kwargs={
                                "title": random.choice(util.list_entries())
                            }))
