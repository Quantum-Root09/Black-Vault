import requests
import os
import sys
import time
import random
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import get_close_matches

# Color definitions - green for running, red for errors, white for everything else
GREEN = "\033[92m"
RED = "\033[91m"
WHITE = "\033[97m"
RESET = "\033[0m"

def print_status(text, is_running=False, is_error=False):
    """Print text - green for running, red for errors, white for everything else"""
    if is_error:
        print(f"{RED}{text}{RESET}")
    elif is_running:
        print(f"{GREEN}{text}{RESET}")
    else:
        print(f"{WHITE}{text}{RESET}")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    banner = f"""
{WHITE}
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║       🔍  USERNAME SEARCH TOOL v1.0  🔍              ║
    ║                                                      ║
    ║          Advanced Username Intelligence              ║
    ║                                                      ║
    ║           {RED}Made By Quantumroot09{RESET}                      ║
    ╚══════════════════════════════════════════════════════╝
{RESET}
    """
    print(banner)

def username_search_simple():
    """Original username search function - unchanged"""
    clear_screen()
    
    print(f"\n{WHITE}{'═'*60}{RESET}")
    print(f"{WHITE}🔍 BASIC USERNAME SEARCH{RESET}".center(60))
    print(f"{WHITE}{'═'*60}{RESET}\n")

    usuario = input(f"{WHITE}[~] Enter username: {RESET}").strip()

    if not usuario:
        print_status("[!] Username cannot be empty.", is_error=True)
        input(f"\n{WHITE}Press Enter to continue...{RESET}")
        return

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    sites = {
        "GitHub": f"https://github.com/{usuario}",
        "Instagram": f"https://www.instagram.com/{usuario}",
        "facebook": f"https://www.facebook.com/{usuario}",
        "YouTube": f"https://www.youtube.com/{usuario}",
        "ChatGPT": f"https://chat.openai.com/{usuario}",
        "Wikipedia": f"https://en.wikipedia.org/{usuario}",
        "X (Twitter)": f"https://twitter.com/{usuario}",
        "Reddit": f"https://www.reddit.com/user/{usuario}",
        "Pinterest": f"https://www.pinterest.com/{usuario}",
        "Twitch": f"https://www.twitch.tv/{usuario}",
        "Telegram": f"https://t.me/{usuario}",
        "tiktok": f"https://www.tiktok.com/{usuario}",
        "yahoo": f"https://profiles.yahoo.com/u/{usuario}",
        "amazon": f"https://www.amazon.com/{usuario}",
        "linkedin": f"https://www.linkedin.com/{usuario}",
        "flipkart": f"https://www.flipkart.com/{usuario}",
        "hotstar": f"https://www.hotstar.com/{usuario}",
        "moneycontrol": f"https://www.moneycontrol.com/{usuario}",
        "bing": f"https://www.bing.com/{usuario}",
        "indiatimes": f"https://www.indiatimes.com/{usuario}",
        "netflix": f"https://www.netflix.com/{usuario}",
        "cricbuzz": f"https://www.cricbuzz.com/{usuario}",
        "GitLab": f"https://gitlab.com/{usuario}",
        "CodeWars": f"https://www.codewars.com/users/{usuario}",
        "Replit": f"https://replit.com/{usuario}",
        "Xbox Gamertag": f"https://xboxgamertag.com/search/{usuario}",
        "Spotify": f"https://open.spotify.com/user/{usuario}",
        "Snapchat": f"https://www.snapchat.com/add/{usuario}",
        "Quora": f"https://www.quora.com/profile/{usuario}",
        "Medium": f"https://medium.com/@{usuario}",
        "Dev.to": f"https://dev.to/{usuario}",
        "StackOverflow": f"https://stackoverflow.com/users/{usuario}",
        "HackerRank": f"https://www.hackerrank.com/{usuario}",
        "LeetCode": f"https://leetcode.com/{usuario}",
        "CodeChef": f"https://www.codechef.com/users/{usuario}",
        "GeeksforGeeks": f"https://auth.geeksforgeeks.org/user/{usuario}",
        "Kaggle": f"https://www.kaggle.com/{usuario}",
        "Behance": f"https://www.behance.net/{usuario}",
        "Dribbble": f"https://dribbble.com/{usuario}",
        "Flickr": f"https://www.flickr.com/people/{usuario}",
        "Vimeo": f"https://vimeo.com/{usuario}",
        "SoundCloud": f"https://soundcloud.com/{usuario}",
        "Bandcamp": f"https://bandcamp.com/{usuario}",
        "Steam": f"https://steamcommunity.com/id/{usuario}",
        "Epic Games": f"https://www.epicgames.com/id/{usuario}",
        "Roblox": f"https://www.roblox.com/user.aspx?username={usuario}",
        "Discord": f"https://discord.com/users/{usuario}",
        "Mastodon": f"https://mastodon.social/@{usuario}",
        "Threads": f"https://www.threads.net/@{usuario}",
        "Product Hunt": f"https://www.producthunt.com/@{usuario}",
        "Goodreads": f"https://www.goodreads.com/{usuario}",
        "Letterboxd": f"https://letterboxd.com/{usuario}",
        "IMDb": f"https://www.imdb.com/user/{usuario}",
        "Tripadvisor": f"https://www.tripadvisor.com/members/{usuario}",
        "Booking.com": f"https://www.booking.com/profile/{usuario}",
        "Airbnb": f"https://www.airbnb.com/users/show/{usuario}",
        "Paytm": f"https://paytm.com/{usuario}",
        "PhonePe": f"https://www.phonepe.com/{usuario}",
        "Zomato": f"https://www.zomato.com/users/{usuario}",
        "Swiggy": f"https://www.swiggy.com/user/{usuario}",
        "Myntra": f"https://www.myntra.com/{usuario}",
        "Meesho": f"https://www.meesho.com/{usuario}",
        "Ajio": f"https://www.ajio.com/{usuario}",
        "Nykaa": f"https://www.nykaa.com/{usuario}",
        "OLX": f"https://www.olx.in/profile/{usuario}",
        "ShareChat": f"https://sharechat.com/profile/{usuario}",
        "Moj": f"https://mojapp.in/@{usuario}",
        "Josh": f"https://share.myjosh.in/profile/{usuario}",
        "Koo": f"https://www.kooapp.com/profile/{usuario}",
        "Dailyhunt": f"https://profile.dailyhunt.in/{usuario}",
        "Truecaller": f"https://www.truecaller.com/search/in/{usuario}",
        "ResearchGate": f"https://www.researchgate.net/profile/{usuario}",
        "Academia": f"https://independent.academia.edu/{usuario}",
        "Giters": f"https://giters.com/{usuario}",
        "Hashnode": f"https://hashnode.com/@{usuario}",
        "BuyMeACoffee": f"https://www.buymeacoffee.com/{usuario}",
        "Patreon": f"https://www.patreon.com/{usuario}",
    }

    print()

    found_count = 0
    for name, url in sites.items():
        try:
            r = requests.get(
                url,
                headers=headers,
                timeout=8,
                allow_redirects=True
            )

            if r.status_code == 200:
                print_status(f"[✔] Found on {name:<12} -> {url}", is_running=False)
                found_count += 1
            else:
                print_status(f"[✘] Not Found on {name:<12}", is_error=True)

        except Exception:
            print_status(f"[!] Error checking {name}", is_error=True)

    print(f"\n{WHITE}[📊] Total found: {found_count}/{len(sites)}{RESET}")
    print()
    input(f"{WHITE}Press Enter to continue...{RESET}")

