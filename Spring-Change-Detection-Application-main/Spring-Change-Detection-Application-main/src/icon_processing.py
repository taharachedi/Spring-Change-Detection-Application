from PIL import Image

# Load the generated PNG
img = Image.open(r"D:\03. Projects\Spring-Change-Detection-Application\src\icon\spring_change_icon.png")

# Save as .ico with all required sizes
img.save("app_icon.ico", sizes=[(16,16), (32,32), (48,48), (256,256)])
