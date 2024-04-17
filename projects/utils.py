from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search(request, model_class, query_set_name='query_set'):
    '''
    filters records from a table using custom model managers
    '''
    q = request.GET.get("search_query", '')
    result = \
        model_class.search.search(q_string=q) if q else model_class.objects.all()
    context = {
        query_set_name: result,
        "q": q
    }
    return context

def paginate(request, result_count, q_set):
    
    try:
        page_number = int(request.GET.get('page'))
    except ValueError:
        page_number = 1

    pages = Paginator(q_set, result_count)
    # if not isinstance(page_number, int):
    #     print("Nada bruv")
    try:
        query_set = pages.page(page_number)
    except EmptyPage:
        page_number = pages.num_pages
        query_set = pages.page(page_number)

    if page_number - 2 < 1:
        left_index = 1
    else:
        left_index = page_number - 2

    if page_number + 3 > pages.num_pages:
        right_index = pages.num_pages
    else:
        right_index = page_number + 3

    # custom_range = range(left_index, right_index)

    return query_set, right_index, left_index, pages.num_pages
