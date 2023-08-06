

def pathify(text: str = None, class_name: str = None, **kwargs):
    paths = []
    if class_name:
        paths.append(f"@class='{class_name}'")
    if text:
        paths.append(f"normalize-space(text())='{text}'")
    for key, value in kwargs.items():
        if '_contains' in key:
            length = len('_contains')
            attribute = key[:-length]
            if attribute == 'class_name':
                attribute = "class"
            if attribute == 'text':
                paths.append(f"contains(normalize-space(text()), '{value}')")
            else:
                paths.append(f"contains(@{attribute}, '{value}')")
        elif '_starts_with' in key:
            length = len('_starts_with')
            attribute = key[:-length]
            if attribute == 'class_name':
                attribute = "class"
            if attribute == 'text':
                paths.append(f"starts-with(normalize-space(text()), '{value}')")
            else:
                paths.append(f"starts-with(@{attribute}, '{value}')")
        elif '_ends_with' in key:
            length = len('_ends_with')
            attribute = key[:-length]
            if attribute == 'class_name':
                attribute = "class"
            if attribute == 'text':
                paths.append(f"ends-with(normalize-space(text()), '{value}')")
            else:
                paths.append(f"ends-with(@{attribute}, '{value}')")
        elif '_regex' in key:
            length = len('_regex')
            attribute = key[:-length]
            if attribute == 'class_name':
                attribute = "class"
            if attribute == "text":
                paths.append(f"matches(normalize-space(text()), '{value}')")
            else:
                paths.append(f"matches(@{attribute}, '{value}')")
        else:
            paths.append(f"@{key}='{value}'")
    if paths:
        return '[' + ' and '.join(paths) + ']'
    return ''