from django.shortcuts import render


def about(request):
    return render(request, "about.html")


def home(request):
    return render(request, "home.html")


def sample(request):
    data = {
        'movies': [
            {
                'title': "Arsenic and Old Lace",
                'director': "Frank Capra",
                'recommended': True,
            },
            {
                'title': "Citizen Kane",
                'director': "Orson Welles",
                'recommended': True,
            },
            {
                'title': "Doctor Zhivago",
                'director': "David Lean",
                'recommended': False,
            },
            {
                'title': "The Maltese Falcon",
                'director': "John Huston",
                'recommended': True,
            },
        ]
    }
    return render(request, "sample.html", data)
