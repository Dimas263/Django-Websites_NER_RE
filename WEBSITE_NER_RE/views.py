from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd

def index(request):
    context = {
        'judul': 'NLP - Text Mining',
        'subjudul': 'Prediksi Entitas dan Relasi suatu Kalimat',
        'author': 'Dimas Dwi Putra',
        'nav': [
            ['/', 'Home'],
            ['/sample/', 'Kalimat'],
            # ['/predict/', 'Predict'],
            ['/about/', 'About'],
        ]
    }

    return render(request, 'index.html', context)

def sample(request):
    context = {
        'judul': 'NLP - Text Mining | Contoh Kalimat',
        'subjudul': 'Prediksi Entitas dan Relasi suatu Kalimat',
        'author': 'Dimas Dwi Putra',
        'nav': [
            ['/', 'Home'],
            ['/sample/', 'Kalimat'],
            # ['/predict/', 'Predict'],
            ['/about/', 'About'],
        ]
    }
    

    sheet_id = '1A2YQIcaEG1pN7D2o3ikO8zFeQ3ITziQEuh2ja7f3Eyg'
    sheet_name = 'sentences'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

    df = pd.read_csv(url)
    
    sentences = []
    for s in zip(df['sentences'].tolist()):
      sentences.append(s)
    
    join_sentences = (','.join(str(a)for a in sentences))
    replace_first = join_sentences.replace("('Public ","<span class='text-danger'>-</span> Public ")
    replace_second = replace_first.replace("',),('","<br><br><span class='text-danger'>-</span> ")
    replace_third = replace_second.replace("',)","")
    sentences = replace_third.replace(",- Public","<br><br><span class='text-danger'>-</span> Public")

    context['samples'] = sentences 

    return render(request, 'sample.html', context)