def extract_name_parts(username):
    """Intelligently split a username into possible name components."""
    import re
    parts = re.split(r'[_.\-\d]+', username)
    parts = [p.lower() for p in parts if len(p) >= 2]

    if len(parts) == 1 and len(parts[0]) >= 6:
        word = parts[0]
        candidates = []
        for i in range(3, len(word) - 2):
            left, right = word[:i], word[i:]
            if 3 <= len(left) <= 9 and 3 <= len(right) <= 9:
                candidates.append((left, right))
        if candidates:
            mid = candidates[len(candidates) // 2]
            parts = list(mid)

    return parts

def fetch_usernames_from_github(query, limit=150):
    """Search GitHub public API for real users matching the query."""
    results = set()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/vnd.github.v3+json"
    }
    pages = [1, 2, 3]
    for page in pages:
        try:
            url = f"https://api.github.com/search/users?q={query}&per_page=50&page={page}"
            r = requests.get(url, headers=headers, timeout=8)
            if r.status_code == 200:
                data = r.json()
                for user in data.get('items', []):
                    login = user.get('login', '').lower()
                    if login:
                        results.add(login)
            elif r.status_code == 403:
                break
            time.sleep(0.5)
        except Exception:
            pass
    return list(results)[:limit]

def fetch_usernames_from_wikipedia(name_part, limit=60):
    """Search Wikipedia for people with this name to extract realistic name combos."""
    results = set()
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        url = (f"https://en.wikipedia.org/w/api.php?action=query&list=search"
               f"&srsearch={name_part}&srnamespace=0&srlimit=50&format=json")
        r = requests.get(url, headers=headers, timeout=8)
        if r.status_code == 200:
            data = r.json()
            for item in data.get('query', {}).get('search', []):
                title = item.get('title', '')
                clean = title.split('(')[0].strip().lower()
                words = clean.split()
                if 2 <= len(words) <= 3:
                    first = words[0]
                    last = words[-1]
                    results.add(f"{first}{last}")
                    results.add(f"{first}_{last}")
                    results.add(f"{first}.{last}")
                    results.add(f"{last}{first}")
                    results.add(f"{last}_{first}")
                    if len(words) == 3:
                        mid = words[1]
                        results.add(f"{first}{mid}{last}")
                        results.add(f"{first}_{mid}_{last}")
    except Exception:
        pass
    return list(results)[:limit]

def build_instagram_style_variations(base_username, name_parts):
    """Build Instagram-realistic username variations."""
    variations = set()
    variations.add(base_username)

    identity_prefixes = [
        'its', 'im', 'iam', 'real', 'official', 'the', 'mr', 'ms', 'mrs',
        'miss', 'hey', 'yo', 'hi', 'iamthe', 'thisis', 'justcall', 'callme',
        'only', 'xo', 'xox', 'not', 'lil', 'big', 'little', 'young',
    ]

    identity_suffixes = [
        'official', 'real', 'original', 'gram', 'insta', 'ig', 'here',
        'daily', 'world', 'life', 'vibes', 'tv', 'yt', 'official_',
        'xo', 'xox', 'only', 'fan', 'fans', 'lover',
    ]

    birth_years = [
        '90', '91', '92', '93', '94', '95', '96', '97', '98', '99',
        '00', '01', '02', '03', '04', '05', '06', '07', '08',
        '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005'
    ]

    surnames = [
        'patel', 'sharma', 'verma', 'gupta', 'kumar', 'singh', 'reddy', 'rao',
        'yadav', 'jha', 'thakur', 'mishra', 'pandey', 'dubey', 'mehta',
        'shah', 'jain', 'agarwal', 'sethi', 'malhotra', 'chopra', 'kapoor',
        'patil', 'joshi', 'kulkarni', 'deshmukh', 'gaikwad', 'wagh',
        'khan', 'ali', 'ansari', 'qureshi', 'shaikh', 'siddiqui',
        'nair', 'menon', 'pillai', 'iyer', 'iyengar', 'krishnan',
        'das', 'dey', 'ghosh', 'banerjee', 'mukherjee', 'chatterjee',
        'smith', 'jones', 'williams', 'brown', 'johnson', 'wilson',
        'lee', 'kim', 'park', 'choi', 'ahmed', 'hussain', 'malik',
    ]

    for part in name_parts:
        variations.add(part)
        for surname in surnames[:25]:
            if part != surname:
                variations.add(f"{part}{surname}")
                variations.add(f"{part}_{surname}")
                variations.add(f"{part}.{surname}")
                variations.add(f"{surname}{part}")
                variations.add(f"{surname}_{part}")
        for prefix in identity_prefixes:
            variations.add(f"{prefix}{part}")
            variations.add(f"{prefix}_{part}")
        for suffix in identity_suffixes:
            variations.add(f"{part}{suffix}")
            variations.add(f"{part}_{suffix}")
        for year in birth_years:
            variations.add(f"{part}{year}")
            variations.add(f"{part}_{year}")

    for surname in surnames[:30]:
        variations.add(f"{base_username}{surname}")
        variations.add(f"{base_username}_{surname}")
        variations.add(f"{base_username}.{surname}")
        variations.add(f"{surname}{base_username}")
        variations.add(f"{surname}_{base_username}")

    for prefix in identity_prefixes:
        variations.add(f"{prefix}{base_username}")
        variations.add(f"{prefix}_{base_username}")

    for suffix in identity_suffixes:
        variations.add(f"{base_username}{suffix}")
        variations.add(f"{base_username}_{suffix}")
        variations.add(f"{base_username}.{suffix}")

    for year in birth_years:
        variations.add(f"{base_username}{year}")
        variations.add(f"{base_username}_{year}")

    for num in list(range(0, 10)) + [11, 21, 22, 23, 24, 25, 99, 100, 786, 420, 111, 7]:
        variations.add(f"{base_username}{num}")
        variations.add(f"{base_username}_{num}")

    if len(name_parts) >= 2:
        a, b = name_parts[0], name_parts[1]
        variations.add(f"{a}{b}")
        variations.add(f"{a}_{b}")
        variations.add(f"{a}.{b}")
        variations.add(f"{b}{a}")
        variations.add(f"{b}_{a}")
        for year in birth_years[:10]:
            variations.add(f"{a}{b}{year}")
            variations.add(f"{a}_{b}_{year}")
        for suffix in identity_suffixes[:8]:
            variations.add(f"{a}{b}{suffix}")
            variations.add(f"{a}_{b}_{suffix}")

    cleaned = set()
    for v in variations:
        v = v.strip('._-')
        if 3 <= len(v) <= 30 and v.replace('_', '').replace('.', '').isalnum():
            cleaned.add(v.lower())

    return cleaned

