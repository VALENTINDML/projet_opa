import websocket
import json
import time 
from kafka import KafkaProducer

conn = psycopg2.connect(
    dbname="binance_data",
    user="VALDML",
    password="PROJETOPA",  # Remplace ici
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# Connexion à la base PostgreSQL
last_saved_time = 0  # Dernier moment où on a écrit dans le CSV
save_interval = 1   # Intervalle en secondes entre deux sauvegardes
today = datetime.datetime.now().strftime("%Y-%m-%d")
csv_path = Path(f"binance_trades_{today}.csv")

# Créer le fichier CSV avec en-tête s'il n'existe pas
if not csv_path.exists():
    with open(csv_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['symbol', 'price', 'quantity', 'timestamp'])

consumer = KafkaConsumer( 'Binance_trades' , bootstrap_servers = '18.203.161.161:8080/',
value_deserializer= lambda m: json.loads(m).decode('utf-8') , auto_offset_reset= 'latest', 
group_id= 'bianance-consumer')

def insert_trade(data):
    try:
        timestamp = int(data["T"]) / 1000
        formatted_time = datetime.datetime.fromtimestamp(timestamp)
        query = """
            INSERT INTO binance_trades (symbol, price, quantity, timestamp)
            VALUES (%s, %s, %s, %s)
        """
        values = (data["s"], data["p"], data["q"], formatted_time)
        cur.execute(query, values)
        conn.commit()
        print(f"✅ Inséré : {data['s']} à {formatted_time}")
    except Exception as e:
        print(f"❌ Erreur insertion : {e}")
     
    global last_saved_time
    current_time = time.time()
    if current_time - last_saved_time >= save_interval:
        with open(csv_path, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([data["s"], data["p"], data["q"], formatted_time])
        last_saved_time = current_time

for message in consumer:
    data = message.value  # Le message est un dictionnaire après désérialisation
    insert_trade(data)