from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from random import choice
import re

from . import util

class NewArticleForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Article Title',
            'class': 'new-article'}
    ))
    article = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Markdown Content Here'}
    ))

    def clean_title(self):
        print("Called")
        data = self.cleaned_data.get("title")
        current_entries = util.list_entries()
        for entry in current_entries:
            if data.lower() == entry.lower():
                message = "There is already an article of the same name. Please rename article."
                raise forms.ValidationError(message)
        return data

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new(request):
    if request.method == "POST":
        form = NewArticleForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["title"])
            print(form.cleaned_data["article"])

            file = ContentFile(form.cleaned_data["article"])
            path = 'entries/' + form.cleaned_data["title"] + '.md'
            default_storage.delete(path)
            default_storage.save(path, file)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewArticleForm()
        })

def search(request):
    if request.method == "POST":
        form = request.POST.copy()
        if form['q'] == '':
            return HttpResponseRedirect(reverse("index"))
        all_entries = util.list_entries()
        entries = []
        query = re.compile(form['q'], flags=re.IGNORECASE)
        for result in all_entries:
            if form['q'] == result:
                return HttpResponseRedirect("wiki/"+result)
            elif query.search(result):
                entries.append(result)
        return render(request, "encyclopedia/search.html", {
            "entries": entries
        })
    else:
        return HttpResponseRedirect(reverse("index"))

def edit(request, entry):
    if request.method == "POST":
        form = request.POST

        file = ContentFile(form["article"])
        path = 'entries/' + form["entry"] + '.md'
        default_storage.delete(path)
        default_storage.save(path, file)
        return HttpResponseRedirect(reverse("index"))
    else: 
        if not util.get_entry(entry):
            return render(request, "encyclopedia/error.html")
        return render(request, "encyclopedia/edit.html", {
            "value": util.get_entry(entry),
            "entry": entry
        })

def random(request):
    return HttpResponseRedirect("wiki/"+choice(util.list_entries()))

def entry(request, entry):
    if request.method == "POST":
        return HttpResponseRedirect("/edit/"+entry)
    else:
        if not util.get_entry(entry):
            return render(request, "encyclopedia/error.html")
        entry_formatted = util.get_entry(entry).splitlines()
        entry_output = []

        #Regex
        h = re.compile('#{1,6}')
        list = re.compile(r'^\*{1}')
        bold = re.compile(r'\*{2}[^\*]+\*{2}')
        link = re.compile(r'\[[^\]]+\]\([^\)]+\)')
        link_title = re.compile(r'\[[^\]]+\]')
        link_address = re.compile(r'\([^\)]+\)')

        in_list = False
        out = ''


        for line in entry_formatted:
            #Heading Matching
            if h.match(line):
                h_count = 0
                for c in line:
                    if c == '#':
                        h_count += 1

                out = '<h' + str(h_count) + '>' + h.sub('',line).lstrip() + '</h' + str(h_count) + '>'
                entry_output.append(out)
                out = ''

            #List Matching

            if list.match(line):
                if not in_list:
                    out += '<ul>'
                    in_list = True
                out += '<li>' + list.sub('',line).lstrip() + '</li>'
            else: 
                if in_list:
                    out += '</ul>'
                    entry_output.append(out)
                    in_list = False
                    out = ''

            if (not (list.match(line) or h.match(line))) and len(line) > 0:
                out += '<p>'
                link_out = line
                if link.search(line):
                    iterator = link.finditer(line)
                    link_out = ''
                    index = 0
                    for match in iterator:
                        link_out += line[index:match.span()[0]]
                        title_span = link_title.search(line[index:]).span()
                        address_span = link_address.search(line[index:]).span()
                        title_text = line[index+title_span[0]+1:index+title_span[1]-1]
                        address_text = line[index+address_span[0]+1:index+address_span[1]-1]
                        link_out += '<a href="' + address_text + '">' + title_text + '</a>'
                        index = match.span()[1]
                if bold.search(link_out):
                    iterator = bold.finditer(link_out)
                    format_bold = ''
                    index = 0
                    for match in iterator:
                        format_bold += link_out[index:match.span()[0]] + '<strong>' + link_out[match.span()[0]+2:match.span()[1]-2] + '</strong>'
                        index = match.span()[1]
                    format_bold += link_out[index:] 
                    out += format_bold
                else:
                    out += link_out
                out += '</p>'
                entry_output.append(out)
                out = ''



    
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "entry_output": entry_output
    })

