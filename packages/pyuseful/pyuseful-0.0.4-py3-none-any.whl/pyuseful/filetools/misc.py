def mod_name_with_ext(filename: str, mod: str):
    split_line = filename.split(".")
    ext = split_line[-1]
    base = ".".join(split_line[:-1])

    return f"{base}.{ext}"