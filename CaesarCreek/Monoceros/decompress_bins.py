# decompress_bins.py
import os, zlib, json

ctx = "context"
with open(os.path.join(ctx, "index.json"), "r") as f:
    meta = json.load(f)

out = "context_decompressed"
os.makedirs(out, exist_ok=True)

for seg in meta.get("segments", []):
    bin_path = os.path.join(ctx, seg["file"])
    name = seg.get("name") or os.path.basename(seg["file"]).split(".")[0]
    with open(bin_path, "rb") as bf:
        raw = bf.read()
    try:
        data = zlib.decompress(raw)
    except zlib.error:
        data = raw  # not compressed
    with open(os.path.join(out, f"{name}.bin"), "wb") as wf:
        wf.write(data)
    print("wrote", name)
