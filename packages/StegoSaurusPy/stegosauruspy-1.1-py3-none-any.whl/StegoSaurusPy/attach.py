def attach(target_file_path: str, data: bytes):
    splitname = target_file_path.split(".")
    extension = splitname.pop()
    backup_file_name = ".".join(splitname) + ".backup." + extension

    with open(backup_file_name, "wb") as backup_file, open(target_file_path, "rb") as original_file:
        backup_file.write(original_file.read())

    target_file = open(target_file_path, "ab")

    target_file.write(bytes("", "UTF-8"))
    target_file.write(data)

    target_file.close()
