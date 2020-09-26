def to_latex(set_to_export, inline=True):
    start_delim = "$" if inline else "\\["
    end_delim = "$" if inline else "\\]"
    return f"{start_delim}{set_to_export.__latex__()}{end_delim}"