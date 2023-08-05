import os

def detach(target_file_path) -> bytes:
    target_file = open(target_file_path, "rb")
    src_size = os.path.getsize(target_file_path)

    src_bytes = []

    for i in range(src_size):
        src_bytes.append(target_file.read(1))

    src_bytes = src_bytes[::-1]
    out_bytes = []

    for end_byte in src_bytes:
        if end_byte == bytes("", "UTF-8"):
            break
        out_bytes.append(end_byte)

    out_bytes = out_bytes[::-1]

    return b"".join(out_bytes)