def fetch_real_usernames_from_web(base_username, platform_name):
    """Deep Instagram username discovery engine."""
    discovered_usernames = set()

    print_status(f"[🌐] Extracting name components from '{base_username}'...", is_running=True)
    name_parts = extract_name_parts(base_username)
    if name_parts:
        print(f"{WHITE}[ℹ] Detected name parts: {', '.join(name_parts)}{RESET}")

    print_status(f"[🔍] Querying GitHub public API for real users like '{base_username}'...", is_running=True)
    github_users = fetch_usernames_from_github(base_username, limit=150)
    discovered_usernames.update(github_users)

    for part in name_parts:
        if part != base_username:
            part_users = fetch_usernames_from_github(part, limit=80)
            discovered_usernames.update(part_users)

    print(f"{WHITE}[✓] GitHub API: found {len(github_users)} real usernames{RESET}")

    print_status(f"[🔍] Mining Wikipedia for real people named '{base_username}'...", is_running=True)
    wiki_users = fetch_usernames_from_wikipedia(base_username)
    discovered_usernames.update(wiki_users)

    for part in name_parts:
        wiki_part = fetch_usernames_from_wikipedia(part)
        discovered_usernames.update(wiki_part)

    print(f"{WHITE}[✓] Wikipedia: mined {len(wiki_users)} name-based usernames{RESET}")

    print_status(f"[⚙] Building smart Instagram-style name variations...", is_running=True)
    smart_variations = build_instagram_style_variations(base_username, name_parts)
    discovered_usernames.update(smart_variations)
    print(f"{WHITE}[✓] Generated {len(smart_variations)} intelligent variations{RESET}")

    relevant = set()
    search_tokens = [base_username] + name_parts
    for uname in discovered_usernames:
        if uname and 3 <= len(uname) <= 30:
            for token in search_tokens:
                if token in uname or uname in token or get_close_matches(uname, [token], n=1, cutoff=0.7):
                    relevant.add(uname)
                    break

    if len(relevant) < 50:
        relevant = discovered_usernames

    result_list = list(relevant)
    random.shuffle(result_list)

    total = len(result_list)
    print(f"{WHITE}[📊] Total unique candidates to verify: {total}{RESET}")

    return result_list

def check_username_on_platform(username, platform_url, platform_name, headers):
    """Check if a username exists on a specific platform"""
    try:
        url = platform_url.format(username)
        r = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        if r.status_code == 200:
            return platform_name, username, url, True
        return platform_name, username, url, False
    except:
        return platform_name, username, url, False

