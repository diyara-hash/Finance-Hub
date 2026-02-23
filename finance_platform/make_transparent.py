from PIL import Image
import os

# Define paths
base_dir = r"c:\Users\diyar.arslan\Desktop\finance_platform\finance_platform\simulator\static\similator\img"
input_path = os.path.join(base_dir, "logo.png")
output_path = os.path.join(base_dir, "logo.png") # Overwrite directly or save to temp then move

print(f"Processing: {input_path}")

try:
    img = Image.open(input_path)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        # Beyaz ve beyaza yakın pikselleri şeffaf yap
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(output_path, "PNG")
    print(f"Success! Transparent logo saved to: {output_path}")

except Exception as e:
    print(f"Error: {e}")
