"""
League of Legends Analytics Tracker
Récupère les données depuis l'API Riot Games et sauvegarde les statistiques
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

class LoLTracker:
    def __init__(self, api_key, riot_id, tag):
        """
        Args:
            api_key: Ta clé API Riot Games (https://developer.riotgames.com/)
            riot_id: Ton pseudonyme LoL
            tag: Ton tag (ex: "EUW")
        """
        self.api_key = api_key
        self.riot_id = riot_id
        self.tag = tag
        self.base_url = "https://europe.api.riotgames.com"
        self.regional_url = "https://euw1.api.riotgames.com"
        self.data_file = "lol_stats.json"
        self.load_data()

    def load_data(self):
        """Charge les données existantes ou crée un nouveau fichier"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "player_info": {},
                "matches": [],
                "champion_stats": {},
                "daily_summary": []
            }

    def save_data(self):
        """Sauvegarde les données en JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"✓ Données sauvegardées dans {self.data_file}")

    def get_player_puuid(self):
        """Récupère le PUUID du joueur"""
        try:
            url = f"{self.base_url}/riot/account/v1/accounts/by-riot-id/{self.riot_id}/{self.tag}"
            headers = {"X-Riot-Token": self.api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()['puuid']
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du PUUID: {e}")
            return None

    def get_player_ranked_info(self, summoner_id):
        """Récupère les infos ranked (LP, rank, etc)"""
        try:
            url = f"{self.regional_url}/lol/league/v4/entries/by-summoner/{summoner_id}"
            headers = {"X-Riot-Token": self.api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des infos ranked: {e}")
            return []

    def get_summoner_by_puuid(self, puuid):
        """Récupère l'ID du summoner depuis le PUUID"""
        try:
            url = f"{self.regional_url}/lol/summoner/v4/summoners/by-puuid/{puuid}"
            headers = {"X-Riot-Token": self.api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()['id']
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du summoner ID: {e}")
            return None

    def get_match_history(self, puuid, start=0, count=20):
        """Récupère l'historique des matches"""
        try:
            url = f"{self.base_url}/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
            headers = {"X-Riot-Token": self.api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de l'historique: {e}")
            return []

    def get_match_details(self, match_id):
        """Récupère les détails d'un match"""
        try:
            url = f"{self.base_url}/lol/match/v5/matches/{match_id}"
            headers = {"X-Riot-Token": self.api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du match {match_id}: {e}")
            return None

    def process_matches(self, match_ids, puuid):
        """Traite les matches et extrait les stats pertinentes"""
        for match_id in match_ids:
            # Vérifie si le match est déjà dans la base
            if any(m['match_id'] == match_id for m in self.data['matches']):
                continue

            match_data = self.get_match_details(match_id)
            if not match_data:
                continue

            # Trouve les données du joueur dans le match
            player_stats = None
            for participant in match_data['info']['participants']:
                if participant['puuid'] == puuid:
                    player_stats = participant
                    break

            if player_stats:
                match_info = {
                    'match_id': match_id,
                    'timestamp': datetime.fromtimestamp(match_data['info']['gameEndTimestamp'] / 1000).isoformat(),
                    'duration_seconds': match_data['info']['gameDuration'],
                    'queue_id': match_data['info']['queueId'],
                    'champion': player_stats['championName'],
                    'role': player_stats.get('teamPosition', 'UNKNOWN'),
                    'win': player_stats['win'],
                    'kills': player_stats['kills'],
                    'deaths': player_stats['deaths'],
                    'assists': player_stats['assists'],
                    'cs': player_stats['totalMinionsKilled'],
                    'gold': player_stats['goldEarned'],
                    'damage': player_stats['totalDamageDealtToChampions'],
                    'items': [player_stats.get(f'item{i}', 0) for i in range(7)],
                    'lane_opponent': player_stats.get('opposingTeamSize', 0)
                }

                self.data['matches'].append(match_info)
                self.update_champion_stats(match_info)
                print(f"✓ Match ajouté: {player_stats['championName']} - {'WIN' if player_stats['win'] else 'LOSS'}")

    def update_champion_stats(self, match_info):
        """Met à jour les stats par champion"""
        champion = match_info['champion']

        if champion not in self.data['champion_stats']:
            self.data['champion_stats'][champion] = {
                'games': 0,
                'wins': 0,
                'losses': 0,
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'total_cs': 0,
                'total_gold': 0,
                'total_damage': 0
            }

        stats = self.data['champion_stats'][champion]
        stats['games'] += 1
        stats['wins'] += 1 if match_info['win'] else 0
        stats['losses'] += 0 if match_info['win'] else 1
        stats['kills'] += match_info['kills']
        stats['deaths'] += match_info['deaths']
        stats['assists'] += match_info['assists']
        stats['total_cs'] += match_info['cs']
        stats['total_gold'] += match_info['gold']
        stats['total_damage'] += match_info['damage']

    def generate_summary(self):
        """Génère un résumé des statistiques"""
        if not self.data['matches']:
            print("❌ Aucun match trouvé")
            return

        total_games = len(self.data['matches'])
        wins = sum(1 for m in self.data['matches'] if m['win'])
        wr = (wins / total_games * 100) if total_games > 0 else 0

        print("\n" + "="*50)
        print("📊 STATISTIQUES GLOBALES")
        print("="*50)
        print(f"Total matches: {total_games}")
        print(f"Wins: {wins} | Losses: {total_games - wins}")
        print(f"Win Rate: {wr:.1f}%")
        print(f"\n📈 TOP CHAMPIONS:")

        for champion, stats in sorted(
            self.data['champion_stats'].items(),
            key=lambda x: x[1]['wins'],
            reverse=True
        )[:5]:
            winrate = (stats['wins'] / stats['games'] * 100) if stats['games'] > 0 else 0
            kda = (stats['kills'] + stats['assists']) / max(stats['deaths'], 1)
            print(f"  {champion}: {stats['games']}G | WR {winrate:.1f}% | KDA {kda:.2f}")

    def sync_all(self):
        """Synchronise toutes les données"""
        print("🔄 Synchronisation LoL Stats...")

        # Récupère le PUUID
        puuid = self.get_player_puuid()
        if not puuid:
            print("❌ Impossible de récupérer le PUUID")
            return False

        print(f"✓ PUUID trouvé: {puuid}")

        # Récupère l'historique des matches
        match_ids = self.get_match_history(puuid, start=0, count=20)
        if match_ids:
            print(f"✓ {len(match_ids)} matches trouvés")
            self.process_matches(match_ids, puuid)

        # Sauvegarde les données
        self.save_data()
        self.generate_summary()

        return True

if __name__ == "__main__":
    # Charge la configuration depuis config.json
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)

        API_KEY = config.get('api_key')
        RIOT_ID = config.get('riot_id')
        TAG = config.get('tag')

        if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
            print("❌ Veuillez remplir config.json avec ta clé API, pseudo et tag")
            exit(1)

        print(f"✓ Configuration chargée pour {RIOT_ID}#{TAG}")
        tracker = LoLTracker(API_KEY, RIOT_ID, TAG)
        tracker.sync_all()

    except FileNotFoundError:
        print("❌ Fichier config.json non trouvé!")
        print("Crée un fichier config.json avec la structure suivante:")
        print(json.dumps({
            "api_key": "RGAPI-xxxx-xxxx-xxxx",
            "riot_id": "YourName",
            "tag": "EUW"
        }, indent=2))
        exit(1)
    except json.JSONDecodeError:
        print("❌ config.json invalide (pas du JSON valide)")
        exit(1)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        exit(1)