def detailed_username_search():
    """Advanced deep username search using real public APIs + smart name intelligence"""
    clear_screen()
    print_banner()
    
    platforms = {
         "1": {"name": "Instagram", "url": "https://www.instagram.com/{}"},
         "2": {"name": "Facebook", "url": "https://www.facebook.com/{}"},
         "3": {"name": "Reddit", "url": "https://www.reddit.com/user/{}"},
         "4": {"name": "Twitter (X)", "url": "https://twitter.com/{}"},
         "5": {"name": "GitHub", "url": "https://github.com/{}"},
         "6": {"name": "TikTok", "url": "https://www.tiktok.com/@{}"},
         "7": {"name": "YouTube", "url": "https://www.youtube.com/@{}"},
         "8": {"name": "Twitch", "url": "https://www.twitch.tv/{}"},
         "9": {"name": "Telegram", "url": "https://t.me/{}"},
        "10": {"name": "Pinterest", "url": "https://www.pinterest.com/{}"},
        "11": {"name": "Spotify", "url": "https://open.spotify.com/user/{}"},
        "12": {"name": "Snapchat", "url": "https://www.snapchat.com/add/{}"},
        "13": {"name": "LinkedIn", "url": "https://www.linkedin.com/in/{}"},
        "14": {"name": "LeetCode", "url": "https://leetcode.com/{}"},
        "15": {"name": "CodeWars", "url": "https://www.codewars.com/users/{}"},
        "16": {"name": "Replit", "url": "https://replit.com/{}"},
        "17": {"name": "Xbox Gamertag", "url": "https://xboxgamertag.com/search/{}"},
        "18": {"name": "Threads", "url": "https://www.threads.net/@{}"},
        "19": {"name": "Mastodon", "url": "https://mastodon.social/@{}"},
        "20": {"name": "Product Hunt", "url": "https://www.producthunt.com/@{}"},
        "30": {"name": "Goodreads", "url": "https://www.goodreads.com/{}"},
        "31": {"name": "Letterboxd", "url": "https://letterboxd.com/{}"},
        "32": {"name": "IMDb", "url": "https://www.imdb.com/user/{}"},
        "33": {"name": "Tripadvisor", "url": "https://www.tripadvisor.com/members/{}"},
        "34": {"name": "Booking.com", "url": "https://www.booking.com/profile/{}"},
        "35": {"name": "Airbnb", "url": "https://www.airbnb.com/users/show/{}"},
        "36": {"name": "Paytm", "url": "https://paytm.com/{}"},
        "37": {"name": "PhonePe", "url": "https://www.phonepe.com/{}"},
        "38": {"name": "Zomato", "url": "https://www.zomato.com/users/{}"},
        "39": {"name": "Swiggy", "url": "https://www.swiggy.com/user/{}"},
        "40": {"name": "Myntra", "url": "https://www.myntra.com/{}"},
        "41": {"name": "Meesho", "url": "https://www.meesho.com/{}"},
        "42": {"name": "Ajio", "url": "https://www.ajio.com/{}"},
        "43": {"name": "Nykaa", "url": "https://www.nykaa.com/{}"},
        "44": {"name": "OLX", "url": "https://www.olx.in/profile/{}"},
        "45": {"name": "ShareChat", "url": "https://sharechat.com/profile/{}"},
        "46": {"name": "Moj", "url": "https://mojapp.in/@{}"},
        "47": {"name": "Josh", "url": "https://share.myjosh.in/profile/{}"},
        "48": {"name": "Koo", "url": "https://www.kooapp.com/profile/{}"},
        "49": {"name": "Dailyhunt", "url": "https://profile.dailyhunt.in/{}"},
        "50": {"name": "Truecaller", "url": "https://www.truecaller.com/search/in/{}"},
        "51": {"name": "ResearchGate", "url": "https://www.researchgate.net/profile/{}"},
        "52": {"name": "Academia", "url": "https://independent.academia.edu/{}"},
        "53": {"name": "Giters", "url": "https://giters.com/{}"},
        "54": {"name": "Hashnode", "url": "https://hashnode.com/@{}"},
        "55": {"name": "BuyMeACoffee", "url": "https://www.buymeacoffee.com/{}"},
        "56": {"name": "Patreon", "url": "https://www.patreon.com/{}"},
        "57": {"name": "Dev.to", "url": "https://dev.to/{}"},
        "58": {"name": "StackOverflow", "url": "https://stackoverflow.com/users/{}"},
        "59": {"name": "HackerRank", "url": "https://www.hackerrank.com/{}"},
        "60": {"name": "LeetCode", "url": "https://leetcode.com/{}"},
        "61": {"name": "CodeChef", "url": "https://www.codechef.com/users/{}"},
        "62": {"name": "GeeksforGeeks", "url": "https://auth.geeksforgeeks.org/user/{}"},
        "63": {"name": "Kaggle", "url": "https://www.kaggle.com/{}"},
        "64": {"name": "flipkart", "url": "https://www.flipkart.com/{}"}
    }

    print(f"\n{WHITE}┌────────────────────────────────────────────┐{RESET}")
    print(f"{WHITE}│        SELECT SOCIAL PLATFORM              │{RESET}")
    print(f"{WHITE}└────────────────────────────────────────────┘{RESET}\n")
    
    for key, platform in list(platforms.items())[:64]:
        print(f"  {WHITE}[{key}]{RESET} {platform['name']}")
    
    print(f"\n  {WHITE}[0]{RESET} Back to Main Menu")
    
    choice = input(f"\n{WHITE}[➜] Select platform: {RESET}").strip()
    
    if choice == "0":
        return
    elif choice not in platforms:
        print_status("[!] Invalid choice!", is_error=True)
        time.sleep(1)
        return
    
    selected = platforms[choice]
    
    print(f"\n{WHITE}{'─'*50}{RESET}")
    base_username = input(f"{WHITE}[➜] Enter base username for {selected['name']}: {RESET}").strip().lower()
    
    if not base_username:
        print_status("[!] Username cannot be empty!", is_error=True)
        time.sleep(1)
        return
    
    print(f"\n{WHITE}╔══════════════════════════════════════════════════╗{RESET}")
    print(f"{WHITE}║     🕵️  DEEP USERNAME SEARCH ENGINE STARTING     ║{RESET}")
    print(f"{WHITE}╚══════════════════════════════════════════════════╝{RESET}")
    print_status("[ℹ] Phase 1 → GitHub public API (real registered users)", is_running=True)
    print_status("[ℹ] Phase 2 → Wikipedia name mining (real people's names)", is_running=True)
    print_status("[ℹ] Phase 3 → Smart Instagram-style variation engine", is_running=True)
    print_status(f"[ℹ] Phase 4 → Live verification on {selected['name']}", is_running=True)
    print_status("[⏳] This may take 30–90 seconds. Please wait...", is_running=True)
    print()

    similar_usernames = fetch_real_usernames_from_web(base_username, selected['name'])
    similar_usernames = list(set(similar_usernames))
    
    print(f"{WHITE}[✓] Discovered {len(similar_usernames)} potential usernames from internet sources{RESET}")
    print_status(f"[🔍] Checking availability on {selected['name']}...", is_running=True)
    print()
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    found_usernames = []
    total = len(similar_usernames)
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = {
            executor.submit(
                check_username_on_platform, 
                username, 
                selected['url'], 
                selected['name'], 
                headers
            ): username for username in similar_usernames
        }
        
        for i, future in enumerate(as_completed(futures), 1):
            platform_name, username, url, exists = future.result()
            
            progress = int((i / total) * 50)
            bar = "█" * progress + "░" * (50 - progress)
            print(f"\r{GREEN}[{bar}] {i}/{total}{RESET}", end="", flush=True)
            
            if exists:
                found_usernames.append((username, url))
    
    print(f"\n\n{WHITE}{'='*60}{RESET}")
    print(f"{WHITE}📊 RESULTS FOR {selected['name'].upper()}{RESET}")
    print(f"{WHITE}{'='*60}{RESET}\n")
    
    actual_found = len(found_usernames)
    
    if actual_found > 0:
        print(f"{WHITE}[📊] ({actual_found}) usernames found on {selected['name']}{RESET}\n")
        
        try:
            requested_limit = int(input(f"{WHITE}[➜] How many usernames to display? (1-{actual_found}): {RESET}").strip())
            if requested_limit < 1:
                requested_limit = actual_found
            elif requested_limit > actual_found:
                requested_limit = actual_found
        except ValueError:
            requested_limit = actual_found
            print_status("[!] Invalid input, showing all results", is_error=True)
        
        print()
        display_list = found_usernames[:requested_limit]
        print(f"{WHITE}[✓] Showing {requested_limit} of {actual_found} registered usernames found{RESET}\n")
        
        for idx, (username, url) in enumerate(display_list, 1):
            if username == base_username or username == f"{base_username}_official":
                print(f"  {WHITE}{idx:3}.{RESET} {WHITE}{username:<35}{RESET} → {WHITE}{url}{RESET}")
            else:
                print(f"  {WHITE}{idx:3}.{RESET} {username:<35} → {WHITE}{url}{RESET}")
        
        save_choice = input(f"\n{WHITE}[💾] Save results to file? (y/n): {RESET}").strip().lower()
        if save_choice == 'y':
            filename = f"{selected['name']}_{base_username}_results.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Username search results for {selected['name']}\n")
                f.write(f"Base username: {base_username}\n")
                f.write(f"Found: {actual_found} usernames\n")
                f.write(f"Displayed: {len(display_list)}\n\n")
                for username, url in display_list:
                    f.write(f"{username} -> {url}\n")
            print(f"{WHITE}[✓] Saved to {filename}{RESET}")
    
    else:
        print_status(f"[✗] No active accounts found on {selected['name']} for any discovered usernames.", is_error=True)
        print_status(f"[ℹ] Try a different username or platform. {selected['name']} may be rate-limiting requests.", is_error=True)
    print(f"\n{WHITE}{'─'*50}{RESET}")
    back_choice = input(f"{WHITE}[⬅] Press Enter to go back to menu...{RESET}")
    return

