import matplotlib.pyplot as plt
import pydicom
import imageio
from skimage import exposure

# Carregar o arquivo DICOM
ds = pydicom.dcmread(r"C:\Users\alice\dicom\000ae00eb3942d27e0b97903dd563a6e.dicom")

# Obter a matriz de pixel da imagem DICOM
pixel_array = ds.pixel_array

# Exibir a imagem original
plt.imshow(pixel_array, cmap="gray")
plt.axis("off")
plt.show()

# Salvar a imagem original como PNG
imageio.imwrite("imagem_original.png", pixel_array)

# Normalizar contraste para melhorar a visualização
pixel_array_norm = exposure.rescale_intensity(pixel_array, out_range=(0, 255))

# Salvar a imagem com contraste ajustado
imageio.imwrite("imagem_contraste.png", pixel_array_norm.astype("uint8"))

# Exibir a imagem com contraste ajustado
plt.imshow(pixel_array_norm, cmap="gray")
plt.axis("off")
plt.show()

