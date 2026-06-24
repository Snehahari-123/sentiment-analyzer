from django.shortcuts import render
from .models import SentimentRecord
from textblob import TextBlob
from django.db.models import Count

def home(request):
    result = None

    if request.method == "POST":
        text = request.POST.get("text")

        score = TextBlob(text).sentiment.polarity

        if score > 0:
            sentiment = "Positive 😊"
        elif score == 0:
            sentiment = "Neutral 😐"
        else:
            sentiment = "Negative 😞"

        SentimentRecord.objects.create(text=text, sentiment=sentiment)
        result = sentiment

    return render(request, "home.html", {"result": result})


def history(request):
    data = SentimentRecord.objects.all().order_by('-created_at')
    return render(request, "history.html", {"data": data})


def dashboard(request):
    stats = SentimentRecord.objects.values('sentiment').annotate(count=Count('sentiment'))
    return render(request, "dashboard.html", {"stats": stats})