# ==================== SHERLOCK-STYLE SEARCH (OPTION 3) ====================

# Full Sherlock Sites Dictionary
SHERLOCK_SITES = {
    # Social Media
    "Instagram": "https://www.instagram.com/{}",
    "Facebook": "https://www.facebook.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Tumblr": "https://{}.tumblr.com",
    "Mastodon": "https://mastodon.social/@{}",
    "Threads": "https://www.threads.net/@{}",
    "Telegram": "https://t.me/{}",
    "WhatsApp": "https://wa.me/{}",
    "Signal": "https://signal.me/#p/{}",
    
    # Developer Platforms
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "BitBucket": "https://bitbucket.org/{}",
    "LeetCode": "https://leetcode.com/{}",
    "CodeWars": "https://www.codewars.com/users/{}",
    "HackerRank": "https://www.hackerrank.com/{}",
    "CodeChef": "https://www.codechef.com/users/{}",
    "GeeksforGeeks": "https://auth.geeksforgeeks.org/user/{}",
    "Kaggle": "https://www.kaggle.com/{}",
    "Replit": "https://replit.com/@{}",
    "StackOverflow": "https://stackoverflow.com/users/{}",
    "Dev.to": "https://dev.to/{}",
    "Hashnode": "https://hashnode.com/@{}",
    "Medium": "https://medium.com/@{}",
    "Quora": "https://www.quora.com/profile/{}",
    
    # Gaming
    "Steam": "https://steamcommunity.com/id/{}",
    "Xbox": "https://xboxgamertag.com/search/{}",
    "PlayStation": "https://psnprofiles.com/{}",
    "Nintendo": "https://nintendo.com/users/{}",
    "EpicGames": "https://www.epicgames.com/id/{}",
    "Roblox": "https://www.roblox.com/user.aspx?username={}",
    "Chess.com": "https://www.chess.com/member/{}",
    "Lichess": "https://lichess.org/@/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Discord": "https://discord.com/users/{}",
    
    # Creative/Portfolio
    "Behance": "https://www.behance.net/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Flickr": "https://www.flickr.com/people/{}",
    "500px": "https://500px.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Bandcamp": "https://bandcamp.com/{}",
    "Vimeo": "https://vimeo.com/{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "ArtStation": "https://www.artstation.com/{}",
    
    # Professional/Academic
    "ResearchGate": "https://www.researchgate.net/profile/{}",
    "Academia": "https://independent.academia.edu/{}",
    "GoogleScholar": "https://scholar.google.com/citations?user={}",
    "AngelList": "https://angel.co/u/{}",
    
    # Blogging/Writing
    "WordPress": "https://{}.wordpress.com",
    "Blogger": "https://{}.blogspot.com",
    "Substack": "https://{}.substack.com",
    "Ghost": "https://{}.ghost.io",
    "Wix": "https://{}.wixsite.com/home",
    
    # Dating
    "Tinder": "https://tinder.com/@{}",
    "Bumble": "https://bumble.com/profile/{}",
    
    # Shopping/Reviews
    "Amazon": "https://www.amazon.com/gp/profile/{}",
    "Ebay": "https://www.ebay.com/usr/{}",
    "Etsy": "https://www.etsy.com/people/{}",
    "Goodreads": "https://www.goodreads.com/{}",
    "IMDb": "https://www.imdb.com/user/{}",
    "Tripadvisor": "https://www.tripadvisor.com/members/{}",
    "Yelp": "https://www.yelp.com/user_details?userid={}",
    
    # Coding/Technical (continued)
    "PyPI": "https://pypi.org/user/{}",
    "NPM": "https://www.npmjs.com/~{}",
    "RubyGems": "https://rubygems.org/profiles/{}",
    "Crates.io": "https://crates.io/users/{}",
    "DockerHub": "https://hub.docker.com/u/{}",
    "Figma": "https://www.figma.com/@{}",
    "Codepen": "https://codepen.io/{}",
    "JSFiddle": "https://jsfiddle.net/user/{}",
    "Glitch": "https://glitch.com/@{}",
    
    # Forums/Communities
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "ProductHunt": "https://www.producthunt.com/@{}",
    "Keybase": "https://keybase.io/{}",
    "About.me": "https://about.me/{}",
    "Imgur": "https://imgur.com/user/{}",
    "Pastebin": "https://pastebin.com/u/{}",
    "Disqus": "https://disqus.com/by/{}",
    "Gravatar": "https://en.gravatar.com/{}",
    
    # Indian Platforms
    "ShareChat": "https://sharechat.com/profile/{}",
    "Moj": "https://mojapp.in/@{}",
    "Josh": "https://share.myjosh.in/profile/{}",
    "Koo": "https://www.kooapp.com/profile/{}",
    "Dailyhunt": "https://profile.dailyhunt.in/{}",
    "Flipkart": "https://www.flipkart.com/profile/{}",
    "Paytm": "https://paytm.com/profile/{}",
    "PhonePe": "https://www.phonepe.com/{}",
    "Zomato": "https://www.zomato.com/users/{}",
    "Swiggy": "https://www.swiggy.com/user/{}",
    "Myntra": "https://www.myntra.com/{}",
    "Meesho": "https://www.meesho.com/{}",
    "OLX": "https://www.olx.in/profile/{}",
    "Truecaller": "https://www.truecaller.com/search/in/{}",
    
    # Other
    "Wikipedia": "https://en.wikipedia.org/wiki/User:{}",
    "Wikia": "https://community.fandom.com/wiki/User:{}",
    "Giters": "https://giters.com/{}",
    "BuyMeACoffee": "https://www.buymeacoffee.com/{}",
    "Patreon": "https://www.patreon.com/{}",
    "Last.fm": "https://www.last.fm/user/{}",
    "MyAnimeList": "https://myanimelist.net/profile/{}",
    "Trello": "https://trello.com/{}",
    "Pocket": "https://getpocket.com/@{}",
}

