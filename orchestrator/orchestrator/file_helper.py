def load_content_as_string(file_name, break_lines=False) -> str:
    with open(file_name, mode="r", encoding="utf-8") as file:
        if break_lines:
            return "".join(f"{line.rstrip()}\n" for line in file)
        else:
            return "".join(line.rstrip() for line in file)
