def paginate(list, page, per_page):
    length = len(list)
    pages = 1
    if per_page < length:
        pages = length//per_page
        if length/per_page > length//per_page:
            pages = pages + 1
    has_pre = page != 1
    has_next = page < pages
    foot = per_page*page
    head = foot - per_page
    result = list[head:foot]
    paginate = {
        "page": page,
        "length": length,
        "pages": pages,
        "has_next": has_next,
        "has_pre": has_pre,
        "result": result,
    }
    return paginate