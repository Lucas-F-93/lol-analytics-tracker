# 🚀 Setup - League of Legends Analytics

## ✅ Étapes de Configuration

### 1️⃣ Complète config.json

Ouvre `config.json` et remplis tes infos:

```json
{
  "api_key": "RGAPI-7e3258b6-efa4-4164-93a0-8a1a98e06678",
  "riot_id": "TonPseudo",    ← Change "YourName" par ton pseudo LoL
  "tag": "EUW"               ← Ton tag (EUW, NA, KR, etc.)
}
```

**Où trouver ton tag?**
- Va sur https://www.leagueoflegends.com/profile/
- Ton profil affiche: `PseudoLoL#TAG`

**Exemple:**
```json
{
  "api_key": "RGAPI-7e3258b6-efa4-4164-93a0-8a1a98e06678",
  "riot_id": "Doublelift",
  "tag": "NA1"
}
```

---

### 2️⃣ Lance le script Python

```bash
python lol_tracker.py
```

**Ça va:**
- ✓ Charger ta config
- ✓ Récupérer tes 20 derniers matchs rangés
- ✓ Créer `lol_stats.json` avec les données
- ✓ Afficher un résumé

**Résultat attendu:**
```
✓ Configuration chargée pour Doublelift#NA1
🔄 Synchronisation LoL Stats...
✓ PUUID trouvé: xxx-xxx-xxx
✓ 20 matches trouvés
✓ Match ajouté: Vayne - WIN
✓ Match ajouté: Kai'Sa - LOSS
...
✓ Données sauvegardées dans lol_stats.json
```

---

### 3️⃣ Ouvre le Dashboard

1. **Double-clique** sur `dashboard.html` (ou fais clic droit → Ouvrir avec → Navigateur)
2. Clique sur **"Charger les données"**
3. Sélectionne **`lol_stats.json`**
4. Profite de tes stats! 📊

---

## 🔄 Mise à Jour de la Clé API

⚠️ **La clé API gratuite expire toutes les 24h!**

### Chaque jour:
1. Va sur https://developer.riotgames.com/
2. Génère une **nouvelle clé API**
3. Remplace la valeur dans `config.json`
4. Relance: `python lol_tracker.py`

### Ou demande une Production Key (permanente):
- Sur le même site, demande une "Production API Key"
- C'est gratuit mais faut attendre la validation Riot
- Une fois validée, elle n'expire jamais ✓

---

## ✨ C'est bon!

Tes fichiers:
- ✓ `config.json` - Ta configuration personnelle
- ✓ `lol_tracker.py` - Script de synchronisation
- ✓ `dashboard.html` - Interface web
- ✓ `lol_stats.json` - Créé après le premier lancement

**Prochaines fois:** 
```bash
python lol_tracker.py  # Met à jour les stats
# Puis ouvre dashboard.html pour voir les graphiques
```

---

**Des questions?** Consulte `README.md` pour plus de détails!

**Good luck et GG!** 🎮⚔️
