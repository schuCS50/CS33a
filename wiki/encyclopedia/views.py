from django.shortcuts import render
import re

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if not util.get_entry(entry):
        return render(request, "encyclopedia/error.html")
    entry_formatted = util.get_entry(entry).splitlines()
    entry_output = []

    #Regex
    h = re.compile('#{1,6}')
    list = re.compile('^\*{1}')
    bold = re.compile('\*{2}[^\*]+\*{2}')
    link = re.compile('\[[^\]]+\]\([^\)]+\)')
    link_title = re.compile('\[[^\]]+\]')
    link_address = re.compile('\([^\)]+\)')

    in_list = False
    out = ''


    for line in entry_formatted:
        print(line)
        #Heading Matching
        if h.match(line):
            h_count = 0
            for c in line:
                if c == '#':
                    h_count += 1
            
            out = '<h' + str(h_count) + '>' + h.sub('',line).lstrip() + '</h' + str(h_count) + '>'
            print(out)
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
                print("link")
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

