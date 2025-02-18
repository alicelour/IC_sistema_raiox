import os
import pydicom

# 📂 Defina a pasta onde estão os arquivos DICOM
pasta_dicom = r"C:\Users\alice\teste_html\dicom"  # Ajuste para o caminho correto

# 🔍 Percorre todos os arquivos na pasta
for filename in os.listdir(pasta_dicom):
    if filename.lower().endswith('.dcm'):  # Verifica se é um arquivo DICOM
        filepath = os.path.join(pasta_dicom, filename)
        
        try:
            # 📥 Carrega o arquivo DICOM
            ds = pydicom.dcmread(filepath)

            # 📌 Extrai metadados
            nome_paciente = ds.get("PatientName")
            idade = ds.get("PatientAge")  # Exemplo: '070Y' (70 anos)
            sexo = ds.get("PatientSex")   # 'M' ou 'F'
            estudo = ds.get("StudyDescription")
            data_estudo = ds.get("StudyDate")
            
            # 🖨️ Exibe os metadados
            print(f"\n📄 Arquivo: {filename}")
            print(f"👤 Nome: {nome_paciente}")
            print(f"🎂 Idade: {idade}")
            print(f"⚧ Sexo: {sexo}")
            print(f"📝 Estudo: {estudo}")
            print(f"📅 Data do Estudo: {data_estudo}")

        except Exception as e:
            print(f"❌ Erro ao processar {filename}: {e}")

print("\n✅ Extração de metadados concluída!")
