import subprocess
import cv2
import numpy as np
import os

# — Passo 1: Script para o Blender gerar a cena + render —
"""
SCRIPT_BLENDER = 
import bpy

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Cena simples
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0,0,0))
bpy.ops.mesh.primitive_cube_add(location=(3,0,0))
bpy.ops.mesh.primitive_cone_add(location=(-3,0,0))

bpy.ops.object.light_add(type='SUN', location=(5,5,10))
bpy.context.active_object.data.energy = 5

bpy.ops.object.camera_add(location=(8,-8,5))
cam = bpy.context.active_object
cam.rotation_euler = (1.1, 0, 0.785)
bpy.context.scene.camera = cam

bpy.context.scene.render.filepath = 'blender_render####'
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.resolution_x = 960
bpy.context.scene.render.resolution_y = 540
bpy.ops.render.render(write_still=True)

print("Render concluído!")


# Salvar script temporário
with open("script_render.py", "w") as f:
    f.write(SCRIPT_BLENDER)
    """

# — Passo 2: Chamar Blender em modo headless —
print("Iniciando Blender em modo background...")
# subprocess.run(["blender", "-b", "--python", "script_render.py"])
# (Descomente a linha acima para rodar de verdade)

# Para o lab, criamos uma imagem sintética como se fosse o render
render = np.zeros((540, 960, 3), dtype=np.uint8)
cv2.circle(render, (480, 270), 150, (100, 150, 200), -1)
cv2.rectangle(render, (650, 120), (800, 400), (80, 120, 80), -1)
cv2.imwrite("blender_render0001.png", render)

# — Passo 3: OpenCV pós-processa o render —
img = cv2.imread("blender_render0001.png")

# Adicionar marca d'água
cv2.putText(img, "CG - UNIFG 2026 | Prof. Petros", (20, 520),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200,200,200), 2)

# Realçar bordas (estilo toon shader básico)
cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bordas = cv2.Canny(cinza, 30, 100)
bordas_bgr = cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR)
resultado = cv2.addWeighted(img, 0.85, bordas_bgr, 0.15, 0)

cv2.imwrite("render_processado.png", resultado)
print("Render processado salvo em render_processado.png")