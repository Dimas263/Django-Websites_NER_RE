from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'judul': 'NLP - Text Mining | About',
        'subjudul': 'Prediksi Entitas dan Relasi suatu Kalimat',
        'author': 'Dimas Dwi Putra',
        'nav': [
            ['/', 'Home'],
            ['/sample/', 'Kalimat'],
            # ['/predict/', 'Predict'],
            ['/about/', 'About'],
        ]
    }
    return render(request, "about.html", context)
