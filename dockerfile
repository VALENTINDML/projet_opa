# Utiliser une image officielle Python légère
FROM python:3.11-alpine

# Installer les outils de compilation nécessaires pour scikit-learn
RUN apk add --no-cache build-base gcc musl-dev python3-dev

# Définit le dossier de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application dans le conteneur
COPY . .

# Exposer le port 8000 (celui sur lequel FastAPI tourne par défaut)
EXPOSE 8000
EXPOSE 8888

# Commande pour lancer FastAPI avec uvicorn
CMD ["uvicorn", "fast_api:app", "--host", "0.0.0.0", "--port", "8000" & "jupyter notebook --ip=0.0.0.0 --port 8888 --allow-root --no-browser]
