# Guide rapide - Controle des LEDs ESP32

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Kicksbld/ESP32_WS.git
cd ESP32_WS
```

### 2. Installer Thonny

Telecharger et installer Thonny : https://thonny.org/

### 3. Configurer Thonny pour l'ESP32

1. Brancher l'ESP32 en USB
2. Ouvrir Thonny
3. Menu **Run** > **Configure interpreter**
4. Selectionner **MicroPython (ESP32)**
5. Selectionner le port USB (ex: `/dev/tty.usbserial-0001` ou `COM3`)
6. Cliquer **OK**

### 4. Uploader les fichiers

1. Dans Thonny, ouvrir chaque fichier `.py` du projet
2. Menu **File** > **Save as...**
3. Choisir **MicroPython device**
4. Garder le meme nom de fichier

Fichiers a uploader :
- `boot.py`
- `main.py`
- `sensor.py`
- `ochestrator.py`
- `Message.py`
- `wsclient.py`
- `ledstrip.py`
- `button.py`
- `joystick.py`
- `lightSensor.py`
- `rfid.py`

### 5. Configurer le WiFi

Modifier `boot.py` ligne 23 avec vos identifiants :

```python
wifi_connect("NOM_WIFI", "MOT_DE_PASSE")
```

### 6. Configurer le serveur WebSocket

Modifier `main.py` ligne 74 avec l'IP du serveur :

```python
ws = WSClient("ws://VOTRE_IP:9000", ...)
```

### 7. Lancer

Appuyer sur le bouton **RST** de l'ESP32 ou cliquer sur **Run** dans Thonny.

---

## Architecture

```
[Client WebSocket] --> [Serveur WS :9000] --> [ESP32 "ESP_Killian"]
```

## Configuration materielle

| Composant | Config |
|-----------|--------|
| LED Strip | 27 LEDs NeoPixel sur pin **13** |
| Serveur WS | `ws://192.168.4.230:9000` |
| Client ESP | `ESP_Killian` |

## Message pour controler une LED

Envoyer ce JSON via WebSocket au serveur :

```json
{
  "message_type": "RECEPTION_SENSOR",
  "data": {
    "emitter": "MonClient",
    "receiver": "ESP_Killian",
    "sensor_id": "LED",
    "value": {
      "led_id": 1,
      "state": "on"
    }
  }
}
```

### Champs value

| Champ | Type | Description |
|-------|------|-------------|
| `led_id` | int (1-27) | Numero de la LED. Omettre pour toutes |
| `state` | string | `"on"` = clignote 3x blanc, `"off"` = eteint |

## Exemples

### Allumer LED n5

```json
{ "led_id": 5, "state": "on" }
```

### Eteindre toutes les LEDs

```json
{ "state": "off" }
```

### Message complet pour allumer toutes les LEDs

```json
{"message_type":"RECEPTION_SENSOR","data":{"emitter":"Test","receiver":"ESP_Killian","sensor_id":"LED","value":{"state":"on"}}}
```

## Test avec wscat

```bash
# Installer wscat
npm install -g wscat

# Se connecter au serveur
wscat -c ws://192.168.4.230:9000

# Envoyer la commande (copier sur une seule ligne)
{"message_type":"RECEPTION_SENSOR","data":{"emitter":"Test","receiver":"ESP_Killian","sensor_id":"LED","value":{"led_id":1,"state":"on"}}}
```

## Test au demarrage

L'ESP32 fait automatiquement un test LED au boot :
1. Rouge
2. Vert
3. Bleu
4. Off

Si tu vois ce cycle, les LEDs fonctionnent correctement.

## Fichiers cles

| Fichier | Role |
|---------|------|
| [main.py](main.py) | Point d'entree, gestion WebSocket et callbacks |
| [ledStrip.py](ledStrip.py) | Classe LedStrip (fill, set, off, red, green, blue) |
| [Message.py](Message.py) | Format des messages WebSocket |
| [standard.json](standard.json) | Schema JSON des messages |