def check_sherlock_site(site_name, url, username, headers, timeout, proxies=None):
    """Check a single site for username existence"""
    try:
        if proxies:
            r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True, proxies=proxies)
        else:
            r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        
        # Different platforms have different indicators of existence
        if r.status_code == 200:
            # Additional check for false positives (some sites return 200 for non-existent users)
            content = r.text.lower()
            
            # False positive patterns
            false_positives = [
                "page not found", "doesn't exist", "user not found", 
                "not found", "404", "no user found", "invalid user",
                "could not find", "sorry, no posts", "this account doesn't exist",
                "profile not found", "user does not exist", "account not found"
            ]
            
            for fp in false_positives:
                if fp in content:
                    return site_name, False, url
            
            return site_name, True, url
        elif r.status_code == 404:
            return site_name, False, url
        else:
            # Other status codes might indicate rate limiting or other issues
            return site_name, False, url
    except requests.exceptions.Timeout:
        return site_name, False, url
    except requests.exceptions.ConnectionError:
        return site_name, False, url
    except Exception:
        return site_name, False, url

def sherlock_bulk_search():
    """Sherlock-style bulk username search across multiple platforms"""
    clear_screen()
    print_banner()
    
    print(f"\n{WHITE}{'═'*60}{RESET}")
    print(f"{WHITE}🔎 SHERLOCK-STYLE BULK USERNAME SEARCH{RESET}".center(60))
    print(f"{WHITE}{'═'*60}{RESET}\n")
    
    # Get username(s) from user
    print(f"{WHITE}[📝] Enter usernames to search (separate multiple with commas or spaces){RESET}")
    print(f"{WHITE}[ℹ] Example: john_doe, jsmith, alice2024{RESET}\n")
    
    username_input = input(f"{WHITE}[➜] Username(s): {RESET}").strip()
    
    if not username_input:
        print_status("[!] Username cannot be empty!", is_error=True)
        time.sleep(1)
        return
    
    # Parse multiple usernames
    usernames = []
    # Split by comma first, then by space
    if ',' in username_input:
        usernames = [u.strip().lower() for u in username_input.split(',') if u.strip()]
    else:
        usernames = [u.strip().lower() for u in username_input.split() if u.strip()]
    
    # Filter out empty strings
    usernames = [u for u in usernames if u]
    
    if not usernames:
        print_status("[!] No valid usernames provided!", is_error=True)
        time.sleep(1)
        return
    
    # Ask for search depth
    print(f"\n{WHITE}[⚙] SEARCH CONFIGURATION{RESET}")
    print(f"{WHITE}{'─'*50}{RESET}")
    print(f"{WHITE}[1] Quick search (faster, fewer sites ~100){RESET}")
    print(f"{WHITE}[2] Standard search (recommended, ~150 sites){RESET}")
    print(f"{WHITE}[3] Deep search (slower, ~250+ sites){RESET}")
    
    depth_choice = input(f"\n{WHITE}[➜] Select search depth (1-3) [default: 2]: {RESET}").strip()
    
    if depth_choice == "1":
        # Quick search: use a subset of sites
        sites_to_check = dict(list(SHERLOCK_SITES.items())[:100])
        print_status(f"[⚡] Quick mode: checking ~{len(sites_to_check)} platforms", is_running=True)
    elif depth_choice == "3":
        sites_to_check = SHERLOCK_SITES.copy()
        print_status(f"[🐌] Deep mode: checking all {len(sites_to_check)} platforms", is_running=True)
    else:
        # Standard: use about 150 sites
        sites_to_check = dict(list(SHERLOCK_SITES.items())[:150])
        print_status(f"[✓] Standard mode: checking ~{len(sites_to_check)} platforms", is_running=True)
    
    # Timeout configuration
    timeout_choice = input(f"\n{WHITE}[➜] Request timeout in seconds (1-15) [default: 5]: {RESET}").strip()
    try:
        timeout = int(timeout_choice)
        if timeout < 1:
            timeout = 5
        elif timeout > 15:
            timeout = 15
    except:
        timeout = 5
    
    # Ask for proxy support (optional)
    use_proxy = input(f"\n{WHITE}[➜] Use proxy? (y/n) [default: n]: {RESET}").strip().lower()
    proxies = None
    if use_proxy == 'y':
        proxy_input = input(f"{WHITE}[➜] Enter proxy (e.g., http://127.0.0.1:8080): {RESET}").strip()
        if proxy_input:
            proxies = {
                'http': proxy_input,
                'https': proxy_input
            }
            print_status("[✓] Proxy configured", is_running=True)
    
    # Start search
    print(f"\n{WHITE}{'='*60}{RESET}")
    print(f"{WHITE}🔍 STARTING BULK SEARCH FOR {len(usernames)} USERNAME(S){RESET}")
    print(f"{WHITE}{'='*60}{RESET}\n")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    all_results = {}
    
    for username in usernames:
        print(f"\n{WHITE}[🎯] SEARCHING: {username}{RESET}")
        print(f"{WHITE}{'─'*50}{RESET}")
        
        found_sites = []
        total = len(sites_to_check)
        
        # Use threading for faster checking
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {}
            for site_name, url_template in sites_to_check.items():
                url = url_template.format(username)
                future = executor.submit(
                    check_sherlock_site,
                    site_name,
                    url,
                    username,
                    headers,
                    timeout,
                    proxies
                )
                futures[future] = site_name
            
            completed = 0
            for future in as_completed(futures):
                completed += 1
                site_name, found, url = future.result()
                
                # Progress indicator
                progress = int((completed / total) * 40)
                bar = "█" * progress + "░" * (40 - progress)
                print(f"\r{GREEN}[{bar}] {completed}/{total} sites checked{RESET}", end="", flush=True)
                
                if found:
                    found_sites.append((site_name, url))
        
        print(f"\n")  # New line after progress bar
        
        # Store results
        all_results[username] = found_sites
        
        # Display results for this username
        if found_sites:
            print_status(f"[✓] FOUND {len(found_sites)} PROFILE(S):", is_running=False)
            print()
            for idx, (site_name, url) in enumerate(found_sites, 1):
                print(f"  {WHITE}{idx:3}.{RESET} {site_name:<20} → {WHITE}{url}{RESET}")
        else:
            print_status(f"[✗] No profiles found for '{username}' on any platform", is_error=True)
        
        print(f"\n{WHITE}{'─'*50}{RESET}")
        
        # Small delay between usernames to avoid rate limiting
        if len(usernames) > 1 and username != usernames[-1]:
            print_status("[⏳] Waiting 2 seconds before next search...", is_running=True)
            time.sleep(2)
    
    # Summary
    print(f"\n{WHITE}{'='*60}{RESET}")
    print(f"{WHITE}📊 SEARCH SUMMARY{RESET}")
    print(f"{WHITE}{'='*60}{RESET}\n")
    
    total_found = sum(len(results) for results in all_results.values())
    
    for username, results in all_results.items():
        if results:
            print(f"  {WHITE}✓{RESET} {username}: {len(results)} profiles found")
        else:
            print_status(f"  ✗ {username}: 0 profiles found", is_error=True)
    
    print(f"\n{WHITE}[📈] TOTAL: {total_found} profiles across {len(usernames)} username(s){RESET}")
    
    # Save results to file
    save_choice = input(f"\n{WHITE}[💾] Save all results to file? (y/n): {RESET}").strip().lower()
    if save_choice == 'y':
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"sherlock_results_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("SHERLOCK-STYLE USERNAME SEARCH RESULTS\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Usernames searched: {', '.join(usernames)}\n")
            f.write(f"{'='*80}\n\n")
            
            for username, results in all_results.items():
                f.write(f"USERNAME: {username}\n")
                f.write(f"{'-'*40}\n")
                if results:
                    f.write(f"Found {len(results)} profiles:\n\n")
                    for idx, (site_name, url) in enumerate(results, 1):
                        f.write(f"  {idx}. {site_name}\n")
                        f.write(f"     URL: {url}\n\n")
                else:
                    f.write("No profiles found.\n\n")
                f.write(f"{'='*80}\n\n")
        
        print(f"{WHITE}[✓] Results saved to: {filename}{RESET}")
        
        # Also save as JSON option
        json_choice = input(f"\n{WHITE}[💾] Also save as JSON? (y/n): {RESET}").strip().lower()
        if json_choice == 'y':
            json_filename = f"sherlock_results_{timestamp}.json"
            json_data = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "usernames": usernames,
                "results": {
                    username: [
                        {"platform": site_name, "url": url}
                        for site_name, url in results
                    ]
                    for username, results in all_results.items()
                }
            }
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2)
            print(f"{WHITE}[✓] JSON results saved to: {json_filename}{RESET}")
    
    print(f"\n{WHITE}{'─'*50}{RESET}")
    input(f"{WHITE}[⬅] Press Enter to return to main menu...{RESET}")

