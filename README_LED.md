# Guide rapide - Controle des LEDs ESP32

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
