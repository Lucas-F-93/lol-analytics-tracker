# 🎮 League of Legends Analytics Tracker

Une solution complète pour tracker tes performances LoL avec un script Python + dashboard web interactif.

## 📋 Contenu

- **`lol_tracker.py`** - Script Python pour récupérer les données via l'API Riot Games
- **`dashboard.html`** - Dashboard web interactif avec graphiques et statistiques
- **`README.md`** - Ce fichier

---

## 🚀 Installation & Configuration

### Étape 1: Obtenir ta clé API Riot Games

1. Va sur https://developer.riotgames.com/
2. Connecte-toi avec ton compte Riot
3. Crée une nouvelle application dans "Applications"
4. Copie ta **API Key** (valable 24h en développement)
5. Note ton **Riot ID** (pseudonyme#tag)

> **Important**: La clé API gratuite dure 24h et permet ~100 requêtes/minute. C'est largement suffisant pour tracker tes perfs.

### Étape 2: Installer les dépendances Python

```bash
pip install requests
```

### Étape 3: Configurer le script

Ouvre `lol_tracker.py` et remplis les valeurs (ligne ~170-173):

```python
API_KEY = "RGAPI-xxxx-xxxx-xxxx-xxxx"  # Ta clé API
RIOT_ID = "MonPseudo"                   # Ton pseudo LoL
TAG = "EUW"                              # Ton tag (EUW, NA, KR, etc.)
```

Trouve ton tag ici: https://www.leagueoflegends.com/profile/

---

## 🔄 Utilisation

### Option 1: Automatique (Recommandé)

**Première synchronisation:**
```bash
python lol_tracker.py
```

Cela va:
- ✓ Récupérer ton historique des 20 derniers matchs
- ✓ Extraire les stats détaillées
- ✓ Créer `lol_stats.json` avec toutes les données
- ✓ Afficher un résumé

**Utiliser le dashboard:**
1. Ouvre `dashboard.html` dans ton navigateur
2. Clique sur "Charger les données"
3. Sélectionne `lol_stats.json`
4. Profite des graphiques et stats! 📊

### Option 2: Tracking Manuel

Si tu préfères tracker manuellement:
1. Télécharge le template `lol_stats.json` depuis le dashboard
2. Ajoute tes matchs manuellement en remplissant les champs
3. Recharge dans le dashboard

---

## 📊 Données Tracées

### Globales
- Total de matchs
- Win Rate (%)
- KDA moyen
- CS moyen

### Par Champion
- Nombre de matchs
- Win Rate individuel
- KDA
- Stats (kills, deaths, assists, gold, damage)

### Graphiques
- Evolution du WR au fil des matchs
- Win Rate par champion
- KDA par champion
- Distribution des jeux (pie chart)

### Historique
- Liste des 50 derniers matchs
- Champion joué
- KDA
- CS
- Résultat (WIN/LOSS)

---

## 🔧 Troubleshooting

### ❌ "Erreur lors de la récupération du PUUID"

**Solutions:**
1. Vérifie que ta clé API est correcte et valide (< 24h)
2. Vérifie ton RIOT_ID et TAG (sensible à la casse)
3. Essaie de réattendre 1 minute (rate limit)

### ❌ "Aucun match trouvé"

**Solutions:**
1. Tu dois avoir au moins 1 match rangé (pas les normals)
2. Essaie avec `count=50` au lieu de 20 dans la fonction

### ❌ Le dashboard ne charge pas les données

**Solutions:**
1. Vérifie que c'est bien du JSON valide
2. Le fichier doit avoir la structure correcte (voir template)
3. Utilise le bouton "Télécharger template" pour avoir le bon format

---

## 💡 Idées d'Améliorations

- [ ] Script de scheduling (mise à jour automatique chaque jour)
- [ ] Bot Discord pour les notifications
- [ ] Tracking des tendances (meilleur/pire champion)
- [ ] Analyse des lanes et matchups
- [ ] Export CSV pour tableur
- [ ] Prédictions basées sur l'IA
- [ ] Comparaison avec d'autres joueurs

---

## ⚙️ Configuration Avancée

### Augmenter le nombre de matchs tracés

Dans `lol_tracker.py`, ligne ~158:
```python
match_ids = self.get_match_history(puuid, start=0, count=50)  # Augmente 50
```

### Tracker d'autres queues (ARAM, Flex, etc)

Les queues sont filtrées par `queue_id` dans l'API Riot. Tu peux ajouter du filtering dans `process_matches()`.

### Automatiser la synchronisation

Utilise le task scheduler de ton OS ou un cron job:

**Windows (PowerShell):**
```powershell
$action = New-ScheduledTaskAction -Execute 'python' -Argument 'C:\path\to\lol_tracker.py'
$trigger = New-ScheduledTaskTrigger -Daily -At 10:00AM
Register-ScheduledTask -TaskName "LoL_Sync" -Action $action -Trigger $trigger
```

**Linux/Mac (crontab):**
```bash
0 10 * * * cd /path/to/project && python lol_tracker.py
```

---

## 📝 Licence & Disclaimer

- L'API Riot Games est fournie gratuitement pour un usage personnel
- Respecte les termes de service de Riot Games
- Cet outil n'est pas affilié à Riot Games

---

## 🤝 Support

Des questions? Besoin d'améliorations?

1. Vérifie les errors du script (ils sont assez explicites)
2. Consulte la doc de l'API Riot: https://developer.riotgames.com/docs
3. Teste avec un autre compte si tu soupçonnes un bug

---

**Bonne chance et GG!** ⚔️