def sherlock_bulk_search_multiple():
    """Alternative: Search multiple usernames from a file"""
    clear_screen()
    print_banner()
    
    print(f"\n{WHITE}{'═'*60}{RESET}")
    print(f"{WHITE}📁 BULK SEARCH FROM FILE{RESET}".center(60))
    print(f"{WHITE}{'═'*60}{RESET}\n")
    
    print(f"{WHITE}[ℹ] This option reads usernames from a text file (one per line){RESET}")
    print(f"{WHITE}[ℹ] Example file format:{RESET}")
    print(f"  {WHITE}john_doe{RESET}")
    print(f"  {WHITE}jsmith123{RESET}")
    print(f"  {WHITE}alice2024{RESET}\n")
    
    filename = input(f"{WHITE}[➜] Enter username file path: {RESET}").strip()
    
    if not filename:
        print_status("[!] No filename provided!", is_error=True)
        time.sleep(1)
        return
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            usernames = [line.strip().lower() for line in f if line.strip()]
        
        if not usernames:
            print_status("[!] No usernames found in file!", is_error=True)
            time.sleep(1)
            return
        
        print(f"{WHITE}[✓] Loaded {len(usernames)} username(s) from {filename}{RESET}")
        
        # Ask for confirmation
        print(f"\n{WHITE}First 10 usernames: {', '.join(usernames[:10])}{RESET}")
        if len(usernames) > 10:
            print(f"{WHITE}... and {len(usernames) - 10} more{RESET}")
        
        confirm = input(f"\n{WHITE}[➜] Start bulk search? (y/n): {RESET}").strip().lower()
        if confirm != 'y':
            print_status("[!] Search cancelled.", is_error=True)
            time.sleep(1)
            return
        
        # Search depth selection
        print(f"\n{WHITE}[⚙] SEARCH CONFIGURATION{RESET}")
        print(f"{WHITE}{'─'*50}{RESET}")
        print(f"{WHITE}[1] Quick search (faster){RESET}")
        print(f"{WHITE}[2] Standard search (recommended){RESET}")
        print(f"{WHITE}[3] Deep search (slower, more thorough){RESET}")
        
        depth_choice = input(f"\n{WHITE}[➜] Select search depth (1-3) [default: 2]: {RESET}").strip()
        
        if depth_choice == "1":
            sites_to_check = dict(list(SHERLOCK_SITES.items())[:100])
            print_status(f"[⚡] Quick mode: checking ~{len(sites_to_check)} platforms", is_running=True)
        elif depth_choice == "3":
            sites_to_check = SHERLOCK_SITES.copy()
            print_status(f"[🐌] Deep mode: checking all {len(sites_to_check)} platforms", is_running=True)
        else:
            sites_to_check = dict(list(SHERLOCK_SITES.items())[:150])
            print_status(f"[✓] Standard mode: checking ~{len(sites_to_check)} platforms", is_running=True)
        
        timeout = 5
        timeout_choice = input(f"\n{WHITE}[➜] Request timeout (1-15) [default: 5]: {RESET}").strip()
        try:
            timeout = int(timeout_choice)
            if timeout < 1:
                timeout = 5
            elif timeout > 15:
                timeout = 15
        except:
            timeout = 5
        
        headers = {"User-Agent": "Mozilla/5.0"}
        
        all_results = {}
        
        for idx, username in enumerate(usernames, 1):
            print(f"\n\n{WHITE}{'='*60}{RESET}")
            print(f"{WHITE}[{idx}/{len(usernames)}] SEARCHING: {username}{RESET}")
            print(f"{WHITE}{'='*60}{RESET}")
            
            found_sites = []
            total = len(sites_to_check)
            
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = {}
                for site_name, url_template in sites_to_check.items():
                    url = url_template.format(username)
                    future = executor.submit(
                        check_sherlock_site,
                        site_name,
                        url,
                        username,
                        headers,
                        timeout
                    )
                    futures[future] = site_name
                
                completed = 0
                for future in as_completed(futures):
                    completed += 1
                    site_name, found, url = future.result()
                    
                    progress = int((completed / total) * 40)
                    bar = "█" * progress + "░" * (40 - progress)
                    print(f"\r{GREEN}[{bar}] {completed}/{total}{RESET}", end="", flush=True)
                    
                    if found:
                        found_sites.append((site_name, url))
            
            print(f"\n")
            all_results[username] = found_sites
            
            if found_sites:
                print_status(f"[✓] Found {len(found_sites)} profile(s):", is_running=False)
                for site_name, url in found_sites[:10]:  # Show first 10
                    print(f"     → {site_name}: {WHITE}{url}{RESET}")
                if len(found_sites) > 10:
                    print(f"{WHITE}     ... and {len(found_sites) - 10} more{RESET}")
            else:
                print_status(f"[✗] No profiles found", is_error=True)
            
            # Delay between searches
            if idx < len(usernames):
                print_status(f"[⏳] Waiting 2 seconds before next search...", is_running=True)
                time.sleep(2)
        
        # Save all results
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"bulk_sherlock_results_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("BULK SHERLOCK-STYLE USERNAME SEARCH RESULTS\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total usernames searched: {len(usernames)}\n")
            f.write(f"Source file: {filename}\n")
            f.write(f"{'='*80}\n\n")
            
            total_profiles = 0
            for username, results in all_results.items():
                total_profiles += len(results)
                f.write(f"USERNAME: {username}\n")
                f.write(f"{'-'*40}\n")
                if results:
                    f.write(f"Found {len(results)} profiles:\n\n")
                    for site_name, url in results:
                        f.write(f"  • {site_name}\n")
                        f.write(f"    {url}\n\n")
                else:
                    f.write("  No profiles found.\n\n")
                f.write(f"{'='*80}\n\n")
            
            f.write(f"\nSUMMARY:\n")
            f.write(f"  Total usernames: {len(usernames)}\n")
            f.write(f"  Total profiles found: {total_profiles}\n")
            f.write(f"  Average profiles per username: {total_profiles/len(usernames):.2f}\n")
        
        print(f"\n\n{WHITE}[✓] Results saved to: {filename}{RESET}")
        print(f"{WHITE}[📊] Total profiles found: {total_profiles}{RESET}")
        
    except FileNotFoundError:
        print_status(f"[!] File not found: {filename}", is_error=True)
    except Exception as e:
        print_status(f"[!] Error reading file: {e}", is_error=True)
    
    print(f"\n{WHITE}{'─'*50}{RESET}")
    input(f"{WHITE}[⬅] Press Enter to return to main menu...{RESET}")

