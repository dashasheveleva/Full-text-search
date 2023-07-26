from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchRank
from django.db.models import F, Q
from .models import Organization


def home_view(request):
    """
    Обработчик представления для домашней страницы.

    GET-запрос:
    - Извлекаем поисковый запрос из параметров запроса.
    - Используем SearchVector для выполнения полнотекстового поиска по полям full_name и short_name.
    - Используем SearchRank для определения релевантности результатов поиска.
    - Используем __icontains для выполнения частичного поиска по полям full_name и short_name.
    - Объединяем результаты полнотекстового поиска и частичного поиска в Python коде.

    :param request: HTTP-запрос, который содержит поисковый запрос.
    :return: Возвращает HTML-страницу 'home.html' с результатами поиска и поисковым запросом.
    """
    if request.method == 'GET':
        # Получаем поисковый запрос из параметров запроса.
        query = request.GET.get('search_query', '')

        # Используем SearchVector для выполнения полнотекстового поиска по полям full_name и short_name.
        vector = SearchVector('full_name', 'short_name')
        results_full_text = Organization.objects.annotate(search=vector).filter(search=query)

        # Используем SearchRank для определения релевантности результатов полнотекстового поиска.
        rank = SearchRank(vector, query)
        results_full_text = results_full_text.annotate(rank=rank)

        # Используем __icontains для выполнения частичного поиска по полям full_name и short_name.
        results_partial_text = Organization.objects.filter(
            Q(full_name__icontains=query) | Q(short_name__icontains=query)
        )

        # Объединяем результаты полнотекстового поиска и частичного поиска в Python коде and remove duplicates.
        results = list(results_full_text) + list(results_partial_text)
        results = sorted(results, key=lambda x: x.rank if hasattr(x, 'rank') and x.rank else float('-inf'))

        # Use a set to remove duplicates
        unique_results = list(set(results))

        # Возвращаем HTML-страницу 'home.html' с результатами поиска и поисковым запросом.
        return render(request, 'home.html', {'results': unique_results, 'search_query': query})
