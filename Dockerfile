# Utiliser une image officielle Python légère
FROM python:3.11-slim

# Installer les outils de compilation nécessaires pour scikit-learn
#RUN apt add --no-cache build-base gcc musl-dev python3-dev

# Définit le dossier de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires pour ton projet dans le conteneur
COPY ./projet_opa /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application dans le conteneur
COPY . .

# Commande pour lancer FastAPI avec uvicorn
#CMD ["uvicorn", "fast_api:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["jupyter notebook --ip=0.0.0.0 --port 8888 --allow-root --no-browser]

CMD ["python3" , "producer.py"]

CMD ["python3" , "consumer.py"]

RUN echo '#!/bin/bash\n\
            uvicorn fast_api:app --host 0.0.0.0 --port 8000 &\n\
            jupyter notebook --ip=0.0.0.0 --port 8888 --allow-root --no-browser' > /start.sh && chmod +x /start.sh

# Exposer le port 8000 (celui sur lequel FastAPI tourne par défaut)
EXPOSE 8000
EXPOSE 8888

# Commande pour démarrer le script
CMD ["/bin/bash","/start.sh"]
