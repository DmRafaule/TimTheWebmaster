from django.shortcuts import render
from Main.utils import initDefaults


def tool_main(request):
    context = initDefaults(request)
    return render(request, 'NewsAggregator/news_aggregator.html', context=context)