def sherlock_menu():
    """Submenu for Sherlock-style searches"""
    while True:
        clear_screen()
        print_banner()
        
        print(f"\n{WHITE}┌────────────────────────────────────────────┐{RESET}")
        print(f"{WHITE}│         SHERLOCK-STYLE SEARCH MENU         │{RESET}")
        print(f"{WHITE}└────────────────────────────────────────────┘{RESET}\n")
        
        print(f"  {WHITE}[1]{RESET} 🔎 Search Single Username")
        print(f"  {WHITE}[2]{RESET} 📝 Search Multiple Usernames (Manual Entry)")
        print(f"  {WHITE}[3]{RESET} 📁 Search Multiple Usernames (From File)")
        print(f"  {WHITE}[0]{RESET} ⬅️ Back to Main Menu")
        
        print(f"\n{WHITE}{'─'*50}{RESET}")
        choice = input(f"\n{WHITE}[➜] Enter your choice: {RESET}").strip()
        
        if choice == "1":
            # Single username search
            sherlock_bulk_search()
        elif choice == "2":
            # Multiple usernames manual entry
            sherlock_bulk_search()
        elif choice == "3":
            # From file
            sherlock_bulk_search_multiple()
        elif choice == "0":
            return
        else:
            print_status("[!] Invalid choice!", is_error=True)
            time.sleep(1)

def main_menu():
    while True:
        clear_screen()
        print_banner()
        
        print(f"\n{WHITE}┌────────────────────────────────────────────┐{RESET}")
        print(f"{WHITE}│               MAIN MENU                    │{RESET}")
        print(f"{WHITE}└────────────────────────────────────────────┘{RESET}\n")
        
        print(f"  {WHITE}[1]{RESET} 🔍 Basic Username Search")
        print(f"  {WHITE}[2]{RESET} 🎯 Advanced Username Search (Internet Discovery)")
        print(f"  {WHITE}[3]{RESET} 🔎 Sherlock-Style Bulk Username Search")
        print(f"  {WHITE}[0]{RESET} 🚪 Exit")
        
        print(f"\n{WHITE}{'─'*50}{RESET}")
        choice = input(f"\n{WHITE}[➜] Enter your choice: {RESET}").strip()
        
        if choice == "1":
            username_search_simple()
        elif choice == "2":
            detailed_username_search()
        elif choice == "3":
            sherlock_menu()
        elif choice == "0":
            print(f"\n{WHITE}Thanks for using, Leaving no footprints..!{RESET}")
            print(f"{WHITE}Exiting...{RESET}\n")
            sys.exit(0)
        else:
            print_status("[!] Invalid choice! Please try again.", is_error=True)
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Interrupted by user{RESET}")
        sys.exit(0)
    except Exception as e:
        print_status(f"[!] Error: {e}", is_error=True)
        sys.exit(1)
        
def run():
    print_banner()
    main_menu()