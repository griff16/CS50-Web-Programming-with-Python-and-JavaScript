import random
from django import forms
from django.urls import reverse
from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util

# Forms
class CreatePageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

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

def search(request):
    if not request.GET["q"]:
        return redirect(reverse("index"))

    query = request.GET["q"]
    entries = util.list_entries()

    if query in entries:
        return redirect(reverse("entry", kwargs={"title": query}))

    return render(request, "encyclopedia/search.html", {
                    "query": query,
                    "entries": [entry for entry in entries
                                    if query.lower() in entry.lower()]}  
                )

def create(request):
    if request.method == "POST":
        form = CreatePageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if title.lower() in [entry.lower() for entry in util.list_entries()]:
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "error": "This page already exists"
                })

            util.save_entry(title, content)
            return redirect(reverse("entry", kwargs={"title": title}))

        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })

    return render(request, "encyclopedia/create.html", {
        "form": CreatePageForm
    })

def edit(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect(reverse("entry", kwargs={"title": title}))

    form = EditPageForm({
        "content": util.get_entry(title)
    })

    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title
    })

