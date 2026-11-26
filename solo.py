# -*- coding: utf-8 -*-
# ═════════════════════════════════════════════════════════════════════════════
#  🇧🇩🇮🇳  SAADXBATA — IND + BD UNIFIED SQUAD & AUTO GUILD BOT  🇧🇩🇮🇳
#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     👑 Credit     : SAADXBATA
#     🌏 Regions    : IND + BD Unified Support
#     🎮 Features   : Auto Squad + Auto Guild Join + Smart Movement + Health API
#     ⚡ Edition    : IND + BD GLORY EDITION v6.0
#     📅 Build      : 2026
#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import sys, os, json, time, uuid, random, asyncio, base64, struct, socket
import itertools, traceback, ssl, hmac, hashlib, string, re, subprocess, math
import urllib.parse, urllib.request, urllib.error
import httpx
import aiohttp
import aiohttp.web
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    from google_play_scraper import app as play_scraper
except Exception:
    play_scraper = None

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

try:
    from protobuf_decoder.protobuf_decoder import Parser
except Exception:
    Parser = None

try:
    from message_ids import MESSAGE_ID_TO_NAME
except Exception:
    MESSAGE_ID_TO_NAME = {}

try:
    import thunderFF_pb2
except Exception:
    thunderFF_pb2 = None

try:
    import CguFF_pb2
    _HAS_CGU = True
except Exception:
    _HAS_CGU = False

try:
    import StartMatch_pb2
except Exception:
    StartMatch_pb2 = None

try:
    import reqClan_pb2
    _CLAN_PB_AVAILABLE = True
except Exception:
    _CLAN_PB_AVAILABLE = False

try:
    import requests as _requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except Exception:
    _requests = None

# ═══════════════════════════ CREDIT & BRANDING ═══════════════════════════
CREDIT_NAME     = "SAADXBATA"
BRAND_NAME      = "SAADXBATA"
BRAND_TITLE     = "SAADXBATA — IND + BD AUTO SQUAD & GUILD BOT"
BRAND_VERSION   = "IND+BD GLORY v6.0"
BRAND_YEAR      = "2026"
BRAND_TAGLINE   = "⚡ IND + BD Unified Squad + Auto Guild Join Bot • Credit: SAADXBATA ⚡"

# ═══════════════════════════ GLOBAL CONFIG (IND + BD) ═══════════════════════════
SUPPORTED_REGIONS = ["IND", "BD"]
DEFAULT_REGION = str(os.environ.get("BOT_REGION") or "BD").strip().upper()
if DEFAULT_REGION not in SUPPORTED_REGIONS:
    DEFAULT_REGION = "BD"

WEB_HOST = "0.0.0.0"
WEB_PORT = int(os.environ.get("SERVER_PORT") or os.environ.get("PORT") or "8086")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACCOUNTS_FILE = os.path.join(BASE_DIR, "accounts.json")
TOKEN_CACHE_FILE = os.path.join(BASE_DIR, "token_cache.json")
DEVICES_FILE = os.path.join(BASE_DIR, "devices.json")
NETWORK_REFERENCE_FILE = os.path.join(BASE_DIR, "network_capture_reference.json")

TOKEN_CACHE_TTL = 86400 * 7
NEW_MATCH_DELAY = 4.0
MAX_MATCH_DURATION = 1500
MATCH_IDLE_TIMEOUT = 120.0
START_MATCH_INTERVAL = 8.0
EXP_REFRESH_INTERVAL = 45.0
EXP_REFRESH_AFTER_MATCH_DELAY = 8.0
NON_MATCH_RECONNECT_DELAY = 1.5

NO_MATCH_RESTART_ENABLED = True
NO_MATCH_RESTART_TIMEOUT = 10800.0
NO_MATCH_RESTART_GRACE = 999999.0

BR_MODE_ID = 1
BR_MAP_ID = 1

ANTI_AFK_MIN_INTERVAL = 5.0
ANTI_AFK_MAX_INTERVAL = 9.0

MATCH_SEARCH_TIMEOUT = 90.0
MATCH_WATCHDOG_CHECK = 30.0
MAX_SEARCH_ATTEMPTS = 25

SAFE_PLAY_MODE = True
BYPASS_TIMING_JITTER = True
BYPASS_PACKET_JITTER = True
BYPASS_HELLO_DELAY = True
BYPASS_KA_JITTER = True

ENABLE_SPEED_MOVEMENT = True
MOVEMENT_SPEED_MIN = 0.96
MOVEMENT_SPEED_MAX = 1.15
MOVEMENT_PATTERN = "circle"
MOVEMENT_TICK_MS = 220
MOVEMENT_RADIUS = 180
MOVEMENT_UPDATE_SPEED_EVERY = 4.0

MOVEMENT_STATE_IDLE_CHANCE = 0.10
MOVEMENT_STATE_WALK_CHANCE = 0.28
MOVEMENT_STATE_RUN_CHANCE = 0.32
MOVEMENT_STATE_SPRINT_CHANCE = 0.10
MOVEMENT_STATE_JUMP_CHANCE = 0.08
MOVEMENT_STATE_CROUCH_CHANCE = 0.06
MOVEMENT_STATE_PRONE_CHANCE = 0.06

PLAYER_STATE_MAP = {"idle": 0, "walk": 1, "run": 1, "sprint": 1, "jump": 2, "crouch": 3, "prone": 4}
MOVE_STATE_MAP = {"idle": 0, "walk": 1, "run": 2, "sprint": 3, "jump": 4, "crouch": 1, "prone": 1}

ENABLE_HTTP_PING = True
PING_INTERVAL = 20.0
PING_TIMEOUT = 8.0
PING_URL = "https://loginbp.ppmainecoonghj.com/Ping"
PING_REAL_IP = "103.109.214.211"

# ═══════════════════════════ SQUAD & GUILD AUTO-JOIN CONFIG ═══════════════════════════
TEAM_MODE = True
TEAM_SIZE = 4
TEAM_READY_DELAY = 3.0
TEAM_CREATE_WAIT = 2.0
TEAM_INVITE_CYCLE_WAIT = 2.0
TEAM_INVITE_MAX_TIME = 60.0
TEAM_HEARTBEAT_INTERVAL = 2.5
TEAM_IDLE_ITERS_TEAM = 1800
TEAM_MEMBER_START_DELAY = 12.0
TEAM_FINAL_WAIT = 4.0
_accept_friend_request = True
DEBUG_ALL_PACKETS = False

# Auto Guild Join (Supports both Web Guild API for BD/General and RequestJoinClan Protobuf for IND/Clan)
AUTO_JOIN_GUILD_ENABLED = True
AUTO_JOIN_GUILD_BEFORE_MATCH = True
DEFAULT_GUILD_ID = str(os.environ.get("DEFAULT_GUILD_ID") or "").strip()
DEFAULT_CLAN_ID = str(os.environ.get("DEFAULT_CLAN_ID") or "3106357440").strip()
GUILD_BASE = "https://danger-guild-management-web.vercel.app"
GUILD_JOIN_ENDPOINTS = [f"{GUILD_BASE}/join"]
GUILD_LEAVE_ENDPOINTS = [
    f"{GUILD_BASE}/leave", f"{GUILD_BASE}/guild/leave",
    f"{GUILD_BASE}/quit", f"{GUILD_BASE}/guild/quit", f"{GUILD_BASE}/exit",
]
GUILD_UA = "Mozilla/5.0 (Linux; Android 10) CDX_SHANTO/6.0"
GUILD_TAG = "SAADXBATA"

JWT_API_ENDPOINTS = [
    ("AGS COMMUNITY JWT API", "https://ags-community-jwt-api.vercel.app/token"),
]
FRIEND_URLS_BY_REGION = {
    "BD": [
        "https://client.bd.freefiremobile.com/RequestAddingFriend",
        "https://clientbp.ggblueshark.com/RequestAddingFriend",
    ],
    "IND": [
        "https://clientbp.freefireind.in/RequestAddingFriend",
        "https://clientbp.ggblueshark.com/RequestAddingFriend",
    ],
}
FRIEND_AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
FRIEND_AES_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
FRIEND_HEADERS = {
    "User-Agent": "UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
    "X-GA": "v1 1",
    "ReleaseVersion": "OB55",
    "Content-Type": "application/octet-stream",
    "X-Unity-Version": "2022.3.47f1",
    "Connection": "Keep-Alive",
}

AES_KEY = b"Yg&tc%DEuh6%Zc^8"
AES_IV = b"6oyZDr22E3ychjM%"
HEX_KEY = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
API_KEY = HEX_KEY.encode()

REGION_LANG = {
    "BD": "en",
    "IND": "hi",
}

def normalize_region(region: Optional[str]) -> str:
    reg = str(region or DEFAULT_REGION).strip().upper()
    if reg in ("IN", "INDIA"):
        return "IND"
    if reg in ("BGD", "BANGLADESH"):
        return "BD"
    return reg if reg in SUPPORTED_REGIONS else DEFAULT_REGION

def get_server_code_for_region(region: str) -> str:
    reg = normalize_region(region)
    return "IDC3" if reg == "IND" else "BDC3"

def get_region_api_base(region: str) -> str:
    reg = normalize_region(region)
    if reg == "IND":
        return "https://clientbp.freefireind.in"
    return "https://client.bd.freefiremobile.com"

def get_tcp_prefix(region: str, typ: str = "OnLine") -> str:
    reg = normalize_region(region)
    if typ == "OnLine":
        return "7114" if reg == "IND" else "7119"
    return "9214" if reg == "IND" else "9219"

def get_keepalive_bytes(region: str) -> bytes:
    reg = normalize_region(region)
    return bytes.fromhex("0214" if reg == "IND" else "0219")

def get_br_prefix(region: str) -> str:
    reg = normalize_region(region)
    return "031400" if reg == "IND" else "031900"

def get_team_prefix(region: str) -> str:
    reg = normalize_region(region)
    return "0514" if reg == "IND" else "0515"

# ═══════════════════════════ NETWORK REFERENCE LOADER ═══════════════════════════
def load_network_reference():
    try:
        with open(NETWORK_REFERENCE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        endpoints = data.get("endpoints", [])
        domains = sorted({
            str(item.get("domain", "")).strip()
            for item in endpoints
            if isinstance(item, dict) and item.get("domain")
        })
        protocols = sorted({
            str(item.get("protocol", "")).strip().upper()
            for item in endpoints
            if isinstance(item, dict) and item.get("protocol")
        })
        return {
            "loaded": True,
            "record_count": int(data.get("record_count", 0) or 0),
            "package_name": data.get("package_name", []),
            "domains": domains,
            "protocols": protocols,
            "endpoint_count": len(endpoints),
            "note": str(data.get("note", "")),
        }
    except FileNotFoundError:
        return {"loaded": False, "reason": "network_capture_reference.json not found"}
    except Exception as exc:
        return {"loaded": False, "reason": f"invalid network reference: {exc}"}

NETWORK_REFERENCE = load_network_reference()

# ═══════════════════════════ CONSOLE COLORS & BANNER ═══════════════════════════
class Colors:
    GREEN = "\033[92m"
    FAIL = "\033[91m"
    WARNING = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    ENDC = "\033[0m"
    BRAND = "\033[38;5;208m"
    BDRED = "\033[38;5;196m"
    BDGREEN = "\033[38;5;46m"
    IND_SAFFRON = "\033[38;5;208m"
    IND_BLUE = "\033[38;5;33m"
    GOLD = "\033[38;5;220m"
    PURPLE = "\033[38;5;93m"
    PINK = "\033[38;5;213m"
    SKY = "\033[38;5;51m"
    DIM = "\033[2m"
    BOLD = "\033[1m"

def print_colored(t, c=Colors.WHITE):
    try:
        print(f"{c}{t}{Colors.ENDC}", flush=True)
    except Exception:
        pass

def print_banner():
    banner = f"""
{Colors.BDRED}╔══════════════════════════════════════════════════════════════════════════╗
{Colors.BDRED}║{Colors.GOLD}   ██████╗██████╗ ██╗  ██╗    ███████╗██╗  ██╗ █████╗ ███╗   ██╗████████╗{Colors.BDRED}  ║
{Colors.BDRED}║{Colors.GOLD}  ██╔════╝██╔══██╗╚██╗██╔╝    ██╔════╝██║  ██║██╔══██╗████╗  ██║╚══██╔══╝{Colors.BDRED}  ║
{Colors.BDRED}║{Colors.BDGREEN}  ██║     ██║  ██║ ╚███╔╝     ███████╗███████║███████║██╔██╗ ██║   ██║   {Colors.BDRED}  ║
{Colors.BDRED}║{Colors.BDGREEN}  ██║     ██║  ██║ ██╔██╗     ╚════██║██╔══██║██╔══██║██║╚██╗██║   ██║   {Colors.BDRED}  ║
{Colors.BDRED}║{Colors.IND_SAFFRON}  ╚██████╗██████╔╝██╔╝ ██╗    ███████║██║  ██║██║  ██║██║ ╚████║   ██║   {Colors.BDRED}  ║
{Colors.BDRED}║{Colors.IND_SAFFRON}   ╚═════╝╚═════╝ ╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   {Colors.BDRED}  ║
{Colors.BDRED}╚══════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}
{Colors.GOLD}       👑  {Colors.BOLD}Credit: {CREDIT_NAME}{Colors.ENDC}  {Colors.SKY}|{Colors.ENDC}  {Colors.BOLD}{BRAND_VERSION}{Colors.ENDC}  {Colors.SKY}|{Colors.ENDC}  {Colors.BOLD}© {BRAND_YEAR}{Colors.ENDC}       {Colors.GOLD}👑{Colors.ENDC}
{Colors.BDGREEN}       🇧🇩 Bangladesh (BD)  +  🇮🇳 India (IND) Unified Squad & Guild Bot       {Colors.ENDC}
{Colors.PINK}               {BRAND_TAGLINE}{Colors.ENDC}
{Colors.DIM}       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}
{Colors.GOLD}   🌈 {Colors.BDRED}S{Colors.GOLD}A{Colors.BDGREEN}A{Colors.SKY}D{Colors.PINK} 🌈{Colors.ENDC}
"""
    try:
        print(banner, flush=True)
    except Exception:
        pass

# ═══════════════════════════ BOT STATE ═══════════════════════════
class BotState:
    def __init__(self):
        self.accounts: Dict[str, dict] = {}
        self.account_workers: Dict[str, asyncio.Task] = {}
        self.account_credentials: Dict[str, dict] = {}
        self.auth_to_game_id: Dict[str, str] = {}
        self.game_to_auth_id: Dict[str, str] = {}
        self.account_token_map: Dict[str, str] = {}
        self.writers: Dict[str, list] = {}
        self.logs: Dict[str, List[dict]] = {}
        self.global_logs: List[dict] = []
        self.squad_logs: Dict[int, List[dict]] = {}
        self._log_lock = asyncio.Lock()
        self.paused: set = set()
        self.total_matches = 0
        self.matches_started = 0
        self.total_exp_gained = 0
        self.expected_workers = 0
        self.start_time = time.time()
        self.guild_jobs: Dict[int, dict] = {}
        self._guild_job_lock = asyncio.Lock()
        self._guild_job_counter = 0

    def _fmt_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def log_sync(self, uid: str, msg: str, level: str = "info"):
        uid = str(uid or "SYSTEM")
        entry = {"t": self._fmt_time(), "time": self._fmt_time(), "uid": uid, "m": str(msg), "message": str(msg), "lvl": level, "level": level}
        if uid not in self.logs:
            self.logs[uid] = []
        self.logs[uid].append(entry)
        if len(self.logs[uid]) > 200:
            self.logs[uid] = self.logs[uid][-200:]
        self.global_logs.append(entry)
        if len(self.global_logs) > 500:
            self.global_logs = self.global_logs[-500:]

    async def log(self, uid: str, msg: str, level: str = "info"):
        async with self._log_lock:
            self.log_sync(uid, msg, level)

    def squad_log(self, squad_id: int, msg: str, level: str = "info"):
        try:
            sid = int(squad_id)
        except Exception:
            sid = 0
        entry = {"t": self._fmt_time(), "time": self._fmt_time(), "m": str(msg), "message": str(msg), "lvl": level, "level": level}
        if sid not in self.squad_logs:
            self.squad_logs[sid] = []
        self.squad_logs[sid].append(entry)
        if len(self.squad_logs[sid]) > 300:
            self.squad_logs[sid] = self.squad_logs[sid][-300:]
        color_map = {
            "success": Colors.BDGREEN,
            "error": Colors.BDRED,
            "warning": Colors.GOLD,
            "info": Colors.SKY,
        }
        print_colored(f"  {color_map.get(level, Colors.SKY)}•{Colors.ENDC} {msg}", Colors.WHITE)

    def register_account(self, uid, nickname, region=None, level=1, exp=0, likes=0,
                         password="", slot=0, guild_id="", clan_id="", token=None, auth_uid=None):
        uid = str(uid)
        reg = normalize_region(region)
        cur = self.accounts.get(uid, {})
        self.accounts[uid] = {
            **cur,
            "uid": uid,
            "nickname": nickname,
            "region": reg,
            "level": level,
            "exp": exp,
            "current_exp": exp,
            "initial_exp": cur.get("initial_exp", exp),
            "gained_exp": cur.get("gained_exp", 0),
            "likes": likes,
            "password": password or cur.get("password", ""),
            "token": token or cur.get("token"),
            "auth_uid": auth_uid or cur.get("auth_uid"),
            "slot": slot or cur.get("slot", 0),
            "guild_id": str(guild_id or cur.get("guild_id", "")),
            "clan_id": str(clan_id or cur.get("clan_id", "")),
            "status": cur.get("status", "ONLINE"),
            "matches": cur.get("matches", 0),
            "active_matches": cur.get("active_matches", 0),
            "added_at": cur.get("added_at", time.time()),
            "guild_status": cur.get("guild_status", "—"),
            "guild_detail": cur.get("guild_detail", ""),
            "squad_id": cur.get("squad_id", 0),
            "is_paused": str(uid) in self.paused,
        }

    def update_status(self, uid, status, matches=None):
        uid = str(uid)
        if uid in self.accounts:
            self.accounts[uid]["status"] = status
            self.accounts[uid]["is_paused"] = (str(status).upper() == "PAUSED")
            if matches is not None:
                self.accounts[uid]["active_matches"] = matches

    def update_exp(self, uid, exp, level=None):
        uid = str(uid)
        if uid in self.accounts:
            a = self.accounts[uid]
            old = a.get("current_exp", 0)
            if exp > old:
                diff = exp - old
                a["gained_exp"] = a.get("gained_exp", 0) + diff
                self.total_exp_gained += diff
            a["current_exp"] = exp
            a["exp"] = exp
            if level:
                a["level"] = level

    def update_guild(self, uid, status, detail=""):
        uid = str(uid)
        if uid in self.accounts:
            self.accounts[uid]["guild_status"] = status
            self.accounts[uid]["guild_detail"] = detail

    def increment_match(self, uid):
        self.total_matches += 1
        uid = str(uid)
        if uid in self.accounts:
            self.accounts[uid]["matches"] = self.accounts[uid].get("matches", 0) + 1
            self.accounts[uid]["last_match_time"] = self._fmt_time()

    def increment_match_started(self):
        self.matches_started += 1

    def register_writer(self, uid, w):
        self.writers.setdefault(str(uid), []).append(w)

    def unregister_writer(self, uid, w):
        try:
            self.writers.get(str(uid), []).remove(w)
        except Exception:
            pass

    def is_paused(self, uid):
        return str(uid) in self.paused

    async def new_guild_job(self, guild_id, action, uids):
        async with self._guild_job_lock:
            self._guild_job_counter += 1
            jid = self._guild_job_counter
            self.guild_jobs[jid] = {
                "id": jid,
                "guild_id": str(guild_id),
                "action": action,
                "uids": list(uids),
                "results": {},
                "started": time.time(),
                "done": False,
            }
            return jid

    def add_guild_result(self, jid, uid, ok, msg, detail=""):
        if jid in self.guild_jobs:
            self.guild_jobs[jid]["results"][str(uid)] = {
                "ok": bool(ok),
                "msg": str(msg)[:200],
                "detail": str(detail)[:200],
                "at": time.time(),
            }

    def finish_guild_job(self, jid):
        if jid in self.guild_jobs:
            self.guild_jobs[jid]["done"] = True

bot_state = BotState()

def print_success(t, uid=""):
    print_colored(f"  {Colors.BDGREEN}✔{Colors.ENDC} {t}", Colors.WHITE)
    bot_state.log_sync(uid or "SYSTEM", t, "success")

def print_error(t, uid=""):
    print_colored(f"  {Colors.BDRED}✘{Colors.ENDC} {t}", Colors.WHITE)
    bot_state.log_sync(uid or "SYSTEM", t, "error")

def print_warning(t, uid=""):
    print_colored(f"  {Colors.GOLD}⚠{Colors.ENDC} {t}", Colors.WHITE)
    bot_state.log_sync(uid or "SYSTEM", t, "warning")

def print_info(t, uid=""):
    print_colored(f"  {Colors.SKY}ℹ{Colors.ENDC} {t}", Colors.WHITE)
    bot_state.log_sync(uid or "SYSTEM", t, "info")

def print_section(title, color=None):
    color = color or Colors.PURPLE
    bar = "━" * 68
    print_colored(f"\n{color}┏{bar}┓{Colors.ENDC}", color)
    print_colored(f"{color}┃{Colors.ENDC}  {Colors.BOLD}{Colors.GOLD}{title.center(64)}{Colors.ENDC}  {color}┃{Colors.ENDC}", color)
    print_colored(f"{color}┗{bar}┛{Colors.ENDC}\n", color)

def get_proto_field(d, key, default=None):
    if not d or not isinstance(d, dict):
        return default
    if key in d:
        v = d[key].get("data")
        return v if v is not None else default
    if str(key) in d:
        v = d[str(key)].get("data")
        return v if v is not None else default
    return default

# ═══════════════════════════ MATCH COUNTER & SQUAD RUNTIME ═══════════════════════════
_match_counters: Dict[str, int] = {}
_match_counter_lock = asyncio.Lock()

async def _inc_match(uid):
    async with _match_counter_lock:
        _match_counters[uid] = _match_counters.get(uid, 0) + 1
        return _match_counters[uid]

async def _dec_match(uid):
    async with _match_counter_lock:
        if uid in _match_counters and _match_counters[uid] > 0:
            _match_counters[uid] -= 1
        return _match_counters.get(uid, 0)

async def _get_match_count(uid):
    async with _match_counter_lock:
        return _match_counters.get(uid, 0)

class SquadRuntime:
    def __init__(self, squad_id, region="BD"):
        self.squad_id = squad_id
        self.region = normalize_region(region)
        self.members_uids: List[str] = []
        self.peers: Dict[str, dict] = {}
        self.leader_uid: Optional[str] = None
        self.team_code: Optional[str] = None
        self.pk_code: Optional[str] = None
        self.members_joined: set = set()
        self.lock = asyncio.Lock()
        self.members_lock = asyncio.Lock()
        self.is_running = False
        self.team_active = True
        self.match_count = 0
        self.match_in_progress = False
        self.match_expected_uids: set = set()
        self.match_started_uids: set = set()
        self.match_completed_uids: set = set()
        self.match_lock = asyncio.Lock()
        self.solo_fallback = False

    async def member_join(self, uid):
        uid = str(uid)
        async with self.members_lock:
            before = len(self.members_joined)
            self.members_joined.add(uid)
            after = len(self.members_joined)
        if after != before:
            print_success(f"👥 [{self.region} SQUAD-{self.squad_id}] Member Joined ({after}/{TEAM_SIZE}) → {uid}", uid)
            bot_state.squad_log(self.squad_id, f"[{self.region}] Member joined ({after}/{TEAM_SIZE}): {uid}", "success")
        return after

    async def member_leave(self, uid):
        async with self.members_lock:
            self.members_joined.discard(str(uid))

    async def member_count(self):
        async with self.members_lock:
            return len(self.members_joined)

    async def reset_members(self, keep_leader=True):
        async with self.members_lock:
            self.members_joined.clear()
            if keep_leader and self.leader_uid:
                self.members_joined.add(self.leader_uid)

# ═══════════════════════════ TOKEN CACHE ═══════════════════════════
_token_cache_memo: Dict[str, Any] = {}
_token_cache_memo_time: float = 0.0
_TOKEN_CACHE_MEMO_TTL = 5.0

def _json_serializer(obj):
    if isinstance(obj, (bytes, bytearray)):
        return {"__bytes_hex__": bytes(obj).hex()}
    raise TypeError(f"not serializable: {type(obj)}")

def _json_deserializer(obj):
    if isinstance(obj, dict):
        if "__bytes_hex__" in obj and len(obj) == 1:
            try:
                return bytes.fromhex(obj["__bytes_hex__"])
            except Exception:
                return b""
        return {k: _json_deserializer(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_deserializer(x) for x in obj]
    return obj

def _load_token_cache():
    global _token_cache_memo, _token_cache_memo_time
    now = time.time()
    if _token_cache_memo and (now - _token_cache_memo_time) < _TOKEN_CACHE_MEMO_TTL:
        return _token_cache_memo
    if not os.path.exists(TOKEN_CACHE_FILE):
        return {}
    try:
        with open(TOKEN_CACHE_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            return {}
        data = json.loads(content)
        if not isinstance(data, dict):
            raise ValueError("root must be dict")
        parsed = _json_deserializer(data)
        _token_cache_memo = parsed
        _token_cache_memo_time = now
        return parsed
    except Exception:
        return {}

def _save_token_cache(cache):
    global _token_cache_memo, _token_cache_memo_time
    try:
        tmp = TOKEN_CACHE_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, default=_json_serializer)
        os.replace(tmp, TOKEN_CACHE_FILE)
        _token_cache_memo = cache
        _token_cache_memo_time = time.time()
    except Exception:
        pass

def cache_get(uid):
    cache = _load_token_cache()
    e = cache.get(str(uid))
    if not e:
        return None
    if time.time() - e.get("cached_at", 0) > TOKEN_CACHE_TTL:
        cache_invalidate(uid)
        return None
    if str(e.get("account_id", "")).isdigit():
        e["account_id"] = int(e["account_id"])
    if not isinstance(e.get("login_payload_data"), (bytes, bytearray)):
        cache_invalidate(uid)
        return None
    return e

def cache_set(uid, data):
    cache = _load_token_cache()
    e = dict(data)
    e["cached_at"] = time.time()
    cache[str(uid)] = e
    _save_token_cache(cache)

def cache_invalidate(uid):
    cache = _load_token_cache()
    if str(uid) in cache:
        del cache[str(uid)]
        _save_token_cache(cache)

def _update_cache_profile(data, level, exp):
    try:
        keys = []
        if data.get("auth_uid"):
            keys.append(str(data["auth_uid"]))
        if data.get("auth_token"):
            keys.append(f"tok_{data['auth_token'][:20]}")
        if not keys:
            return
        cache = _load_token_cache()
        ch = False
        for k in keys:
            if k in cache and isinstance(cache[k], dict):
                cache[k]["level"] = level
                cache[k]["exp"] = exp
                ch = True
        if ch:
            _save_token_cache(cache)
    except Exception:
        pass

# ═══════════════════════════ ANTI-BAN & DEVICE & DNS ═══════════════════════════
def bypass_jitter(base, spread=0.35):
    if not (SAFE_PLAY_MODE and BYPASS_TIMING_JITTER):
        return base
    return max(0.05, base + random.uniform(-spread, spread))

def bypass_packet_jitter(base, spread_ratio=0.35):
    if not (SAFE_PLAY_MODE and BYPASS_PACKET_JITTER):
        return base
    return max(0.1, base + random.uniform(-base * spread_ratio, base * spread_ratio))

def bypass_hello_delay():
    if not (SAFE_PLAY_MODE and BYPASS_HELLO_DELAY):
        return 0.0
    return random.uniform(0.05, 0.45)

def bypass_ka_jitter(base=5.0):
    if not (SAFE_PLAY_MODE and BYPASS_KA_JITTER):
        return base
    return max(3.0, base + random.uniform(-0.8, 1.2))

def bypass_human_reconnect_delay(attempt):
    if not (SAFE_PLAY_MODE and BYPASS_TIMING_JITTER):
        return min(attempt * 0.5, 2.0)
    return max(0.05, min(attempt * 0.5, 2.0) + random.uniform(-0.4, 0.7))

def get_device_for_account(account_identifier):
    devices = {}
    if os.path.exists(DEVICES_FILE):
        try:
            with open(DEVICES_FILE, "r", encoding="utf-8") as f:
                devices = json.load(f)
                if not isinstance(devices, dict):
                    devices = {}
        except Exception:
            devices = {}
    key = str(account_identifier)
    if key in devices:
        return devices[key]
    dev_list = [
        ("Samsung", "SM-G998B", "Adreno (TM) 660", "Android OS 12 / API-31"),
        ("Xiaomi", "2201122G", "Adreno (TM) 730", "Android OS 13 / API-33"),
        ("Realme", "RMX3700", "Mali-G710", "Android OS 14 / API-34"),
        ("OnePlus", "CPH2451", "Adreno (TM) 740", "Android OS 13 / API-33"),
        ("OPPO", "CPH2611", "Adreno (TM) 720", "Android OS 14 / API-34"),
    ]
    brand, model, gpu, os_ver = random.choice(dev_list)
    dev = {
        "unique_device_id": f"Google|{uuid.uuid4()}",
        "brand": brand,
        "model": model,
        "gpu_renderer": gpu,
        "system_software": os_ver,
        "screen_width": random.choice([1080, 1440, 720]),
        "screen_height": random.choice([2400, 3200, 1600]),
        "screen_dpi": str(random.randint(300, 420)),
        "memory": random.randint(2800, 6500),
        "processor_details": f"ARM64 FP ASIMD AES | {random.randint(2200, 3200)} | {random.randint(6, 12)}",
        "client_ip": f"{random.randint(103, 223)}.{random.randint(10, 250)}.{random.randint(10, 250)}.{random.randint(10, 250)}",
    }
    devices[key] = dev
    try:
        with open(DEVICES_FILE, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=2)
    except Exception:
        pass
    return dev

_DNS_CACHE: Dict[str, Tuple[str, float]] = {}
_DNS_CACHE_TTL = 300.0

async def resolve_host_cloudflare(hostname):
    if not hostname:
        return hostname
    parts = hostname.split(".")
    if len(parts) == 4 and all(p.isdigit() for p in parts):
        return hostname
    now = time.time()
    if hostname in _DNS_CACHE:
        ip, exp = _DNS_CACHE[hostname]
        if now < exp:
            return ip
    try:
        loop = asyncio.get_running_loop()
        info = await loop.getaddrinfo(hostname, None, family=socket.AF_INET)
        if info:
            ip = info[0][4][0]
            _DNS_CACHE[hostname] = (ip, now + _DNS_CACHE_TTL)
            return ip
    except Exception:
        if "clientbp.ggpolarbear.com" in hostname:
            return "104.28.197.151"
    return hostname

def optimize_tcp_socket(sock):
    try:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 131072)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 131072)
    except Exception:
        pass

def optimize_udp_socket(sock):
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 131072)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 131072)
    except Exception:
        pass
    if sys.platform == "win32":
        try:
            sock.ioctl(0x9800000C, b"\x00\x00\x00\x00")
        except Exception:
            pass

async def safe_close_writer(writer):
    if not writer:
        return
    try:
        if not writer.is_closing():
            writer.close()
        await asyncio.wait_for(writer.wait_closed(), timeout=1.5)
    except Exception:
        pass

# ═══════════════════════════ HTTP CLIENT & ENCRYPTION ═══════════════════════════
client = httpx.AsyncClient(
    verify=False,
    timeout=12.0,
    limits=httpx.Limits(max_connections=200, max_keepalive_connections=100),
)
_LOGIN_SEMAPHORE = asyncio.Semaphore(6)

base_headers = {
    "User-Agent": "UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Unity-Version": "2022.3.47f1",
    "X-GA-SV": "1789535859",
    "X-GA": "v1 1",
    "ReleaseVersion": "OB55",
}

CRC7_TABLE = bytes([
    0,9,18,27,36,45,54,63,72,65,90,83,108,101,126,119,25,16,11,2,61,52,47,38,
    81,88,67,74,117,124,103,110,50,59,32,41,22,31,4,13,122,115,104,97,94,87,76,69,
    43,34,57,48,15,6,29,20,99,106,113,120,71,78,85,92,100,109,118,127,64,73,82,91,
    44,37,62,55,8,1,26,19,125,116,111,102,89,80,75,66,53,60,39,46,17,24,3,10,
    86,95,68,77,114,123,96,105,30,23,12,5,58,51,40,33,79,70,93,84,107,98,121,112,
    7,14,21,28,35,42,49,56,65,72,83,90,101,108,119,126,9,0,27,18,45,36,63,54,
    88,81,74,67,124,117,110,103,16,25,2,11,52,61,38,47,115,122,97,104,87,94,69,76,
    59,50,41,32,31,22,13,4,106,99,120,113,78,71,92,85,34,43,48,57,6,15,20,29,
    37,44,55,62,1,8,19,26,109,100,127,118,73,64,91,82,60,53,46,39,24,17,10,3,
    116,125,102,111,80,89,66,75,23,30,5,12,51,58,33,40,95,86,77,68,123,114,105,96,
    14,7,28,21,42,35,56,49,70,79,84,93,98,107,112,121,
])
_DELTA = 0x9E3779B9
_ROUNDS = 16
_FIELD_SIZES = {0: 1, 1: 2, 2: 2, 3: 1, 4: 2}
_FIELD_NAMES = {0: "sendOption", 1: "cmd", 2: "orderId", 3: "flags", 4: "length"}

async def aes_encrypt(payload, key, iv):
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(payload, AES.block_size))

def encrypt_api(plain_hex):
    return AES.new(AES_KEY, AES.MODE_CBC, AES_IV).encrypt(
        pad(bytes.fromhex(plain_hex), AES.block_size)
    ).hex()

def encrypt_api_bytes(plain_bytes):
    return AES.new(AES_KEY, AES.MODE_CBC, AES_IV).encrypt(pad(plain_bytes, AES.block_size))

def encode_varint(n):
    if n < 0:
        n &= 0xFFFFFFFFFFFFFFFF
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            b |= 0x80
        out.append(b)
        if not n:
            break
    return bytes(out)

def _pb_varint(fn, val):
    return encode_varint((fn << 3) | 0) + encode_varint(val)

def _pb_length(fn, val):
    enc = val.encode("utf-8") if isinstance(val, str) else val
    return encode_varint((fn << 3) | 2) + encode_varint(len(enc)) + enc

def create_proto(fields) -> bytes:
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(field, str):
            field = int(field)
        if isinstance(value, dict):
            packet.extend(_pb_length(field, bytes(create_proto(value))))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    packet.extend(_pb_length(field, bytes(create_proto(item))))
                elif isinstance(item, str):
                    packet.extend(_pb_length(field, item))
                elif isinstance(item, (bytes, bytearray)):
                    packet.extend(_pb_length(field, bytes(item)))
                elif isinstance(item, bool):
                    packet.extend(_pb_varint(field, 1 if item else 0))
                elif isinstance(item, int):
                    packet.extend(_pb_varint(field, item))
        elif isinstance(value, bool):
            packet.extend(_pb_varint(field, 1 if value else 0))
        elif isinstance(value, int):
            packet.extend(_pb_varint(field, value))
        elif isinstance(value, str):
            packet.extend(_pb_length(field, value))
        elif isinstance(value, (bytes, bytearray)):
            packet.extend(_pb_length(field, bytes(value)))
    return bytes(packet)

def build_proto(fields):
    return create_proto(fields)

def decode_varint(data, offset):
    result = 0
    shift = 0
    while offset < len(data):
        byte = data[offset]
        result |= (byte & 0x7F) << shift
        offset += 1
        if not (byte & 0x80):
            return result, offset
        shift += 7
    return None, offset

def decode_protobuf_2(data):
    result = {}
    offset = 0
    data_len = len(data)
    while offset < data_len:
        header, offset = decode_varint(data, offset)
        if header is None:
            break
        fn = header >> 3
        wt = header & 0x7
        if wt == 0:
            v, offset = decode_varint(data, offset)
            if v is not None:
                result[fn] = v
        elif wt == 2:
            length, offset = decode_varint(data, offset)
            if length is None or offset + length > data_len:
                break
            value = data[offset:offset + length]
            offset += length
            try:
                s = value.decode("utf-8")
                result[fn] = s if s else value.hex()
            except UnicodeDecodeError:
                nested = decode_protobuf_2(value)
                result[fn] = nested if nested else value.hex()
        elif wt == 1:
            offset += 8
        elif wt == 5:
            offset += 4
        else:
            break
    return result

def extract_raw_fields(data: bytes) -> dict:
    result = {}
    offset = 0
    data_len = len(data)
    while offset < data_len:
        header, offset = decode_varint(data, offset)
        if header is None:
            break
        fn = header >> 3
        wt = header & 0x7
        if wt == 0:
            v, offset = decode_varint(data, offset)
            if v is not None:
                result[fn] = v
        elif wt == 2:
            length, offset = decode_varint(data, offset)
            if length is None or offset + length > data_len:
                break
            result[fn] = bytes(data[offset:offset + length])
            offset += length
        elif wt == 1:
            offset += 8
        elif wt == 5:
            offset += 4
        else:
            break
    return result

async def parse_results(parsed):
    out = {}
    for r in parsed:
        fd = {"wire_type": r.wire_type}
        if r.wire_type in ("varint", "string", "bytes"):
            fd["data"] = r.data
        elif r.wire_type == "length_delimited":
            fd["data"] = await parse_results(r.data.results)
        out[str(r.field)] = fd
    return out

def _recursive_dict(results):
    out = {}
    for r in results:
        fd = {"wire_type": r.wire_type}
        if r.wire_type in ("varint", "string", "bytes"):
            fd["data"] = r.data
        elif r.wire_type == "length_delimited":
            if hasattr(r.data, "results"):
                fd["data"] = _recursive_dict(r.data.results)
            elif isinstance(r.data, list):
                fd["data"] = _recursive_dict(r.data)
            else:
                fd["data"] = str(r.data)
        out[str(r.field)] = fd
    return out

async def decode_protobuf(data):
    if Parser is None:
        raw = bytes.fromhex(data) if isinstance(data, str) else data
        return json.dumps({str(k): {"data": v} for k, v in decode_protobuf_2(raw).items()})
    parsed = Parser().parse(data)
    return json.dumps(await parse_results(parsed))

def decode_protobuf_dict_safe(data):
    if Parser is None:
        raw = bytes.fromhex(data) if isinstance(data, str) else data
        return {str(k): {"data": v} for k, v in decode_protobuf_2(raw).items()}
    try:
        parsed = Parser().parse(data)
        return _recursive_dict(parsed)
    except Exception:
        return {}

# ═══════════════════════════ SQUAD PACKET BUILDERS (IND + BD) ═══════════════════════════
def create_packet(Pk, N, K, V):
    if isinstance(K, str):
        K = bytes.fromhex(K) if len(K) == 32 else K.encode()
    if isinstance(V, str):
        V = bytes.fromhex(V) if len(V) == 32 else V.encode()
    PkEnc = AES.new(K, AES.MODE_CBC, V).encrypt(pad(bytes.fromhex(Pk), 16)).hex()
    L = len(PkEnc) // 2
    hexlen = hex(L)[2:]
    if len(hexlen) % 2 != 0:
        hexlen = "0" + hexlen
    pad_len = 12 - len(N) - len(hexlen)
    if pad_len < 0:
        pad_len = 0
    return bytes.fromhex(N + ("0" * pad_len) + hexlen + PkEnc)

def create_team(key, iv, game_version="1.132.9", region="BD"):
    reg = normalize_region(region)
    srv_code = get_server_code_for_region(reg)
    fields = {
        1: 1,
        2: {
            2: bytes.fromhex("01"),
            3: 1,
            4: 3,
            5: REGION_LANG.get(reg, "en"),
            8: {1: srv_code, 2: 123, 3: reg},
            9: 1,
            10: bytes.fromhex("01090a0b1219202729"),
            11: 2,
            13: 1,
            14: {
                1: "08FBA33B4BABE2790205390333330000009700050092005F72697EB2134DCBB2467625142201040e38e848dc0e748c3f6aa04d81000000ff1113090dcacfa16d",
                2: 478,
                3: "7e585d55",
                4: "y[Z]",
                6: 12,
                7: "15686677735a7506101c",
                8: str(game_version),
                9: 3,
                10: 1,
                11: "03626253513637754174",
            },
            19: 329,
            21: bytes.fromhex("374f521955"),
            24: {1: 21},
            27: "a_6534489873065906362",
        },
    }
    return create_packet(create_proto(fields).hex(), get_team_prefix(reg), key, iv)

def leave_team(account_id, key, iv, region="BD"):
    reg = normalize_region(region)
    return create_packet(
        create_proto({1: 7, 2: {1: int(account_id)}}).hex(),
        get_team_prefix(reg), key, iv
    )

def team_fresh(account_id, key, iv, region="BD"):
    reg = normalize_region(region)
    return create_packet(
        create_proto({1: 72, 2: {1: int(account_id)}}).hex(),
        get_team_prefix(reg), key, iv
    )

def invite_player_in_team(target_uid, key, iv, region="BD"):
    reg = normalize_region(region)
    return create_packet(
        create_proto({1: 2, 2: {1: int(target_uid), 2: reg, 4: 1}}).hex(),
        get_team_prefix(reg), key, iv
    )

def accept_team_invite(target_uid, group_id, key, iv, region="BD", game_version="1.132.9"):
    reg = normalize_region(region)
    srv_code = get_server_code_for_region(reg)
    fields = {
        1: 4,
        2: {
            1: int(target_uid),
            3: int(target_uid),
            4: bytes.fromhex("0107090a0b120f19202729"),
            8: 1,
            9: {
                1: "08FBA33B0522052002041B0222220007000C00010004000547E265AE1080779546762514110104076fa2e8770e748c3f6a68ed75000000ff08080500cacfa16d",
                2: 235,
                3: {14: 80, 11: 86},
                4: "{Y\\R",
                6: 13,
                7: {2: 4},
                8: str(game_version),
                9: 2,
                10: 1,
                11: "0362625351",
            },
            10: str(group_id),
            11: {"1": srv_code, "2": 107, "3": reg},
            13: REGION_LANG.get(reg, "en"),
            16: "374f5219",
            20: {1: 21},
            23: "a_6534489873065906362",
            24: "https://dl-sg-production.freefiremobile.com/",
            27: {1: 2, 2: 4},
        },
    }
    return create_packet(create_proto(fields).hex(), get_team_prefix(reg), key, iv)

def start_match_team(account_id, key, iv, region="BD"):
    reg = normalize_region(region)
    srv_code = get_server_code_for_region(reg)
    fields = {1: 9, 2: {1: int(account_id), 7: {1: srv_code, 2: 410, 3: reg}}}
    return create_packet(create_proto(fields).hex(), get_team_prefix(reg), key, iv)

def ready_for_game(uid, key, iv, region="BD"):
    reg = normalize_region(region)
    return create_packet(create_proto({1: 15, 2: {1: int(uid), 2: 1}}).hex(), get_team_prefix(reg), key, iv)

# ═══════════════════════════ AUTH & LOGIN (IND + BD) ═══════════════════════════
async def get_playstore_version(region="BD"):
    reg = normalize_region(region)
    if play_scraper is None:
        return "1.132.9"
    loop = asyncio.get_running_loop()
    try:
        lang = REGION_LANG.get(reg, "en")
        country = "in" if reg == "IND" else "bd"
        res = await loop.run_in_executor(
            None, lambda: play_scraper("com.dts.freefireth", lang=lang, country=country)
        )
        return res.get("version") or "1.132.9"
    except Exception:
        return "1.132.9"

async def version_config(region="BD"):
    reg = normalize_region(region)
    app_version = await get_playstore_version(reg)
    lang = REGION_LANG.get(reg, "en")
    url = (
        "https://version.ggwhitehawk.com/live/ver.php"
        f"?version={app_version}&lang={lang}&device=android&channel=android"
        f"&appstore=googleplay&region={reg}&whitelist_version=1.3.0&whitelist_sp_version=1.0.0"
    )
    try:
        r = await client.get(url)
        r.raise_for_status()
        d = r.json()
        su = d.get("server_url")
        rv = d.get("remote_version")
        lr = d.get("latest_release_version")
        if not su or not rv or not lr:
            return None
        return lr, rv, su
    except Exception:
        return None

async def get_access_token(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    hdrs = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; SM-G998B)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close",
    }
    data = {
        "uid": str(uid),
        "password": str(password),
        "response_type": "token",
        "client_type": "2",
        "client_secret": HEX_KEY,
        "client_id": "100067",
    }
    for attempt in range(5):
        try:
            r = await client.post(url, headers=hdrs, data=data)
            if r.status_code == 200:
                d = r.json()
                oid = d.get("open_id")
                at = d.get("access_token")
                pf = d.get("platform", 4)
                if oid and at:
                    return oid, at, pf
            if r.status_code == 429:
                await asyncio.sleep(1)
                continue
        except Exception:
            pass
        await asyncio.sleep(0.5)
    return None

async def build_majorlogin_payload(open_id, access_token, platform, client_version, dev, region="BD"):
    reg = normalize_region(region)
    try:
        p = {
            3: str(datetime.now())[:-7],
            4: "free fire",
            5: "1",
            7: str(client_version) if client_version else "1.132.9",
            8: str(dev.get("system_software", "Android OS 14 / API-34")),
            9: "Handheld",
            10: "Airtel" if reg == "IND" else "Grameenphone",
            11: "CarrierDataNetwork",
            12: str(dev.get("screen_width", 1639)),
            13: str(dev.get("screen_height", 720)),
            14: str(dev.get("screen_dpi", 320)),
            15: str(dev.get("processor_details", "ARM64 FP ASIMD AES | 2200 | 8")),
            16: str(dev.get("memory", 5653)),
            17: str(dev.get("gpu_renderer", "Mali-G52 MC2")),
            18: "OpenGL ES 3.2 v1.r49p1-03bet0",
            19: str(dev.get("unique_device_id", f"Google|{uuid.uuid4()}")),
            20: str(dev.get("client_ip", "27.61.46.111" if reg == "IND" else "182.5.135.225")),
            21: REGION_LANG.get(reg, "en"),
            22: str(open_id),
            23: str(platform),
            24: "Handheld",
            25: str(dev.get("model", "Xiaomi")),
            26: reg,
            29: str(access_token),
            30: "1",
            41: "Airtel" if reg == "IND" else "Grameenphone",
            42: "4G",
            57: "7428b253defc164018c604a1ebbfebdf",
            60: "109278",
            61: "55402",
            62: "868",
            64: "55927",
            65: "109278",
            66: "55927",
            67: "109278",
            73: 2,
            74: "/data/app/~~6Cw028g_ld-8Z0z2qhrOLA==/com.dts.freefireth-i3wiaEmpx8CbiRVhUMx_ag==/lib/arm64",
            76: 1,
            77: "b8e0cd5e295eee42f5860d3c86e483dd|/data/app/~~6Cw028g_ld-8Z0z2qhrOLA==/com.dts.freefireth-i3wiaEmpx8CbiRVhUMx_ag==/base.apk",
            78: 6,
            79: 1,
            81: "32",
            83: "2019121229",
            85: 3,
            86: "OpenGLES2",
            87: 3071,
            88: 4,
            89: 14466,
            90: "Coimbatore" if reg == "IND" else "",
            91: "TN" if reg == "IND" else "",
            93: "3rd_party",
            94: "KqsHTyb7yHjsAiyNWUUZa0DSOD6U0AhDQ76smAo1WeHHHpSmJ8KMRyRrxb2ttgJqO9YOqO/K6AORAvDMAX/qBS8+JahIkrM7kHfzlfULbgRAoZ9r",
            95: "111207",
            96: '{"cur_rate":[60,90,120],"support_etc2":true}',
            97: "1",
            98: "1",
            99: str(platform),
            100: str(platform),
            103: "1",
            104: "52837",
            105: "1",
            106: "https://dl.gmc.freefiremobile.com/live/ABHotUpdates/|211c933168f55902c7dfbfd8c4e2957d",
            107: "1.3fb8adbf45f44ce9",
        }
        return encrypt_api_bytes(build_proto(p))
    except Exception as e:
        print_error(f"build_majorlogin_payload: {e}")
        return None

async def send_majorlogin(data, release_version, server_url):
    if thunderFF_pb2 is None:
        return None
    try:
        url = f"{server_url}MajorLogin" if server_url.endswith("/") else f"{server_url}/MajorLogin"
        hdrs = base_headers.copy()
        hdrs["ReleaseVersion"] = str(release_version)
        r = await client.post(url, headers=hdrs, data=data)
        if r.status_code != 200:
            return None
        c = r.content
        if len(c) < 40:
            return None
        for off in [0, 64] + list(range(128)):
            try:
                m = thunderFF_pb2.MajorLoginRes()
                m.ParseFromString(c[off:])
                if m.region and m.token:
                    return m
            except Exception:
                continue
        return None
    except Exception:
        return None

async def send_getlogin(data, base_url, token, release_version):
    if thunderFF_pb2 is None:
        return None
    try:
        url = f"{base_url.rstrip('/')}/GetLoginData"
        hdrs = base_headers.copy()
        hdrs["ReleaseVersion"] = str(release_version)
        hdrs["Authorization"] = f"Bearer {token}"
        r = await client.post(url, headers=hdrs, data=data)
        if r.status_code != 200:
            return None
        c = r.content
        rp = thunderFF_pb2.GetLoginDataRes()
        ok = False
        try:
            rp.ParseFromString(c)
            if rp.functional_addrs or rp.informational_addrs:
                ok = True
        except Exception:
            pass
        if not ok:
            for off in range(min(128, len(c))):
                try:
                    cand = thunderFF_pb2.GetLoginDataRes()
                    cand.ParseFromString(c[off:])
                    if cand.functional_addrs or cand.informational_addrs:
                        rp = cand
                        break
                except Exception:
                    continue
        dd = {}
        try:
            if Parser is not None:
                parsed = Parser().parse(c.hex())
                dd = await parse_results(parsed)
        except Exception:
            pass
        return rp, dd
    except Exception:
        return None

# ═══════════════════════════ HTTP PING & TCP GATEWAY ═══════════════════════════
async def send_ping(account_id, token, release_version):
    try:
        acc = int(account_id) if str(account_id).isdigit() else 0
        now_ms = int(time.time() * 1000)
        payload = struct.pack("<Q", acc & 0xFFFFFFFFFFFFFFFF) + struct.pack("<Q", now_ms & 0xFFFFFFFFFFFFFFFF)
        hdrs = {
            "accept": "*/*",
            "accept-encoding": "deflate, gzip",
            "authorization": f"Bearer {token}",
            "content-type": "application/x-www-form-urlencoded",
            "releaseversion": str(release_version),
            "user-agent": "UnityPlayer/2022.3.47f1",
            "x-ga": "v1 1",
            "x-ga-sv": str(int(time.time())),
            "x-real-ip": PING_REAL_IP,
            "x-request-start": str(now_ms),
            "x-unity-version": "2022.3.47f1",
        }
        r = await client.post(PING_URL, headers=hdrs, content=payload, timeout=PING_TIMEOUT)
        return r.status_code == 200
    except Exception:
        return False

async def ping_worker(account_id, token, release_version, region="BD"):
    if not ENABLE_HTTP_PING:
        return
    uid_str = str(account_id)
    try:
        await asyncio.sleep(5.0 + random.uniform(0, 2.0))
        while True:
            await send_ping(uid_str, token, release_version)
            await asyncio.sleep(max(5.0, PING_INTERVAL + random.uniform(-3.0, 3.0)))
    except asyncio.CancelledError:
        pass

async def build_tcp_startup_packet(account_id, token, server_time, key, iv, region="BD", typ="OnLine"):
    reg = normalize_region(region)
    uid_hex = f"{int(account_id):016x}"
    ts_hex = f"{int(server_time):08x}"
    enc = (await aes_encrypt(token.encode(), key, iv)).hex()
    enc_len = f"{len(enc) // 2:08x}"
    pfx = get_tcp_prefix(reg, typ)
    if typ == "OnLine":
        return f"{pfx}{uid_hex}{ts_hex}00000000{enc_len}{enc}"
    return f"{pfx}{uid_hex}{ts_hex}{enc_len}{enc}"

async def send_keep_alive(region="BD"):
    return get_keepalive_bytes(region)

# ═══════════════════════════ BR SEARCH (IND + BD) ═══════════════════════════
BR_HEX = (
    "080112800a0a010110013a110a044944433110aa011a064555524f50453a100a044944433210311a064555524f5045"
    "40014a0801090a0b1219202758016291090a80013038384638324246303241393637363730323031303130303030"
    "30303030303030303030303030303031363030303130303135303030323232463937454545304630303030303034363736323531"
    "34303030303030303030303030303030303030303030303030303030303030303030303030306666303030303030"
    "3030636163666131366410241afb02735d5e571400024a775d45414d1a041b1c001f11010449715f4243481a001e"
    "1d071c1703004b1a4066785c524570735c51486775421b5c5a4c07504042685a63610816054e19025e7519600147"
    "7c015165406370195f5547404e4550640103020f1304064863754268676c755f65576e40467e5f0a417a4701026d"
    "675d6e73670b1108495a4c6a0b78470b740065645e525a057258425f584a447d4e6759440c11044e7c596d7f4b62"
    "5f7d04055a47505c4e1d6b5b4107447d7201057d7f0f14084e430457674f7e517d72015172415d027473577c4d61"
    "5f79535256780911030f4d5e027a797f614165067806505d53777750475e75064257076500460817014e741e7e50"
    "78487e7a7c465e7669767153497064605a7376677773550d160148037e18675966787f4c42607a645f577e7b44"
    "1b460776026b18685d0b110205490060020f70676175654674706671797f41067346677c4e06585e780f15074c57"
    "047b40517075415f6364027259674b5b0166407f7340600407770a22047a5d5c52300b3a0a167305067162727516"
    "134208312e3133302e3232480350015ae90403626253513635686e556f4e36416456324b796f566c636f47777648"
    "4f624e56526c4d727073504b4f43654177616848494176795556497273743752737149734a7a786b324752526837"
    "7a2f637664626d504f6a73552f79626d38547a4c69586d2f474351696d494b53486833447955726f39515152756c"
    "34545350626d6d624b7949565937545671577059455372323646572f59624578507338514f706d317372785455736c"
    "30796a434144444d4f34616a654b615753366361496c554b4963797a494e396d52516f715277687939797257476d"
    "337a644345337a6a61436f492f5a585233656f65365a42647a64677654636b6b665733356e4d4c6a6a56507256"
    "4b6433523172756174394e50514150724a5546627859696c4c5a3859707336654d5447666b6649793574666a526c"
    "314d4648706b51774c6373374439656378566c41636f374e664f6d2b30654756466c443474447870677138553359"
    "5973587645384842502f70666c767a737138316a32524f4d7857437556445442492f684735625462773166456e42"
    "49725162762b636144775147696f74554e316d4c4b77734379456f4766706746614251457645672b736a764c4c78"
    "704743334c304a5344532f74526169504354553344374e6249306547516651622f5a466f4c36455630775a324d6f"
    "583932414c572f5049752f56634663584e70596b356f7966326151416a536971486a2f363276354843644f525551"
    "303578754e6171795251625653704654303137655237675255636b4966366c6f447476342b514e4a4670766d7475"
    "7077707774396a5a5974437a4b56743657726d6e36785837706658456251555434684f3758a201050803108703a2"
    "01050804108103a20105080510c001a20105081d10cc01a2010408161078a20105080e10af01a201020815"
)

async def start_game_battle_royale(region, client_version, writer, key, iv):
    reg = normalize_region(region)
    packet = bytes.fromhex(BR_HEX)
    try:
        if _HAS_CGU:
            proto = CguFF_pb2.StartMatch()
            proto.ParseFromString(packet)
            if hasattr(proto.main, "region_list") and len(proto.main.region_list) > 0:
                proto.main.region_list[0].region = reg
                if len(proto.main.region_list) > 1:
                    proto.main.region_list[1].region = reg
            if hasattr(proto.main, "client_version"):
                proto.main.client_version.remote_version = client_version
            packet = proto.SerializeToString()
        elif thunderFF_pb2 and hasattr(thunderFF_pb2, "StartMatch"):
            proto = thunderFF_pb2.StartMatch()
            proto.ParseFromString(packet)
            if hasattr(proto.main, "region_list") and len(proto.main.region_list) > 0:
                proto.main.region_list[0].region = reg
                if len(proto.main.region_list) > 1:
                    proto.main.region_list[1].region = reg
            if hasattr(proto.main, "client_version"):
                proto.main.client_version.remote_version = client_version
            packet = proto.SerializeToString()
    except Exception:
        pass
    enc = (await aes_encrypt(packet, key, iv)).hex()
    plen = len(enc) // 2
    hl = hex(plen)[2:]
    hl = hl if len(hl) > 1 else "0" + hl
    pfx = get_br_prefix(reg)
    final = pfx + "0" * (6 - len(hl)) + hl + enc
    writer.write(bytes.fromhex(final))
    await writer.drain()
    print_success(f"[{reg} BR] Search Sent → {plen}B | Region={reg}")

# ═══════════════════════════ UDP CRYPTO & MOVEMENT ═══════════════════════════
async def has_ssan_zig(n):
    z = (n << 1) & 0xFFFFFFFFFFFFFFFF
    out = bytearray()
    while z >= 0x80:
        out.append((z & 0x7F) | 0x80)
        z >>= 7
    out.append(z)
    return bytes(out)

async def uleb_encode(n):
    try:
        n = int(n)
    except Exception:
        n = 0
    if n < 0:
        n &= 0xFFFFFFFFFFFFFFFF
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            b |= 0x80
        out.append(b)
        if not n:
            break
    return bytes(out)

async def zigzag_encode_signed(n):
    try:
        n = int(n)
    except Exception:
        n = 0
    zz = (n << 1) ^ (n >> 63)
    if zz < 0:
        zz = -zz
    zz &= 0xFFFFFFFFFFFFFFFF
    out = bytearray()
    while True:
        b = zz & 0x7F
        zz >>= 7
        if zz:
            b |= 0x80
        out.append(b)
        if not zz:
            break
    return bytes(out)

async def tea_enc(v0, v1, k0, k1, k2, k3):
    s = 0
    for _ in range(_ROUNDS):
        s = (s + _DELTA) & 0xFFFFFFFF
        v0 = (v0 + (((((v1 << 4) & 0xFFFFFFFF) + k0) & 0xFFFFFFFF ^ ((v1 + s) & 0xFFFFFFFF) ^ (((v1 >> 5) + k1) & 0xFFFFFFFF)))) & 0xFFFFFFFF
        v1 = (v1 + (((((v0 << 4) & 0xFFFFFFFF) + k2) & 0xFFFFFFFF ^ ((v0 + s) & 0xFFFFFFFF) ^ (((v0 >> 5) + k3) & 0xFFFFFFFF)))) & 0xFFFFFFFF
    return v0, v1

async def tea_dec(v0, v1, k0, k1, k2, k3):
    s = (_DELTA * _ROUNDS) & 0xFFFFFFFF
    for _ in range(_ROUNDS):
        v1 = (v1 - (((((v0 << 4) & 0xFFFFFFFF) + k2) & 0xFFFFFFFF ^ ((v0 + s) & 0xFFFFFFFF) ^ (((v0 >> 5) + k3) & 0xFFFFFFFF)))) & 0xFFFFFFFF
        v0 = (v0 - (((((v1 << 4) & 0xFFFFFFFF) + k0) & 0xFFFFFFFF ^ ((v1 + s) & 0xFFFFFFFF) ^ (((v1 >> 5) + k1) & 0xFFFFFFFF)))) & 0xFFFFFFFF
        s = (s - _DELTA) & 0xFFFFFFFF
    return v0, v1

async def tea_cbc_encrypt(padded, key_bytes):
    k0, k1, k2, k3 = (struct.unpack_from("<I", key_bytes, o)[0] for o in (0, 4, 8, 12))
    out = bytearray(len(padded))
    pc = bytearray(8)
    pi = bytearray(8)
    for i in range(0, len(padded), 8):
        x = bytearray(8)
        for j in range(8):
            x[j] = padded[i + j] ^ pc[j]
        e0, e1 = await tea_enc(
            struct.unpack_from("<I", x, 0)[0],
            struct.unpack_from("<I", x, 4)[0],
            k0, k1, k2, k3
        )
        enc = bytearray(8)
        struct.pack_into("<I", enc, 0, e0)
        struct.pack_into("<I", enc, 4, e1)
        for j in range(8):
            out[i + j] = enc[j] ^ pi[j]
        pc[:] = out[i:i + 8]
        pi[:] = x
    return bytes(out)

async def tea_cbc_decrypt(body, key_bytes):
    k0, k1, k2, k3 = (struct.unpack_from("<I", key_bytes, o)[0] for o in (0, 4, 8, 12))
    out = bytearray(len(body))
    pi = bytearray(8)
    pc = bytearray(8)
    x = bytearray(8)
    dec = bytearray(8)
    for i in range(0, len(body), 8):
        for j in range(8):
            x[j] = body[i + j] ^ pi[j]
        d0, d1 = await tea_dec(
            struct.unpack_from("<I", x, 0)[0],
            struct.unpack_from("<I", x, 4)[0],
            k0, k1, k2, k3
        )
        struct.pack_into("<I", dec, 0, d0)
        struct.pack_into("<I", dec, 4, d1)
        for j in range(8):
            out[i + j] = dec[j] ^ pc[j]
        pc[:] = body[i:i + 8]
        pi[:] = dec
    return bytes(out)

async def build_padded(content):
    pad_len = (8 - (len(content) + 10) % 8) % 8
    return bytes([pad_len, 0, 0]) + b"\x00" * pad_len + content + b"\x00" * 7

async def encode_header(layout, so, cmd, oid, flags, length, k, v80):
    out = bytearray()
    for code in layout:
        val = {0: so, 1: cmd, 2: oid, 3: flags, 4: length}[code]
        if _FIELD_SIZES[code] == 1:
            out.append((val & 0xFF) ^ k)
        else:
            v = ((val & 0xFFFF) ^ v80) & 0xFFFF
            out.append(v & 0xFF)
            out.append((v >> 8) & 0xFF)
    return bytes(out)

async def crc7_buff(crc, buf):
    c = crc & 0x7F
    for b in buf:
        c = CRC7_TABLE[((2 * (c & 0xFF)) ^ (b & 0xFF)) & 0xFF] & 0x7F
    return c & 0x7F

async def sv_frame(msg_key, layout, so, cmd, oid, flags, content, key, encrypted=True):
    k = key[0]
    v80 = ((k << 8) | k) & 0xFFFF
    body = await tea_cbc_encrypt(await build_padded(content), key) if encrypted else content
    hdr = bytearray([msg_key, 0]) + await encode_header(layout, so, cmd, oid, flags, len(body), k, v80)
    pkt = bytearray(hdr + body)
    pkt[1] = await crc7_buff(0, bytes(pkt[2:])) & 0x7F
    return bytes(pkt)

async def build_packet(msg_key, layout, so, cmd, oid, flags, content, key, encrypted=True):
    k = key[0]
    v80 = ((k << 8) | k) & 0xFFFF
    body = await tea_cbc_encrypt(await build_padded(content), key) if encrypted else content
    hdr = bytearray([msg_key, 0])
    for code in layout:
        val = {0: so, 1: cmd, 2: oid, 3: flags, 4: len(body)}[code]
        if _FIELD_SIZES[code] == 1:
            hdr.append((val & 0xFF) ^ k)
        else:
            v = ((val & 0xFFFF) ^ v80) & 0xFFFF
            hdr.append(v & 0xFF)
            hdr.append((v >> 8) & 0xFF)
    pkt = bytearray(hdr + body)
    pkt[1] = await crc7_buff(0, bytes(pkt[2:])) & 0x7F
    return bytes(pkt)

async def layouts_from_mask(mask):
    if isinstance(mask, (bytes, bytearray)):
        mask = mask.decode("utf-8", errors="ignore")
    s = "".join(ch for ch in str(mask).strip() if ch in "01234")
    ru = [int(c) for c in s] if len(s) == 5 else [0, 1, 4, 3, 2]
    nr = [c for c in ru if c != 2]
    return ru, nr

async def build_hello_packet(text, key, layout):
    data = text.encode("utf-8")
    if len(data) > 25:
        raise ValueError("too long")
    content = b"\x10\x00\x00\x00" + data + b"\x00" * (29 - 4 - len(data))
    k = key[0] if key else 10
    v80 = ((k << 8) | k) & 0xFFFF
    layout = [int(c) for c in str(layout).strip()] if isinstance(layout, str) else list(layout)
    padded = await build_padded(content)
    enc_body = await tea_cbc_encrypt(padded, key)
    hdr = await encode_header(layout, 1, 1, 0, 1, len(enc_body), k, v80)
    pkt = bytearray([0x63, 0x00]) + hdr + enc_body
    pkt[1] = await crc7_buff(0, pkt[2:]) & 0x7F
    return bytes(pkt).hex()

async def classify(frame):
    cmd = frame["cmd"]
    name = MESSAGE_ID_TO_NAME.get(cmd, f"UNKNOWN_{cmd}")
    if name == "UDP_HELLO":
        return "HELLO"
    if name == "UDP_ACK":
        return "ACK"
    if name == "UDP_PING":
        return "PING"
    if name == "RUDP_JOIN_MATCH":
        return "JOIN_MATCH"
    return name

async def reply_for(frame, key, mask, ack_key=0x68, ping_key=0x6D, hello_key=0x5B, ack_style="short"):
    _, nr = await layouts_from_mask(mask)
    typ = await classify(frame)
    if typ == "HELLO":
        if ack_style == "echo":
            content = frame["content"] if frame["content"] else b"\x10\x00\x00\x00"
            return typ, await build_packet(hello_key, nr, 1, 1, None, 1, content, key)
        return typ, await build_packet(ack_key, nr, 0, 2, None, 1, b"\x01\x00", key)
    if typ == "ACK":
        content = frame["content"] if frame["content"] else b"\x01\x00"
        return typ, await build_packet(ack_key, nr, 0, 2, None, 1, content, key)
    if typ == "PING":
        c = frame["content"]
        counter = c[:4] if len(c) >= 4 else c
        return typ, await build_packet(ping_key, nr, 0, 3, None, 0, counter + b"\x00\x00\x00", key, encrypted=False)
    if typ == "JOIN_MATCH":
        return typ, await build_packet(ack_key, nr, 0, 2, None, 1, b"\x02\x00", key)
    return typ, None

async def keepalive_ping(sock, ip, port, key_bytes, mask, stop_event):
    nr = (await layouts_from_mask(mask))[1]
    ping_keys = [0x66, 0x6D, 0x69, 0x6C, 0x6B, 0x6E, 0x6F, 0x70]
    loop = asyncio.get_event_loop()
    i = 0
    while not stop_event.is_set():
        pk = ping_keys[i % len(ping_keys)]
        counter = int(time.time() * 1000) & 0xFFFFFFFF
        pkt = await build_packet(
            pk, nr, 0, 3, None, 0, struct.pack("<I", counter) + b"\x00\x00\x00",
            key_bytes, encrypted=False
        )
        try:
            await loop.sock_sendto(sock, pkt, (ip, port))
        except Exception:
            pass
        i += 1
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=bypass_packet_jitter(3.0, 0.4))
        except asyncio.TimeoutError:
            pass

async def try_header(buf, layout, k, v80):
    off = 2
    out = {}
    for code in layout:
        size = _FIELD_SIZES[code]
        if off + size > len(buf):
            return None
        out[_FIELD_NAMES[code]] = (
            (buf[off] ^ k) if size == 1
            else (((buf[off] | (buf[off + 1] << 8)) ^ v80) & 0xFFFF)
        )
        off += size
    out["headerLen"] = off
    return out

async def oicq_unpad(padded):
    if not padded or len(padded) < 8:
        return None
    if not all(padded[-1 - i] == 0 for i in range(7)):
        return None
    pad_len = padded[0] & 0x07
    s = 3 + pad_len
    e = len(padded) - 7
    return padded[s:e] if s < e else b""

async def decode_packet(packet, key, mask=None):
    data = bytes(packet) if isinstance(packet, bytes) else bytes.fromhex(packet)
    if len(data) < 8:
        return None
    k = key[0]
    v80 = ((k << 8) | k) & 0xFFFF
    crc_ok = (data[1] & 0x7F) == await crc7_buff(0, data[2:])
    candidates = []
    if mask:
        ru, nr = await layouts_from_mask(mask)
        layouts = [("RUDP", ru), ("nonRUDP", nr)]
        if nr != [0, 1, 4, 3]:
            layouts.append(("nonRUDP", [0, 1, 4, 3]))
    else:
        layouts = [("RUDP", list(p)) for p in itertools.permutations([0, 1, 2, 3, 4])]
        layouts += [("nonRUDP", list(p)) for p in itertools.permutations([0, 1, 3, 4])]
    for kind, layout in layouts:
        f = await try_header(data, layout, k, v80)
        if not f or f["flags"] > 7 or f["sendOption"] > 7:
            continue
        exact_len = f["length"] == len(data) - f["headerLen"]
        ack_piggy = bool(f["flags"] & 4) and (0 <= f["length"] <= len(data) - f["headerLen"] - 1) and (len(data) - f["headerLen"] - f["length"] <= 32)
        if not (exact_len or ack_piggy):
            continue
        body = data[len(data) - f["length"]:] if f["length"] > 0 else b""
        content = None
        if f["flags"] & 1:
            if len(body) < 8 or len(body) % 8 != 0:
                continue
            padded = await tea_cbc_decrypt(body, key)
            content = await oicq_unpad(padded)
            if content is None:
                continue
        else:
            content = body
        score = (1 if crc_ok else 0) + (1 if exact_len else 0) + (1 if content is not None else 0)
        candidates.append({
            "kind": kind,
            "layout": layout,
            "headerLen": f["headerLen"],
            "msgKey": data[0],
            "cmd": f["cmd"],
            "flags": f["flags"],
            "sendOption": f["sendOption"],
            "orderId": f.get("orderId"),
            "length": f["length"],
            "content": content,
            "crcOk": crc_ok,
            "score": score,
        })
    if not candidates:
        return None
    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates[0]

async def build_match_startup_packets(token, udp_key, match_code, account_id, block_val,
                                      server_ip="", region="BD", client_version="1.132.9",
                                      client_version_code="2019121229", access_token="",
                                      mode_id=BR_MODE_ID, map_id=BR_MAP_ID):
    reg = normalize_region(region)
    token = token.strip()
    udp_key = bytes.fromhex(udp_key)
    match_code = [int(ch) for ch in str(match_code).strip() if ch.isdigit()] or [0, 1, 4, 3, 2]
    thunder_jwt = token[:660] if len(token) > 660 else token
    sharma_jwt = token[660:] if len(token) > 660 else ""
    eth = thunder_jwt.encode() if isinstance(thunder_jwt, str) else thunder_jwt
    esh = sharma_jwt.encode() if isinstance(sharma_jwt, str) else sharma_jwt
    garena420 = await has_ssan_zig(len(eth)) + eth
    csoversea_block = bytes.fromhex(
        "ca0163736f7665727365612e7374726f6e67686f6c642e66726565666972656d6f62696c652e636f6d"
        "3b302e302e302e303b33342e3132362e37362e34353b33342e38372e3137372e31343b33342e38372e"
        "3137302e3233303b33352e3138352e3138332e35370000000000000100000000000000000000000001"
        "00000800000100000000000100a8a2d7bebd8d8bdf110200"
    )
    mid = bytes.fromhex("0000000001000102030101") + await has_ssan_zig(len(reg)) + reg.encode()
    mid += bytes.fromhex("0001030003000004")
    mid += await has_ssan_zig(len(client_version)) + client_version.encode()
    mid += await has_ssan_zig(len(client_version_code)) + client_version_code.encode()
    mid += csoversea_block
    clean_ip = server_ip.split(":")[0] if server_ip else "0.0.0.0"
    mid += await has_ssan_zig(len(clean_ip)) + clean_ip.encode()
    if access_token:
        clean_acc = access_token.strip()
        mid += await has_ssan_zig(len(clean_acc)) + clean_acc.encode()
    mid += await has_ssan_zig(len(esh)) + esh
    tg = (
        await uleb_encode(int(account_id) if str(account_id).isdigit() else 0)
        + await uleb_encode(int(block_val or 0))
        + await uleb_encode(1)
        + await uleb_encode(int(mode_id))
        + await uleb_encode(int(block_val or 0))
        + await uleb_encode(int(map_id))
        + mid
    )
    process = await sv_frame(0x5E, match_code, 2, 447, 0, 1, garena420, udp_key)
    loading = await sv_frame(0x5A, match_code, 2, 448, 1, 1, tg, udp_key)
    return process.hex(), loading.hex()

# ═══════════════════════════ SMART MOVEMENT CONTROLLER (IND + BD) ═══════════════════════════
def _f32_bits(val: float) -> int:
    return struct.unpack("<I", struct.pack("<f", float(val)))[0]

async def build_movement_packet_2001(key_bytes, msg_key, player_state, x, y, z,
                                     tick, counter, move_state, account_uid,
                                     room_code=None, slot_id=1, phase="arena",
                                     angle=0.0, speed=0.0, vel_y=0.0, s1=0, s2=2,
                                     player_match_id=1):
    if room_code:
        _, nr = await layouts_from_mask(room_code)
    else:
        nr = [0, 1, 4, 3]
    pid_val = int(player_match_id) & 0x7F if player_match_id else 1
    body = bytearray(await uleb_encode((1 << 24) | pid_val))
    body += await zigzag_encode_signed(int(round(x)))
    body += await zigzag_encode_signed(int(round(y)))
    body += await zigzag_encode_signed(int(round(z)))
    ca = math.cos(angle)
    sa = math.sin(angle)
    fx = max(-100, min(100, int(round(100.0 * ca))))
    fy = -24 if s1 == 2 else 0
    fz = max(-100, min(100, int(round(100.0 * sa))))
    body += await zigzag_encode_signed(fx)
    body += await zigzag_encode_signed(fy)
    body += await zigzag_encode_signed(fz)
    if s1 in (4, 2):
        mx, mz = 0, 100
    elif s1 == 1 and s2 == 11:
        mx, mz = 0, 0
    elif speed > 1.0:
        mx, mz = fx, fz
    else:
        mx, mz = 0, 0
    body += await zigzag_encode_signed(mx)
    body += await zigzag_encode_signed(mz)
    vx = int(round((speed * ca) / 10.0))
    vy = int(round(vel_y / 10.0))
    vz = int(round((speed * sa) / 10.0))
    body += await zigzag_encode_signed(vx)
    body += await zigzag_encode_signed(vy)
    body += await zigzag_encode_signed(vz)
    body += await uleb_encode(int(s1))
    body += await uleb_encode(int(s2))
    pitch = -0.25
    cp = math.cos(pitch)
    sp = math.sin(pitch)
    body += await uleb_encode(_f32_bits(ca * cp))
    body += await uleb_encode(_f32_bits(sp))
    body += await uleb_encode(_f32_bits(sa * cp))
    body += b"\x00\x00"
    body += struct.pack("<I", int(tick))
    body += await uleb_encode(int(counter) & 0xFFFFFFFF)
    return await build_packet(msg_key, nr, 0, 2001, None, 0, bytes(body), key_bytes, encrypted=False)

class MovementController:
    def __init__(self, account_id, account_region, key, iv,
                 udp_sock=None, udp_server=None, udp_key_bytes=None,
                 match_code=None, slot_id=1):
        self.account_id = int(account_id) if str(account_id).isdigit() else 0
        self.region = normalize_region(account_region)
        self.key = key
        self.iv = iv
        self.udp_sock = udp_sock
        self.udp_server = udp_server
        self.udp_key = udp_key_bytes
        self.match_code = match_code
        self.slot_id = max(1, min(4, int(slot_id))) if slot_id is not None else 1

        self.player_match_id = None
        self.phase = "island"
        self.air_s1 = 4
        self.air_s2 = 0
        self.spawn_x = 5751
        self.spawn_y = 1400160
        self.spawn_z = 1650
        self.ground_y = 1400160
        self.x = float(self.spawn_x)
        self.y = float(self.spawn_y)
        self.z = float(self.spawn_z)
        self.has_real_coords = False
        self.has_real_ground_coords = False
        self.plane_x = None
        self.plane_y = None
        self.plane_z = None

        self.tick = 18
        self.counter = 0
        self.angle = ((self.slot_id - 1) * (math.pi / 2.0)) + random.uniform(-0.3, 0.3)
        self.state = "sprint"
        self.cur_speed = 0.0
        self.vel_y = 0.0
        self.pkt_s1 = 0
        self.pkt_s2 = 2
        self.speed_mul = random.uniform(MOVEMENT_SPEED_MIN, MOVEMENT_SPEED_MAX)
        self._msg_keys = [0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C]
        self._key_idx = 0
        self._stop_evt = asyncio.Event()
        self._clock_stop = asyncio.Event()
        self._task = None
        self._clock_task = None
        self._last_decision = 0.0
        self._last_speed_change = 0.0
        self._last_jump_t = 0.0
        self._jump_start_t = 0.0
        self._last_clock_echo_t = 0.0
        self._start_time = 0.0

    async def _echo_clock_sync(self, raw_tick_bytes: bytes):
        if not self.udp_sock or not self.udp_server or not self.udp_key:
            return
        try:
            loop = asyncio.get_running_loop()
            _, nr = await layouts_from_mask(self.match_code)
            mk = self._msg_keys[self._key_idx % len(self._msg_keys)]
            pkt = await build_packet(mk, nr, 0, 2000, None, 0, raw_tick_bytes, self.udp_key, encrypted=False)
            await loop.sock_sendto(self.udp_sock, pkt, self.udp_server)
            self._last_clock_echo_t = time.time()
        except Exception:
            pass

    def handle_server_frame(self, frame):
        cmd = frame.get("cmd")
        content = frame.get("content")
        if not content:
            return
        try:
            def _dec_v(b, off):
                res = 0
                s = 0
                cur = off
                while cur < len(b):
                    bt = b[cur]
                    res |= (bt & 0x7F) << s
                    cur += 1
                    s += 7
                    if not (bt & 0x80):
                        break
                return res, cur

            def _dec_zz(n):
                return (n >> 1) ^ -(n & 1)

            if cmd == 2000 and len(content) >= 1:
                _, end_off = _dec_v(content, 0)
                if end_off >= 1:
                    asyncio.create_task(self._echo_clock_sync(bytes(content[:end_off])))
                return

            if cmd == 2001 and len(content) >= 15 and content[:2] == b"\x00\x02" and 1 <= content[2] <= 64:
                pid = content[2]
                if self.player_match_id is None:
                    self.player_match_id = pid
                elif pid != self.player_match_id:
                    return
                cur = 3
                vx, cur = _dec_v(content, cur)
                vy, cur = _dec_v(content, cur)
                vz, cur = _dec_v(content, cur)
                zx, zy, zz = _dec_zz(vx), _dec_zz(vy), _dec_zz(vz)
                s1, s2 = 0, 0
                try:
                    for _ in range(8):
                        _, cur = _dec_v(content, cur)
                    s1, cur = _dec_v(content, cur)
                    s2, cur = _dec_v(content, cur)
                except Exception:
                    pass
                now = time.time()
                if zy >= 800000:
                    self.phase = "island"
                    self.ground_y = zy
                    self.spawn_x, self.spawn_y, self.spawn_z = zx, zy, zz
                    self.x, self.y, self.z = float(zx), float(zy), float(zz)
                    self.has_real_coords = True
                    return
                if s1 == 3:
                    self.phase = "plane"
                    self.has_real_coords = True
                    self.plane_x, self.plane_y, self.plane_z = zx, zy, zz
                    self.x, self.y, self.z = float(zx), float(zy), float(zz)
                    return
                if s1 in (4, 2) or (s1 == 1 and s2 == 10 and not self.has_real_ground_coords):
                    self.has_real_coords = True
                    if self.phase != "airborne":
                        self.phase = "airborne"
                        self.x, self.y, self.z = float(zx), float(zy), float(zz)
                    else:
                        self.y = float(zy)
                    self.air_s1 = s1 if s1 in (4, 2) else 2
                    self.air_s2 = s2
                    return
                if zy < 250000:
                    self.phase = "ground"
                    if not self.has_real_ground_coords:
                        self.spawn_x, self.spawn_y, self.spawn_z = zx, zy, zz
                        self.ground_y = zy
                        self.x, self.y, self.z = float(zx), float(zy), float(zz)
                        self.has_real_coords = True
                        self.has_real_ground_coords = True
                        self.state = "sprint"
                        return
                    is_jumping = self.state == "jump" and (now - self._jump_start_t) < 0.85
                    if s1 == 0 and not is_jumping:
                        self.ground_y = zy
                        self.y = float(zy)
                    if math.hypot(self.x - zx, self.z - zz) > 6000.0:
                        self.x, self.z = float(zx), float(zz)
                        if not is_jumping:
                            self.ground_y = zy
                            self.y = float(zy)
                        self.angle = (self.angle + random.uniform(1.8, 4.4)) % (2.0 * math.pi)
        except Exception:
            pass

    def _pick_state(self) -> str:
        r = random.random()
        if r < 0.72:
            return "sprint"
        if r < 0.90:
            return "run"
        return "walk"

    def _step_position(self, dt):
        now = time.time()
        elapsed = now - self._start_time if self._start_time > 0 else 0.0
        if elapsed > 45.0 and self.phase in ("init", "island", "plane") and not self.has_real_ground_coords:
            slot_off = (self.slot_id - 1) * 800
            bx = self.plane_x if self.plane_x is not None else self.spawn_x
            bz = self.plane_z if self.plane_z is not None else self.spawn_z
            self.spawn_x = bx + slot_off
            self.spawn_z = bz + slot_off
            self.spawn_y = 9229
            self.ground_y = 9229
            self.x, self.y, self.z = float(self.spawn_x), float(self.spawn_y), float(self.spawn_z)
            self.phase = "ground"
            self.has_real_coords = True
            self.has_real_ground_coords = True

        if self.phase in ("init", "island"):
            self.tick = 18
            self.ground_y = self.spawn_y
            self.y = float(self.ground_y)
            self.vel_y = 0.0
            speed = 5600.0 * self.speed_mul
            self.pkt_s1, self.pkt_s2 = 1, 11
            self.cur_speed = speed
            self.x += math.cos(self.angle) * speed * dt
            self.z += math.sin(self.angle) * speed * dt
            return

        if self.phase == "airborne":
            self.cur_speed = 6200.0
            self.vel_y = -11800.0
            self.pkt_s1, self.pkt_s2 = self.air_s1, 0
            self.tick = 17
            self.x += math.cos(self.angle) * self.cur_speed * dt
            self.z += math.sin(self.angle) * self.cur_speed * dt
            self.y += self.vel_y * dt
            return

        self.tick = 18
        if self.state == "jump":
            j_prog = (now - self._jump_start_t) / 0.85
            if 0.0 <= j_prog < 1.0:
                self.y = float(self.ground_y) + 698.0 * 4.0 * j_prog * (1.0 - j_prog)
                self.vel_y = 3285.0 * (1.0 - 2.0 * j_prog)
                self.pkt_s1, self.pkt_s2 = 1, 11
                speed = 5550.0
            else:
                self.y = float(self.ground_y)
                self.vel_y = -3300.0
                self.pkt_s1, self.pkt_s2 = 1, 0
                self.state = "sprint"
                speed = 5600.0
        else:
            self.y = float(self.ground_y)
            self.vel_y = 0.0
            if self.state == "walk":
                speed = 3400.0 * self.speed_mul
                self.pkt_s1, self.pkt_s2 = 0, 1
            elif self.state in ("run", "sprint"):
                speed = 5600.0 * self.speed_mul
                self.pkt_s1, self.pkt_s2 = 1, 11
            else:
                speed = 0.0
                self.pkt_s1, self.pkt_s2 = 0, 0

        self.cur_speed = speed
        if speed > 0.0:
            self.x += math.cos(self.angle) * speed * dt
            self.z += math.sin(self.angle) * speed * dt

    async def _send_udp(self):
        if not self.udp_sock or not self.udp_server or not self.udp_key or self.phase == "plane":
            return False
        try:
            loop = asyncio.get_running_loop()
            time_ms = int((time.time() - self._start_time) * 1000) & 0xFFFFFFFF
            mk = self._msg_keys[self._key_idx % len(self._msg_keys)]
            self._key_idx += 1
            pkt = await build_movement_packet_2001(
                self.udp_key, mk, PLAYER_STATE_MAP.get(self.state, 1),
                self.x, self.y, self.z, self.tick, time_ms, MOVE_STATE_MAP.get(self.state, 2),
                self.account_id, room_code=self.match_code, slot_id=self.slot_id,
                phase=self.state, angle=self.angle, speed=self.cur_speed,
                vel_y=self.vel_y, s1=self.pkt_s1, s2=self.pkt_s2,
                player_match_id=self.player_match_id or 1
            )
            await loop.sock_sendto(self.udp_sock, pkt, self.udp_server)
            return True
        except Exception:
            return False

    async def _clock_sync_loop(self):
        if not self.udp_sock or not self.udp_server or not self.udp_key:
            return
        loop = asyncio.get_running_loop()
        _, nr = await layouts_from_mask(self.match_code)
        tick_val = 60
        try:
            await asyncio.sleep(2.5)
            while not self._clock_stop.is_set():
                try:
                    if (time.time() - self._last_clock_echo_t) > 4.5:
                        body = await uleb_encode(tick_val)
                        pkt = await build_packet(0x68, nr, 0, 2000, None, 0, body, self.udp_key, encrypted=False)
                        await loop.sock_sendto(self.udp_sock, pkt, self.udp_server)
                        tick_val = (tick_val + 60) & 0xFFFFFFFF
                    await asyncio.wait_for(self._clock_stop.wait(), timeout=2.0)
                    break
                except asyncio.TimeoutError:
                    pass
                except asyncio.CancelledError:
                    break
        except asyncio.CancelledError:
            pass

    async def _loop(self):
        self._start_time = time.time()
        await asyncio.sleep(1.0)
        interval = MOVEMENT_TICK_MS / 1000.0
        last_t = time.time()
        self._last_jump_t = last_t
        self._last_decision = last_t
        self._last_speed_change = last_t
        while not self._stop_evt.is_set():
            now = time.time()
            dt = now - last_t
            last_t = now
            if dt <= 0.0 or dt > 0.25:
                dt = interval
            if self.phase == "ground":
                if self.state != "jump" and (now - self._last_jump_t) >= random.uniform(3.8, 6.2):
                    self._last_jump_t = now
                    self._jump_start_t = now
                    self.state = "jump"
                if self.state != "jump" and (now - self._last_decision) >= random.uniform(3.0, 5.5):
                    self.state = self._pick_state()
                    self.angle = (self.angle + random.uniform(-0.9, 0.9)) % (2.0 * math.pi)
                    self._last_decision = now
                if now - self._last_speed_change >= MOVEMENT_UPDATE_SPEED_EVERY:
                    self.speed_mul = random.uniform(MOVEMENT_SPEED_MIN, MOVEMENT_SPEED_MAX)
                    self._last_speed_change = now
            if self.phase != "plane":
                self._step_position(dt)
                await self._send_udp()
            try:
                await asyncio.wait_for(self._stop_evt.wait(), timeout=interval)
            except asyncio.TimeoutError:
                pass

    def start(self):
        if self._task and not self._task.done():
            return
        self._stop_evt.clear()
        self._clock_stop.clear()
        self._task = asyncio.create_task(self._loop())
        self._clock_task = asyncio.create_task(self._clock_sync_loop())

    async def stop(self):
        self._stop_evt.set()
        self._clock_stop.set()
        for t in (self._task, self._clock_task):
            if t:
                try:
                    await asyncio.wait_for(t, timeout=2.5)
                except Exception:
                    t.cancel()

async def send_anti_afk_fire(sock, addr, udp_key_bytes, match_code, account_id):
    try:
        _, nr = await layouts_from_mask(match_code)
        pid = int(account_id) if str(account_id).isdigit() else 0
        ts = int(time.time() * 1000) & 0xFFFFFFFF
        wid = random.choice([101, 102, 103, 201, 202])
        fire = struct.pack("<IIHB", pid & 0xFFFFFFFF, ts, wid, 1)
        fp = await build_packet(0x68, nr, 0, 104, None, 0, fire, udp_key_bytes, encrypted=False)
        loop = asyncio.get_running_loop()
        await loop.sock_sendto(sock, fp, addr)
        await asyncio.sleep(bypass_jitter(random.uniform(0.15, 0.30), 0.05))
        stop = struct.pack("<IIHB", pid & 0xFFFFFFFF, ts + 200, wid, 0)
        sp = await build_packet(0x68, nr, 0, 105, None, 0, stop, udp_key_bytes, encrypted=False)
        await loop.sock_sendto(sock, sp, addr)
        return True
    except Exception:
        return False

async def anti_afk_worker(sock, ip, port, udp_key_bytes, match_code, account_id, stop_event, match_index):
    addr = (ip, port)
    try:
        await asyncio.sleep(bypass_jitter(2.5, 0.5))
        while not stop_event.is_set():
            try:
                await send_anti_afk_fire(sock, addr, udp_key_bytes, match_code, account_id)
                w = bypass_packet_jitter(random.uniform(ANTI_AFK_MIN_INTERVAL, ANTI_AFK_MAX_INTERVAL), 0.25)
                try:
                    await asyncio.wait_for(stop_event.wait(), timeout=w)
                    break
                except asyncio.TimeoutError:
                    pass
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(1.0)
    except asyncio.CancelledError:
        pass

# ═══════════════════════════ UDP MATCH GAMEPLAY ═══════════════════════════
async def play_game(server_ip_port, thunder, sharma, udp_key, match_code,
                    account_id, player_region, client_version, key, iv,
                    match_index, slot_id=1, on_match_complete=None):
    reg = normalize_region(player_region)
    t0 = time.time()
    ping_task = anti_task = None
    sock = None
    ping_stop = asyncio.Event()
    anti_stop = asyncio.Event()
    movement_ctrl = None
    uid_str = str(account_id)
    completed = False
    try:
        ip, port = server_ip_port.split(":")
        port = int(port)
        rip = await resolve_host_cloudflare(ip)
        loop = asyncio.get_running_loop()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.bind(("0.0.0.0", 0))
        except Exception:
            pass
        optimize_udp_socket(sock)
        sock.setblocking(False)
        udp_key_bytes = bytes.fromhex(udp_key)
        await asyncio.sleep(bypass_hello_delay())
        hello = await build_hello_packet(f"{account_id}_2585", udp_key_bytes, match_code)
        await loop.sock_sendto(sock, bytes.fromhex(hello), (rip, port))

        ack_state = "waiting_for_hello_reply"
        thunder_sent = False
        join_match_rcv = False
        local_closed = False
        send_lock = asyncio.Lock()
        anti_started = False
        ping_task = asyncio.create_task(keepalive_ping(sock, rip, port, udp_key_bytes, match_code, ping_stop))
        last_activity = time.time()

        movement_ctrl = MovementController(
            account_id=account_id,
            account_region=reg,
            key=key,
            iv=iv,
            udp_sock=sock,
            udp_server=(rip, port),
            udp_key_bytes=udp_key_bytes,
            match_code=match_code,
            slot_id=slot_id,
        )

        async def start_workers():
            nonlocal anti_task, anti_started
            if anti_started:
                return
            anti_started = True
            anti_task = asyncio.create_task(anti_afk_worker(
                sock, rip, port, udp_key_bytes, match_code, account_id, anti_stop, match_index
            ))
            if ENABLE_SPEED_MOVEMENT and movement_ctrl:
                movement_ctrl.start()

        async def send_startup():
            nonlocal ack_state, thunder_sent
            if thunder_sent:
                return
            async with send_lock:
                if thunder_sent:
                    return
                try:
                    await loop.sock_sendto(sock, bytes.fromhex(thunder), (rip, port))
                    thunder_sent = True
                    await asyncio.sleep(bypass_jitter(0.12, 0.05))
                    _, nr = await layouts_from_mask(match_code)
                    ack = await build_packet(0x68, nr, 0, 2, None, 1, b"\x01\x00", udp_key_bytes)
                    await loop.sock_sendto(sock, ack, (rip, port))
                    await asyncio.sleep(bypass_jitter(0.22, 0.05))
                    await loop.sock_sendto(sock, bytes.fromhex(sharma), (rip, port))
                    ack_state = "thunder_sharma_sent"
                    await start_workers()
                except Exception as e:
                    print_error(f"[{reg} MATCH #{match_index}] startup: {e}", uid_str)

        while not local_closed:
            if time.time() - t0 > MAX_MATCH_DURATION:
                completed = True
                break
            try:
                resp, saddr = await asyncio.wait_for(loop.sock_recvfrom(sock, 65535), timeout=1.5)
                if resp:
                    last_activity = time.time()
                    frame = await decode_packet(resp, udp_key_bytes, match_code)
                    if frame:
                        if movement_ctrl:
                            movement_ctrl.handle_server_frame(frame)
                        pt = await classify(frame)
                        if frame["cmd"] in [103, 107]:
                            completed = True
                            local_closed = True
                            continue
                        if frame["cmd"] == 101:
                            try:
                                _, nr = await layouts_from_mask(match_code)
                                a = await build_packet(0x68, nr, 0, 2, None, 1, b"\x01\x00", udp_key_bytes)
                                await loop.sock_sendto(sock, a, saddr)
                            except Exception:
                                pass
                            continue
                        if pt in ["ACK", "PING", "HELLO", "JOIN_MATCH"]:
                            if pt == "HELLO" and ack_state == "waiting_for_hello_reply":
                                _, r = await reply_for(frame, udp_key_bytes, match_code, ack_style="short")
                                if r:
                                    await loop.sock_sendto(sock, r, saddr)
                                ack_state = "ack_sent_waiting"
                            elif pt == "ACK":
                                if ack_state == "waiting_for_hello_reply":
                                    _, r = await reply_for(frame, udp_key_bytes, match_code)
                                    if r:
                                        await loop.sock_sendto(sock, r, saddr)
                                    ack_state = "ready_to_send_thunder"
                                elif ack_state == "ack_sent_waiting":
                                    ack_state = "ready_to_send_thunder"
                                else:
                                    _, r = await reply_for(frame, udp_key_bytes, match_code)
                                    if r:
                                        await loop.sock_sendto(sock, r, saddr)
                            elif pt == "PING":
                                _, r = await reply_for(frame, udp_key_bytes, match_code)
                                if r:
                                    await loop.sock_sendto(sock, r, saddr)
                            elif pt == "JOIN_MATCH" and not join_match_rcv:
                                _, r = await reply_for(frame, udp_key_bytes, match_code)
                                if r:
                                    await loop.sock_sendto(sock, r, saddr)
                                join_match_rcv = True
            except asyncio.TimeoutError:
                if ack_state in ("ready_to_send_thunder", "ack_sent_waiting") and not thunder_sent:
                    await send_startup()
                elif ack_state == "waiting_for_hello_reply":
                    if (time.time() - last_activity) > 7.0:
                        try:
                            hp = await build_hello_packet(f"{account_id}_2585", udp_key_bytes, match_code)
                            await loop.sock_sendto(sock, bytes.fromhex(hp), (rip, port))
                        except Exception:
                            pass
                        last_activity = time.time()
                    if (time.time() - t0) > 25.0:
                        break
                elif ack_state == "thunder_sharma_sent":
                    if (time.time() - last_activity) > MATCH_IDLE_TIMEOUT:
                        completed = True
                        break
                continue
            except BlockingIOError:
                await asyncio.sleep(0.05)
            except OSError:
                await asyncio.sleep(0.5)
                continue
            except Exception:
                await asyncio.sleep(0.5)
                continue
            if ack_state == "ready_to_send_thunder" and not thunder_sent:
                try:
                    await send_startup()
                except Exception:
                    pass
        return f"match #{match_index} finished"
    except Exception as e:
        print_error(f"[{reg} MATCH #{match_index}] {e}", uid_str)
        return f"match #{match_index} error"
    finally:
        if movement_ctrl:
            try:
                await movement_ctrl.stop()
            except Exception:
                pass
        if completed:
            try:
                bot_state.increment_match(uid_str)
            except Exception:
                pass
            if on_match_complete:
                try:
                    asyncio.create_task(on_match_complete())
                except Exception:
                    pass
        anti_stop.set()
        if anti_task:
            try:
                await asyncio.wait_for(anti_task, timeout=2.0)
            except Exception:
                anti_task.cancel()
                try:
                    await anti_task
                except Exception:
                    pass
        ping_stop.set()
        if ping_task:
            ping_task.cancel()
            try:
                await ping_task
            except asyncio.CancelledError:
                pass
        if sock:
            try:
                sock.close()
            except Exception:
                pass
        rem = await _dec_match(uid_str)
        try:
            bot_state.update_status(uid_str, "IN_MATCH" if rem > 0 else "ONLINE", rem)
        except Exception:
            pass

# ═══════════════════════════ FRIEND & TEAM INVITE HANDLERS ═══════════════════════════
def _wrap_manual(inner):
    try:
        alt = decode_protobuf_2(inner)
        if alt and len(alt) > 0:
            return {str(k): {"data": v} for k, v in alt.items()}
    except Exception:
        pass
    return None

async def _process_social_packet(raw_bytes, account_data, tag="MAIN"):
    try:
        hex_data = raw_bytes.hex()
        candidates = []
        if len(raw_bytes) >= 6:
            plen = raw_bytes[4]
            if 0 < plen <= (len(raw_bytes) - 5):
                try:
                    inner = bytes(raw_bytes[5:5 + plen])
                    d0 = decode_protobuf_dict_safe(inner) or _wrap_manual(inner)
                    if d0:
                        candidates.append((5, d0))
                except Exception:
                    pass
        for off in [5, 6, 10, 8, 12, 4, 0]:
            if off >= len(hex_data):
                continue
            try:
                inner = bytes.fromhex(hex_data[off:])
            except Exception:
                continue
            decoded = decode_protobuf_dict_safe(inner) or _wrap_manual(inner)
            if decoded:
                candidates.append((off, decoded))
        if not candidates:
            return
        candidates.sort(key=lambda x: len(x[1]) if isinstance(x[1], dict) else 0, reverse=True)
        _, decoded = candidates[0]

        def _v(c, k):
            if not isinstance(c, dict):
                return None
            v = c.get(k) if k in c else c.get(str(k))
            if isinstance(v, dict) and "data" in v:
                return v["data"]
            return v

        f5w = decoded.get("5") or decoded.get(5) if isinstance(decoded, dict) else None
        f5 = f5w["data"] if isinstance(f5w, dict) and "data" in f5w else f5w
        target = None
        if isinstance(f5, dict):
            for fk in [1, 2, 3, 4, 6]:
                c = _v(f5, fk)
                if c and str(c).isdigit() and 6 <= len(str(c)) <= 15:
                    target = str(c)
                    break
        if not target:
            return
        own = str(account_data.get("account_id", "")) if account_data else ""
        if own and target == own:
            return
        if not _accept_friend_request or not account_data:
            return
        jwt = account_data.get("token")
        srv = account_data.get("server_url")
        rel = account_data.get("release_version")
        own_id = account_data.get("account_id")
        if not (jwt and srv and rel and own_id):
            return
        url = f"{srv.rstrip('/')}/ConfirmFriendRequest"
        fields = {"1": int(target), "2": int(own_id)}
        try:
            payload = bytes.fromhex(encrypt_api(create_proto(fields).hex()))
            hdrs = {
                "authorization": f"Bearer {jwt}",
                "host": srv.replace("https://", "").replace("http://", "").split("/")[0],
                "x-ga": "v1 1",
                "content-type": "application/x-www-form-urlencoded",
                "accept-encoding": "deflate, gzip",
                "releaseversion": str(rel),
                "user-agent": "UnityPlayer/2022.3.47f1",
                "accept": "*/*",
                "x-unity-version": "2022.3.47f1",
            }
            async with httpx.AsyncClient(verify=False, timeout=8.0) as s:
                r = await s.post(url, headers=hdrs, content=payload)
                if r.status_code == 200 and len(r.content) > 0:
                    print_success(f"👥 [FRIEND-{tag}] ✅ {target}", str(own_id))
        except Exception:
            pass
    except Exception:
        pass

async def _handle_team_invite(hex_data, pl, uid_str, current_account_data,
                              current_key, current_iv, writer, runtime=None,
                              region="BD", game_version="1.132.9"):
    reg = normalize_region(region)
    try:
        candidates = []
        for off in [10, 8, 6, 12, 14, 4, 16, 0, 20, 2]:
            if off >= len(hex_data) or len(hex_data) - off < 4:
                continue
            try:
                inner = bytes.fromhex(hex_data[off:])
            except Exception:
                continue
            dec = decode_protobuf_dict_safe(inner)
            if dec and isinstance(dec, dict) and len(dec) > 0:
                candidates.append((off, "parser", dec))
                continue
            alt = _wrap_manual(inner)
            if alt and len(alt) > 0:
                candidates.append((off, "manual", alt))
        if not candidates:
            return False
        candidates.sort(key=lambda x: len(x[2]) if isinstance(x[2], dict) else 0, reverse=True)
        _, _, dec = candidates[0]

        def _unwrap(d, keys):
            if not isinstance(d, dict):
                return None
            for k in keys:
                v = d.get(k) if k in d else d.get(str(k))
                if isinstance(v, dict) and "data" in v:
                    return v["data"]
                if isinstance(v, dict):
                    return v
            return None

        target_dict = None
        for kp in [["5"], ["4"], ["6"], ["2"], ["1"]]:
            u = _unwrap(dec, kp)
            if isinstance(u, dict) and len(u) >= 3:
                target_dict = u
                break
        if target_dict is None:
            target_dict = dec

        def _g(d, k):
            if not isinstance(d, dict):
                return None
            v = d.get(k) if k in d else d.get(str(k))
            if isinstance(v, dict) and "data" in v:
                return v["data"]
            if isinstance(v, dict):
                for kk in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                    vv = v.get(kk) if kk in v else v.get(int(kk))
                    if isinstance(vv, dict) and "data" in vv:
                        return vv["data"]
            return v

        group_id = None
        for k in list(target_dict.keys()):
            c = _g(target_dict, k)
            if isinstance(c, str) and 10 <= len(c) <= 64 and not c.isdigit():
                group_id = c
                break
        if not group_id:
            for k in list(dec.keys()):
                c = _g(dec, k)
                if isinstance(c, str) and 10 <= len(c) <= 64 and not c.isdigit():
                    group_id = c
                    break

        own_acc = str(current_account_data.get("account_id")) if current_account_data else None
        inviter = None
        all_f = list(target_dict.keys()) + list(dec.keys())
        for k in all_f:
            c = _g(target_dict, k) or _g(dec, k)
            if c and str(c).isdigit() and 6 <= len(str(c)) <= 15:
                if str(c) != uid_str and str(c) != own_acc:
                    inviter = str(c)
                    break

        if inviter and group_id and runtime:
            is_member = runtime.leader_uid != uid_str
            if is_member:
                async with runtime.members_lock:
                    already = uid_str in runtime.members_joined
                if already:
                    return True
                accepted = False
                for _ in range(3):
                    try:
                        acc = accept_team_invite(
                            int(inviter), group_id, current_key, current_iv,
                            region=reg, game_version=game_version
                        )
                        if writer and not writer.is_closing():
                            writer.write(acc)
                            await writer.drain()
                            accepted = True
                            break
                    except Exception:
                        pass
                    await asyncio.sleep(0.8)
                if accepted:
                    await runtime.member_join(uid_str)
                return True
        return False
    except Exception:
        return False

# ═══════════════════════════ PER-SQUAD MAIN LOOP (IND + BD) ═══════════════════════════
async def functional_battle_royale(runtime: SquadRuntime, addrs, starter_packet, account_region,
                                    client_version, key, iv, account_id="", account_data=None,
                                    account_level=2, max_reconnects=10):
    sid = runtime.squad_id
    reg = normalize_region(account_region or runtime.region)
    reconnects = 0
    ip, port = addrs.split(":")
    play_matches: List[asyncio.Task] = []
    no_response_count = 0
    search_attempts = 0
    uid_str = str(account_id)
    current_level = int(account_level or 2)
    current_token = starter_packet
    current_key = key
    current_iv = iv
    current_account_data = account_data
    reconnect_count_total = 0
    _writer_ref = {"w": None}
    _team_active = {"flag": True}
    solo_search_started = False
    solo_match_active = False
    solo_last_search = 0.0

    async def _start_solo_search(reason="team formation failed"):
        nonlocal solo_search_started, solo_last_search
        if not runtime.solo_fallback or solo_match_active:
            return
        now = time.monotonic()
        if solo_search_started and now - solo_last_search < MATCH_SEARCH_TIMEOUT:
            return
        writer = _writer_ref["w"]
        if not writer or writer.is_closing():
            return
        try:
            await start_game_battle_royale(
                reg, client_version, writer, current_key, current_iv
            )
            solo_search_started = True
            solo_last_search = now
            bot_state.squad_log(
                sid,
                f"🎮 [{reg}] {uid_str} started SOLO matchmaking ({reason})",
                "success"
            )
        except Exception as solo_error:
            bot_state.squad_log(
                sid,
                f"[{reg}] {uid_str} solo matchmaking send failed: {solo_error}",
                "error"
            )

    async def trigger_post_match_refresh():
        await asyncio.sleep(EXP_REFRESH_AFTER_MATCH_DELAY)
        try:
            f = bot_state.account_credentials.get(uid_str)
            if f:
                await refresh_account_profile(f)
        except Exception:
            pass

    async def _team_coordinator():
        try:
            deadline = time.time() + 25.0
            while time.time() < deadline:
                async with runtime.lock:
                    n = len(runtime.peers)
                if n >= TEAM_SIZE:
                    break
                if not runtime.is_running or bot_state.is_paused(uid_str):
                    return
                await asyncio.sleep(0.5)

            async with runtime.lock:
                n = len(runtime.peers)
                is_leader = runtime.leader_uid == uid_str
                peers_snapshot = dict(runtime.peers)

            if not is_leader:
                return
            if n < TEAM_SIZE:
                bot_state.squad_log(sid, f"[{reg}] {n}/{TEAM_SIZE} peers ready — forming squad", "warning")

            await asyncio.sleep(TEAM_READY_DELAY)
            async with runtime.lock:
                runtime.team_code = None
                runtime.pk_code = None

            own_id_num = None
            if current_account_data:
                own_id_num = current_account_data.get("account_id")
            if not own_id_num and str(uid_str).isdigit():
                own_id_num = int(uid_str)
            own_id_num = own_id_num or 0

            try:
                pkt = create_team(current_key, current_iv, client_version, region=reg)
                if _writer_ref["w"] and not _writer_ref["w"].is_closing():
                    _writer_ref["w"].write(pkt)
                    await _writer_ref["w"].drain()
                    await runtime.reset_members(keep_leader=False)
                    await runtime.member_join(uid_str)
            except Exception:
                pass

            await asyncio.sleep(TEAM_CREATE_WAIT)

            peer_uids = []
            for peer_uid, info in peers_snapshot.items():
                if peer_uid == uid_str:
                    continue
                pa = None
                try:
                    pa = info["data"].get("account_id")
                except Exception:
                    pass
                target_id = pa or peer_uid
                if str(target_id).isdigit():
                    peer_uids.append(int(target_id))

            heartbeat_stop = asyncio.Event()

            async def heartbeat_loop():
                while not heartbeat_stop.is_set():
                    try:
                        if _writer_ref["w"] and not _writer_ref["w"].is_closing():
                            pkt = team_fresh(int(own_id_num), current_key, current_iv, region=reg)
                            _writer_ref["w"].write(pkt)
                            await _writer_ref["w"].drain()
                    except Exception:
                        pass
                    try:
                        await asyncio.wait_for(heartbeat_stop.wait(), timeout=TEAM_HEARTBEAT_INTERVAL)
                    except asyncio.TimeoutError:
                        pass

            hb_task = asyncio.create_task(heartbeat_loop())

            invite_start = time.time()
            while time.time() - invite_start < TEAM_INVITE_MAX_TIME:
                if not _team_active["flag"] or not runtime.is_running or bot_state.is_paused(uid_str):
                    break
                cnt = await runtime.member_count()
                if cnt >= min(TEAM_SIZE, len(peers_snapshot)):
                    break
                for tuid in peer_uids:
                    async with runtime.members_lock:
                        joined = str(tuid) in runtime.members_joined
                    if joined:
                        continue
                    try:
                        inv = invite_player_in_team(tuid, current_key, current_iv, region=reg)
                        if _writer_ref["w"] and not _writer_ref["w"].is_closing():
                            _writer_ref["w"].write(inv)
                            await _writer_ref["w"].drain()
                    except Exception:
                        pass
                    await asyncio.sleep(0.4)
                try:
                    await asyncio.wait_for(heartbeat_stop.wait(), timeout=TEAM_INVITE_CYCLE_WAIT)
                except asyncio.TimeoutError:
                    pass

            final_cnt = await runtime.member_count()
            bot_state.squad_log(
                sid,
                f"[{reg}] Squad formation result: {final_cnt}/{TEAM_SIZE} members joined",
                "info"
            )
            if final_cnt < TEAM_SIZE or n < TEAM_SIZE:
                runtime.solo_fallback = True
                bot_state.squad_log(
                    sid,
                    f"⚠️ [{reg}] Team formation failed — all accounts switching to SOLO matchmaking",
                    "warning"
                )
                heartbeat_stop.set()
                if hb_task and not hb_task.done():
                    hb_task.cancel()
                    try:
                        await hb_task
                    except asyncio.CancelledError:
                        pass
                await _start_solo_search("team incomplete")
                return

            bot_state.squad_log(
                sid,
                f"[{reg}] Squad ready ({final_cnt}/{TEAM_SIZE}) — starting team match loop",
                "success"
            )
            await asyncio.sleep(TEAM_FINAL_WAIT)
            heartbeat_stop.set()
            if hb_task and not hb_task.done():
                hb_task.cancel()
                try:
                    await hb_task
                except asyncio.CancelledError:
                    pass
                except Exception as hb_error:
                    bot_state.squad_log(
                        sid,
                        f"[{reg}] Team heartbeat stopped with warning: {hb_error}",
                        "warning"
                    )

            # Leader alone requests matchmaking; keep the existing squad.
            bot_state.squad_log(
                sid,
                f"👑 [{reg}] Leader coordinator active for {uid_str}; entering matchmaking loop",
                "success"
            )
            match_cycles = 0
            while _team_active["flag"] and runtime.is_running and not bot_state.is_paused(uid_str):
                if runtime.solo_fallback:
                    await _start_solo_search("team formation failed")
                    await asyncio.sleep(1.0)
                    continue
                if runtime.match_in_progress:
                    await asyncio.sleep(0.5)
                    continue
                try:
                    async with runtime.lock:
                        if runtime.leader_uid != uid_str:
                            break
                    writer = _writer_ref["w"]
                    if not writer or writer.is_closing():
                        bot_state.squad_log(
                            sid,
                            f"[{reg}] Leader gateway not ready; waiting to send matchmaking",
                            "warning"
                        )
                        await asyncio.sleep(1.0)
                        continue
                    oid = current_account_data.get("account_id", own_id_num) if current_account_data else own_id_num
                    if not str(oid).isdigit() or int(oid) <= 0:
                        oid = own_id_num
                    if not str(oid).isdigit() or int(oid) <= 0:
                        bot_state.squad_log(sid, f"[{reg}] Leader account ID invalid; cannot start matchmaking", "error")
                        await asyncio.sleep(3.0)
                        continue
                    match_cycles += 1
                    writer.write(ready_for_game(int(oid), current_key, current_iv, region=reg))
                    await writer.drain()
                    bot_state.squad_log(sid, f"🙋 [{reg}] Leader {oid} sent Ready (cycle #{match_cycles})", "info")
                    await asyncio.sleep(2.0)
                    if runtime.match_in_progress:
                        continue
                    writer.write(start_match_team(int(oid), current_key, current_iv, region=reg))
                    await writer.drain()
                    bot_state.squad_log(sid, f"🚀 [{reg}] Leader {oid} sent StartMatch (cycle #{match_cycles})", "success")
                except asyncio.CancelledError:
                    raise
                except Exception as e:
                    bot_state.squad_log(sid, f"[{reg}] Leader matchmaking send error: {e}", "warning")
                await asyncio.sleep(max(START_MATCH_INTERVAL, 5.0))
        except asyncio.CancelledError:
            raise
        except Exception as e:
            bot_state.squad_log(sid, f"[{reg}] Coordinator error: {e}", "error")
            runtime.solo_fallback = True
            bot_state.squad_log(
                sid,
                f"⚠️ [{reg}] Team coordinator failed — switching all accounts to SOLO matchmaking",
                "warning"
            )
            await _start_solo_search("team coordinator error")

    async def _member_match_trigger():
        try:
            await asyncio.sleep(TEAM_READY_DELAY + TEAM_MEMBER_START_DELAY)
            async with runtime.lock:
                if runtime.leader_uid == uid_str:
                    return
            my_id = current_account_data.get("account_id", uid_str) if current_account_data else uid_str
            last_ready_at = 0.0
            while _team_active["flag"] and runtime.is_running and not bot_state.is_paused(uid_str):
                if runtime.solo_fallback:
                    await _start_solo_search("team formation failed")
                    await asyncio.sleep(1.0)
                    continue
                if runtime.match_in_progress:
                    await asyncio.sleep(0.5)
                    continue
                try:
                    writer = _writer_ref["w"]
                    if writer and not writer.is_closing() and str(my_id).isdigit():
                        if time.time() - last_ready_at >= max(START_MATCH_INTERVAL, 5.0):
                            writer.write(ready_for_game(int(my_id), current_key, current_iv, region=reg))
                            await writer.drain()
                            last_ready_at = time.time()
                            bot_state.squad_log(sid, f"🙋 [{reg}] Member {my_id} sent Ready", "info")
                except asyncio.CancelledError:
                    raise
                except Exception as e:
                    bot_state.squad_log(sid, f"[{reg}] Member Ready send error ({uid_str}): {e}", "warning")
                await asyncio.sleep(1.0)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            bot_state.squad_log(sid, f"[{reg}] Member Ready trigger error ({uid_str}): {e}", "warning")

    try:
        while runtime.is_running:
            while bot_state.is_paused(uid_str):
                bot_state.update_status(uid_str, "PAUSED", 0)
                await asyncio.sleep(1.0)

            writer = None
            gateway_ping_task = None
            team_coord_task = None
            member_trigger_task = None
            try:
                if current_account_data:
                    fresh = None
                    if current_account_data.get("auth_type") == "guest" and current_account_data.get("auth_uid"):
                        fresh = cache_get(str(current_account_data["auth_uid"]))
                    elif current_account_data.get("auth_type") == "token" and current_account_data.get("auth_token"):
                        fresh = cache_get(f"tok_{current_account_data['auth_token'][:20]}")
                    if fresh and normalize_region(fresh.get("region", reg)) == reg:
                        current_account_data = fresh
                        current_key = fresh["aes_ak"]
                        current_iv = fresh["iv_i"]
                        current_token = await build_tcp_startup_packet(
                            fresh["account_id"], fresh["token"], fresh["server_time"],
                            current_key, current_iv, region=reg, typ="OnLine"
                        )
                        try:
                            lv = int(fresh.get("level", current_level) or current_level)
                            if lv != current_level:
                                current_level = lv
                        except Exception:
                            pass
                    else:
                        try:
                            if current_account_data.get("auth_uid"):
                                cache_invalidate(str(current_account_data["auth_uid"]))
                            if current_account_data.get("auth_token"):
                                cache_invalidate(f"tok_{current_account_data['auth_token'][:20]}")
                            new_cred = await relogin_account(uid_str, current_account_data, region_override=reg)
                            if new_cred:
                                current_account_data = new_cred
                                current_key = new_cred["aes_ak"]
                                current_iv = new_cred["iv_i"]
                                current_token = await build_tcp_startup_packet(
                                    new_cred["account_id"], new_cred["token"], new_cred["server_time"],
                                    current_key, current_iv, region=reg, typ="OnLine"
                                )
                            else:
                                raise ConnectionError("Re-login returned empty credentials")
                        except Exception:
                            await asyncio.sleep(5)
                            raise ConnectionError("Cache expired")

                rip = await resolve_host_cloudflare(ip)
                reader, writer = await asyncio.open_connection(rip, int(port))
                bot_state.register_writer(uid_str, writer)
                _writer_ref["w"] = writer
                raw_sock = writer.get_extra_info("socket")
                if raw_sock:
                    optimize_tcp_socket(raw_sock)
                await asyncio.sleep(bypass_hello_delay())
                writer.write(bytes.fromhex(current_token))
                await writer.drain()
                try:
                    ka = await send_keep_alive(reg)
                    if ka and not writer.is_closing():
                        writer.write(ka)
                        await asyncio.wait_for(writer.drain(), timeout=3)
                except Exception:
                    pass

                async def func_gateway_keepalive():
                    ka_bytes = await send_keep_alive(reg)
                    while True:
                        await asyncio.sleep(bypass_ka_jitter(5.0))
                        try:
                            if writer and not writer.is_closing():
                                writer.write(ka_bytes)
                                await writer.drain()
                        except Exception:
                            break

                gateway_ping_task = asyncio.create_task(func_gateway_keepalive())

                connection_start_time = asyncio.get_running_loop().time()
                last_watchdog_check = connection_start_time
                search_attempts = 0
                bot_state.squad_log(sid, f"🔗 [{reg}] TCP connected {uid_str} Lvl{current_level}", "info")
                reconnects = 0
                no_response_count = 0

                async with runtime.lock:
                    runtime.peers[uid_str] = {
                        "writer": writer,
                        "data": current_account_data,
                        "key": current_key,
                        "iv": current_iv,
                    }
                    if runtime.leader_uid is None:
                        runtime.leader_uid = uid_str
                        bot_state.squad_log(sid, f"👑 [{reg}] Leader: {uid_str}", "success")

                if TEAM_MODE:
                    team_coord_task = asyncio.create_task(_team_coordinator())
                    member_trigger_task = asyncio.create_task(_member_match_trigger())
                else:
                    await start_game_battle_royale(reg, client_version, writer, current_key, current_iv)

                while runtime.is_running:
                    play_matches[:] = [m for m in play_matches if not m.done()]
                    if bot_state.is_paused(uid_str):
                        break
                    active = await _get_match_count(uid_str)
                    try:
                        bot_state.update_status(uid_str, "ONLINE" if active == 0 else "IN_MATCH", active)
                    except Exception:
                        pass

                    now = asyncio.get_running_loop().time()
                    if not TEAM_MODE and now - last_watchdog_check >= MATCH_WATCHDOG_CHECK:
                        last_watchdog_check = now
                        if now - connection_start_time > MATCH_SEARCH_TIMEOUT:
                            raise ConnectionError("Search watchdog")
                    if search_attempts >= MAX_SEARCH_ATTEMPTS:
                        raise ConnectionError("Max attempts")

                    try:
                        data = await asyncio.wait_for(reader.read(8192), timeout=0.5)
                    except asyncio.TimeoutError:
                        no_response_count += 1
                        if TEAM_MODE:
                            if no_response_count > TEAM_IDLE_ITERS_TEAM:
                                raise ConnectionError("Team idle timeout")
                        else:
                            if no_response_count > 80:
                                raise ConnectionError("idle")
                        continue

                    if not data:
                        raise ConnectionError("closed")
                    hex_data = data.hex()
                    pl = len(data)
                    no_response_count = 0

                    if hex_data.startswith("0600") and pl > 20:
                        await _process_social_packet(data, current_account_data, tag="MAIN")
                        continue

                    if hex_data.startswith("05") and pl > 10:
                        await _handle_team_invite(
                            hex_data, pl, uid_str, current_account_data,
                            current_key, current_iv, writer, runtime,
                            region=reg, game_version=client_version
                        )
                        continue

                    if hex_data.startswith("0300") and 10 < pl < 30:
                        continue

                    if hex_data.startswith("0300") and pl >= 300:
                        # Match found: keep the squad coordinator and member Ready
                        # loops alive. They pause while match_in_progress is True
                        # and resume automatically after all squad members finish.
                        try:
                            res = json.loads(await decode_protobuf(hex_data[10:]))
                            token = udp_key = match_code = server_ip_port = None
                            match_account_id = block_val = None
                            if "42" in res and "data" in res["42"]:
                                match_code = res["42"]["data"]
                            if "5" in res and "data" in res["5"]:
                                r5 = res["5"]["data"]
                                server_ip_port = r5.get("2", {}).get("data")
                                udp_key = r5.get("3", {}).get("data")
                                token = r5.get("4", {}).get("data")
                                block_val = r5.get("1", {}).get("data")
                                if "42" in r5:
                                    match_code = r5["42"]["data"]
                            if "1" in res and "data" in res["1"]:
                                match_account_id = res["1"]["data"]

                            effective = match_account_id or account_id or f"{reg}_BOT"
                            if token and udp_key and match_code and server_ip_port:
                                if runtime.solo_fallback:
                                    if solo_match_active:
                                        bot_state.squad_log(
                                            sid,
                                            f"[{reg}] Duplicate SOLO Match Found packet ignored for {uid_str}",
                                            "warning"
                                        )
                                        continue
                                    solo_match_active = True
                                else:
                                    async with runtime.match_lock:
                                        if uid_str in runtime.match_started_uids:
                                            bot_state.squad_log(sid, f"[{reg}] Duplicate Match Found packet ignored for {uid_str}", "warning")
                                            continue
                                        if not runtime.match_in_progress:
                                            async with runtime.lock:
                                                runtime.match_expected_uids = set(runtime.peers.keys()) or {uid_str}
                                            runtime.match_started_uids.clear()
                                            runtime.match_completed_uids.clear()
                                            runtime.match_in_progress = True
                                        runtime.match_started_uids.add(uid_str)
                                async with runtime.lock:
                                    runtime.pk_code = str(match_code)
                                bot_state.squad_log(sid, f"🎯 [{reg}] Match found | Room: {match_code} | Server: {server_ip_port}", "success")
                                acc_tok = current_account_data.get("access_token", "") if current_account_data else ""
                                thunder, sharma = await build_match_startup_packets(
                                    token, udp_key, match_code, effective, block_val or 0,
                                    server_ip=server_ip_port, region=reg,
                                    client_version=client_version, access_token=acc_tok,
                                    mode_id=BR_MODE_ID, map_id=BR_MAP_ID
                                )
                                match_index = await _inc_match(uid_str)
                                runtime.match_count += 1
                                bot_state.increment_match_started()
                                bot_state.squad_log(sid, f"🎮 [{reg}] Match #{match_index} starting UDP...", "info")

                                slot_num = bot_state.accounts.get(uid_str, {}).get("slot", 1)
                                new_match = asyncio.create_task(play_game(
                                    server_ip_port, thunder, sharma, udp_key, match_code,
                                    effective, reg, client_version,
                                    current_key, current_iv,
                                    match_index=match_index, slot_id=slot_num,
                                    on_match_complete=trigger_post_match_refresh
                                ))
                                play_matches.append(new_match)

                                async def drain_gw():
                                    while not new_match.done():
                                        try:
                                            dg = await asyncio.wait_for(reader.read(4096), timeout=1.0)
                                            if not dg:
                                                break
                                            gh = dg.hex()
                                            if gh.startswith("0600") and len(dg) > 20:
                                                await _process_social_packet(dg, current_account_data, tag="DRAIN")
                                        except asyncio.TimeoutError:
                                            continue
                                        except Exception:
                                            break

                                drain_task = asyncio.create_task(drain_gw())
                                try:
                                    await new_match
                                except Exception as e:
                                    bot_state.squad_log(sid, f"[{reg}] Match error: {e}", "error")
                                finally:
                                    drain_task.cancel()
                                    try:
                                        await drain_task
                                    except asyncio.CancelledError:
                                        pass
                                play_matches[:] = [m for m in play_matches if not m.done()]

                                if runtime.solo_fallback:
                                    solo_match_active = False
                                    solo_search_started = False
                                    solo_last_search = 0.0
                                    bot_state.squad_log(
                                        sid,
                                        f"✅ [{reg}] {uid_str} SOLO match finished — starting next solo queue",
                                        "success"
                                    )
                                else:
                                    async with runtime.match_lock:
                                        runtime.match_completed_uids.add(uid_str)
                                        expected = runtime.match_expected_uids or {uid_str}
                                        if runtime.match_completed_uids.issuperset(expected):
                                            finished_count = len(runtime.match_completed_uids)
                                            runtime.match_in_progress = False
                                            runtime.match_expected_uids.clear()
                                            runtime.match_started_uids.clear()
                                            runtime.match_completed_uids.clear()
                                            async with runtime.lock:
                                                runtime.pk_code = None
                                            bot_state.squad_log(
                                                sid,
                                                f"✅ [{reg}] Match finished ({finished_count}/{len(expected)} accounts) — same squad retained; leader/member Ready loops resumed",
                                                "success"
                                            )
                                # Do not close the gateway or remove this member here.
                                # Keeping the session alive preserves the current in-game team.
                                continue
                            else:
                                await safe_close_writer(writer)
                                await asyncio.sleep(NON_MATCH_RECONNECT_DELAY)
                                break
                        except Exception as e:
                            bot_state.squad_log(sid, f"[{reg}] Parse error: {e}", "error")
                            await safe_close_writer(writer)
                            await asyncio.sleep(NON_MATCH_RECONNECT_DELAY)
                            break

                    if 30 <= pl <= 40:
                        continue

            except asyncio.CancelledError:
                for m in play_matches:
                    if not m.done():
                        m.cancel()
                if play_matches:
                    await asyncio.gather(*play_matches, return_exceptions=True)
                play_matches.clear()
                if gateway_ping_task:
                    gateway_ping_task.cancel()
                async with runtime.lock:
                    runtime.peers.pop(uid_str, None)
                    if runtime.leader_uid == uid_str:
                        runtime.leader_uid = None
                await runtime.member_leave(uid_str)
                raise
            except Exception as e:
                bot_state.squad_log(sid, f"⚠️ [{reg}] {uid_str} TCP drop ({e}) — reconnecting", "warning")
                if gateway_ping_task:
                    gateway_ping_task.cancel()
                play_matches[:] = [m for m in play_matches if not m.done()]
                if writer:
                    bot_state.unregister_writer(uid_str, writer)
                    await safe_close_writer(writer)
                if "Cache expired" in str(e):
                    break
                reconnect_count_total += 1
                reconnects += 1
                if reconnects > max_reconnects:
                    reconnects = 0
                    await asyncio.sleep(3)
                    continue
                await asyncio.sleep(bypass_human_reconnect_delay(reconnects))
            finally:
                _team_active["flag"] = False
                for tk in (team_coord_task, member_trigger_task):
                    if tk and not tk.done():
                        tk.cancel()
                        try:
                            await tk
                        except (asyncio.CancelledError, Exception):
                            pass
                if gateway_ping_task:
                    gateway_ping_task.cancel()
                if writer:
                    bot_state.unregister_writer(uid_str, writer)
                    await safe_close_writer(writer)
                async with runtime.lock:
                    runtime.peers.pop(uid_str, None)
                    if runtime.leader_uid == uid_str:
                        runtime.leader_uid = None
                await runtime.member_leave(uid_str)
                _team_active["flag"] = True
    except asyncio.CancelledError:
        for m in play_matches:
            if not m.done():
                m.cancel()
        if play_matches:
            await asyncio.gather(*play_matches, return_exceptions=True)
        play_matches.clear()
        raise

# ═══════════════════════════ INFORMATIONAL CHAT TCP ═══════════════════════════
async def informational(addrs, starter_packet, key, iv, region="BD", max_reconnects=3, account_id=""):
    reg = normalize_region(region)
    uid_str = str(account_id)
    reconnects = 0
    ip, port = addrs.split(":")
    while True:
        while uid_str and bot_state.is_paused(uid_str):
            await asyncio.sleep(1.0)
        writer = None
        ping_task = None
        try:
            rip = await resolve_host_cloudflare(ip)
            reader, writer = await asyncio.open_connection(rip, int(port))
            if uid_str:
                bot_state.register_writer(uid_str, writer)
            rs = writer.get_extra_info("socket")
            if rs:
                optimize_tcp_socket(rs)
            writer.write(bytes.fromhex(starter_packet))
            await writer.drain()
            reconnects = 0
            try:
                ka = await send_keep_alive(reg)
                if ka and not writer.is_closing():
                    writer.write(ka)
                    await asyncio.wait_for(writer.drain(), timeout=3)
            except Exception:
                pass

            async def info_ka():
                ka_bytes = await send_keep_alive(reg)
                while True:
                    await asyncio.sleep(bypass_ka_jitter(5.0))
                    try:
                        if writer and not writer.is_closing():
                            writer.write(ka_bytes)
                            await writer.drain()
                    except Exception:
                        break

            ping_task = asyncio.create_task(info_ka())
            while True:
                data = await reader.read(8192)
                if not data:
                    raise ConnectionError("closed")
        except asyncio.CancelledError:
            if ping_task:
                ping_task.cancel()
            if uid_str and writer:
                bot_state.unregister_writer(uid_str, writer)
            await safe_close_writer(writer)
            raise
        except Exception:
            if ping_task:
                ping_task.cancel()
            if uid_str and writer:
                bot_state.unregister_writer(uid_str, writer)
            await safe_close_writer(writer)
            reconnects += 1
            if reconnects > max_reconnects:
                await asyncio.sleep(3)
                reconnects = 0
            else:
                await asyncio.sleep(1)

# ═══════════════════════════ AUTO GUILD JOIN ENGINE (IND + BD) ═══════════════════════════
_guild_ssl = ssl.create_default_context()
_guild_ssl.check_hostname = False
_guild_ssl.verify_mode = ssl.CERT_NONE

def _guild_get(url, timeout=20):
    req = urllib.request.Request(url, method="GET", headers={
        "User-Agent": GUILD_UA,
        "Accept": "application/json, text/plain, */*",
        "Connection": "close",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_guild_ssl) as r:
            return True, r.status, r.read().decode("utf-8", "replace"), url, None
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", "replace")
        except Exception:
            body = ""
        return False, e.code, body, url, None
    except Exception as e:
        return False, 0, "", url, str(e)

def _guild_call(endpoints, guild_id, uid, pwd):
    last = (False, 0, "", endpoints[0])
    for ep in endpoints:
        q = urllib.parse.urlencode({"guild_id": guild_id, "uid": uid, "password": pwd})
        ok, code, body, used, _ = _guild_get(f"{ep}?{q}")
        if ok:
            return True, code, body, used
        last = (False, code, body, used)
    return last

def guild_do_join(g, u, p):
    return _guild_call(GUILD_JOIN_ENDPOINTS, g, u, p)

def guild_do_leave(g, u, p):
    return _guild_call(GUILD_LEAVE_ENDPOINTS, g, u, p)

def guild_call_with_retry(fn, gid, uid, pwd, max_retries=3):
    backoff = 0.6
    last = (False, 0, "", "")
    for attempt in range(max_retries + 1):
        try:
            ok, code, body, ep = fn(gid, uid, pwd)
            last = (ok, code, body, ep)
            if ok:
                return ok, code, body, ep, attempt
            if code == 429 or (500 <= code < 600):
                time.sleep(backoff + random.uniform(0, 0.3))
                backoff *= 2
                continue
            return ok, code, body, ep, attempt
        except Exception as e:
            last = (False, 0, str(e), "")
            time.sleep(backoff)
            backoff *= 2
    return (*last, max_retries)

async def join_clan_proto(jwt_token: str, clan_id: str, region: str = "IND", release_version: str = "OB55") -> Tuple[bool, str]:
    reg = normalize_region(region)
    if not str(clan_id or "").isdigit():
        return False, "Invalid clan_id"
    try:
        if _CLAN_PB_AVAILABLE:
            msg = reqClan_pb2.MyMessage()
            msg.field_1 = int(clan_id)
            raw_pb = msg.SerializeToString()
        else:
            raw_pb = create_proto({1: int(clan_id)})
        payload = AES.new(AES_KEY, AES.MODE_CBC, AES_IV).encrypt(pad(raw_pb, AES.block_size))
        base_url = get_region_api_base(reg)
        url = f"{base_url.rstrip('/')}/RequestJoinClan"
        hdrs = {
            "Authorization": f"Bearer {jwt_token}",
            "X-Unity-Version": "2022.3.47f1",
            "X-GA": "v1 1",
            "ReleaseVersion": str(release_version or "OB55"),
            "Content-Type": "application/octet-stream",
            "Host": base_url.replace("https://", "").replace("http://", ""),
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        r = await client.post(url, headers=hdrs, content=payload, timeout=12.0)
        if r.status_code == 200:
            return True, f"Clan {clan_id} ({reg}) HTTP 200"
        return False, f"Clan {clan_id} ({reg}) HTTP {r.status_code}"
    except Exception as e:
        return False, str(e)[:100]

async def auto_join_guild_or_clan(guild_id: str, clan_id: str, uid: str, password: str,
                                 region: str = "BD", jwt_token: str = "",
                                 release_version: str = "OB55", squad_id: int = 0) -> bool:
    reg = normalize_region(region)
    gid = str(guild_id or DEFAULT_GUILD_ID or "").strip()
    cid = str(clan_id or (DEFAULT_CLAN_ID if reg == "IND" else "") or "").strip()
    if not gid and cid:
        gid = cid

    if not gid and not cid:
        bot_state.update_guild(str(uid), "SKIPPED", "No guild_id / clan_id")
        return True

    bot_state.update_guild(str(uid), "JOINING", f"{reg} | G:{gid or '-'} C:{cid or '-'}")
    bot_state.squad_log(squad_id, f"🏰 [{reg}] Auto-joining guild/clan for UID {uid}...", "info")

    joined_any = False
    details = []

    if gid:
        ok, code, body, _, _ = await asyncio.to_thread(
            guild_call_with_retry, guild_do_join, gid, str(uid), str(password)
        )
        msg = ""
        try:
            if body:
                j = json.loads(body)
                msg = str(j.get("message") or j.get("msg") or j.get("error") or "")[:100]
        except Exception:
            msg = (body or "")[:100].replace("\n", " ")
        details.append(f"Guild({gid}): HTTP {code} {msg}".strip())
        if ok:
            joined_any = True

    if cid and jwt_token:
        c_ok, c_msg = await join_clan_proto(jwt_token, cid, region=reg, release_version=release_version)
        details.append(f"Clan({cid}): {c_msg}")
        if c_ok:
            joined_any = True

    detail_str = " | ".join(details) if details else "Done"
    if joined_any:
        bot_state.update_guild(str(uid), "JOINED", detail_str[:160])
        print_success(f"🏰 [{reg} GUILD-JOIN] {uid} joined → {detail_str}", str(uid))
        bot_state.squad_log(squad_id, f"✅ [{reg}] Guild/Clan joined ({uid}): {detail_str}", "success")
        return True

    bot_state.update_guild(str(uid), "FAILED", detail_str[:160])
    print_warning(f"🏰 [{reg} GUILD-JOIN] {uid} response: {detail_str}", str(uid))
    bot_state.squad_log(squad_id, f"⚠️ [{reg}] Guild/Clan join response ({uid}): {detail_str}", "warning")
    return False

def guild_encrypt_data(data: bytes) -> bytes:
    return AES.new(FRIEND_AES_KEY, AES.MODE_CBC, FRIEND_AES_IV).encrypt(pad(data, AES.block_size))

def guild_build_friend_request_payload(target_uid: int) -> bytes:
    body = encode_varint(8) + encode_varint(target_uid)
    body += encode_varint(16) + encode_varint(target_uid)
    body += encode_varint(24) + encode_varint(26)
    return body

def guild_jwt_from_external_api(api_url: str, uid: str, password: str, retries: int = 1):
    if _requests is None:
        return None, "requests unavailable"
    err_msg = ""
    for attempt in range(retries + 1):
        try:
            url = f"{api_url}?uid={uid}&password={password}"
            resp = _requests.get(url, timeout=12, verify=True)
            if resp.status_code == 200:
                data = resp.json()
                token = (
                    data.get("token") or data.get("jwt") or data.get("access_token")
                    or data.get("data", {}).get("token") or data.get("data", {}).get("jwt")
                )
                if token and len(token) > 50:
                    return token, None
                err_msg = "API json missing Token"
            else:
                err_msg = f"API HTTP {resp.status_code}"
        except Exception as e:
            err_msg = str(e)[:30]
        if attempt < retries:
            time.sleep(0.3)
    return None, err_msg

def guild_get_jwt(uid: str, password: str, retries: int = 1):
    for mname, url in JWT_API_ENDPOINTS:
        jwt, err = guild_jwt_from_external_api(url, uid, password, retries)
        if jwt:
            return jwt, mname, None
    return None, None, "JWT failed"

def guild_send_friend_request(jwt: str, target_uid: int, region: str = "BD", retries: int = 1):
    if _requests is None:
        return False, 0, "requests unavailable"
    reg = normalize_region(region)
    urls = FRIEND_URLS_BY_REGION.get(reg, FRIEND_URLS_BY_REGION["BD"])
    plain = guild_build_friend_request_payload(target_uid)
    encrypted = guild_encrypt_data(plain)
    hdrs = FRIEND_HEADERS.copy()
    hdrs["Authorization"] = f"Bearer {jwt}"
    last_err = "Max retries"
    last_code = 0
    for target_url in urls:
        for attempt in range(retries + 1):
            try:
                resp = _requests.post(target_url, headers=hdrs, data=encrypted, timeout=10, verify=True)
                if resp.status_code == 200:
                    return True, resp.status_code, None
                last_code = resp.status_code
                last_err = f"HTTP_{resp.status_code}"
            except Exception as e:
                last_err = str(e)[:25]
            if attempt < retries:
                time.sleep(0.2)
        if last_code == 200:
            break
    return False, last_code, last_err

async def guild_run_join_or_leave(jid, guild_id, action, accounts, delay, workers, region="BD"):
    fn = guild_do_join if action == "JOIN" else guild_do_leave
    sem = asyncio.Semaphore(max(1, workers))

    async def one(uid, pwd):
        async with sem:
            try:
                ok, code, body, ep, _ = await asyncio.to_thread(
                    guild_call_with_retry, fn, guild_id, uid, pwd, 3
                )
                msg = ""
                try:
                    if body:
                        j = json.loads(body)
                        msg = str(j.get("message") or j.get("msg") or j.get("error") or "")[:120]
                except Exception:
                    msg = (body or "")[:120].replace("\n", " ")
                detail = f"HTTP {code} | ep={ep.split('/')[-1]}"
                bot_state.add_guild_result(jid, uid, ok, msg, detail)
                bot_state.update_guild(str(uid), "SUCCESS" if ok else "FAILED", detail)
                if ok:
                    print_success(f"🏰 [{region} GUILD-{action}] {uid} OK | {msg}", str(uid))
                else:
                    print_error(f"🏰 [{region} GUILD-{action}] {uid} FAIL | {msg}", str(uid))
            except Exception as e:
                bot_state.add_guild_result(jid, uid, False, str(e), "exception")
            await asyncio.sleep(delay)

    tasks = [asyncio.create_task(one(u, p)) for u, p in accounts]
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    bot_state.finish_guild_job(jid)

async def guild_run_owner_spam(jid, guild_id, owner_uid, accounts, delay, workers, region="BD"):
    sem = asyncio.Semaphore(max(1, workers))

    async def one(uid, pwd):
        async with sem:
            try:
                g_ok, g_code, g_body, _, _ = await asyncio.to_thread(
                    guild_call_with_retry, guild_do_join, guild_id, uid, pwd, 2
                )
                f_status = "Skipped"
                fail_reason = ""
                jwt, _, jwt_err = await asyncio.to_thread(guild_get_jwt, uid, pwd, 1)
                if jwt:
                    ok_f, scode, f_err = await asyncio.to_thread(guild_send_friend_request, jwt, owner_uid, region, 1)
                    if ok_f:
                        f_status = f"Sent ({scode})"
                    else:
                        f_status = f"Fail ({scode})"
                        fail_reason = f"Request: {f_err}"
                else:
                    f_status = "JWT Failed"
                    fail_reason = f"JWT: {jwt_err}"
                extra = f"Guild:{'OK' if g_ok else 'FAIL'} | FR:{f_status}"
                msg = ""
                try:
                    if g_body:
                        j = json.loads(g_body)
                        msg = str(j.get("message") or j.get("msg") or j.get("error") or "")[:120]
                except Exception:
                    msg = (g_body or "")[:120]
                bot_state.add_guild_result(jid, uid, g_ok, msg, extra + (f" | {fail_reason}" if fail_reason else ""))
                bot_state.update_guild(str(uid), "SUCCESS" if g_ok else "FAILED", extra)
            except Exception as e:
                bot_state.add_guild_result(jid, uid, False, str(e), "exception")
            await asyncio.sleep(delay)

    tasks = [asyncio.create_task(one(u, p)) for u, p in accounts]
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    bot_state.finish_guild_job(jid)

# ═══════════════════════════ ACCOUNT LOGIN & PROFILE REFRESH ═══════════════════════════
def _register_credentials(ad):
    try:
        acc_id = str(ad["account_id"])
        bot_state.account_credentials[acc_id] = ad
        if ad.get("auth_uid"):
            bot_state.account_credentials[str(ad["auth_uid"])] = ad
        if ad.get("auth_token"):
            bot_state.account_credentials[f"tok_{ad['auth_token'][:20]}"] = ad
    except Exception:
        pass

async def relogin_account(uid_str, old_account_data, region_override=None):
    if not old_account_data:
        return None
    reg = normalize_region(region_override or old_account_data.get("region") or DEFAULT_REGION)
    if old_account_data.get("auth_type") == "guest":
        u = old_account_data.get("auth_uid")
        p = old_account_data.get("auth_password")
        if u and p:
            return await process_account_uid_pass(str(u), str(p), region_override=reg, _skip_cache=True)
    elif old_account_data.get("auth_type") == "token":
        t = old_account_data.get("auth_token")
        if t:
            return await process_account_token(str(t), region_override=reg, _skip_cache=True)
    return None

async def refresh_account_profile(ad_or_uid):
    try:
        if isinstance(ad_or_uid, str):
            uid = str(ad_or_uid)
            ad = bot_state.account_credentials.get(uid)
        else:
            ad = ad_or_uid
            uid = str(ad.get("account_id")) if ad else "?"
        if not ad:
            return
        url = ad.get("server_url")
        token = ad.get("token")
        rel = ad.get("release_version")
        payload = ad.get("login_payload_data")
        if not (url and token and rel and payload):
            return
        res = await send_getlogin(payload, url, token, rel)
        if not res:
            return
        rp, dd = res
        def _si(v, d):
            try:
                if v is None or v == "":
                    return d
                return int(v)
            except Exception:
                return d
        level = _si(get_proto_field(dd, 6, None), None)
        exp = _si(get_proto_field(dd, 7, None), None)
        likes = _si(get_proto_field(dd, 8, None), None)
        try:
            nick = rp.nickname or get_proto_field(dd, 4, "") or ""
        except Exception:
            nick = ""
        if level is None and exp is None:
            return
        level = level if level is not None else 1
        exp = exp if exp is not None else 0
        likes = likes if likes is not None else 0
        acc_id = str(ad["account_id"])
        bot_state.update_exp(acc_id, exp, level)
        if likes > 0 and acc_id in bot_state.accounts:
            bot_state.accounts[acc_id]["likes"] = likes
        if nick and acc_id in bot_state.accounts:
            bot_state.accounts[acc_id]["nickname"] = nick
        _update_cache_profile(ad, level, exp)
        ad["level"] = level
        ad["exp"] = exp
        if likes > 0:
            ad["likes"] = likes
        if nick:
            ad["nickname"] = nick
    except Exception:
        pass

async def process_account_uid_pass(uid, password, region_override=None, _skip_cache=False):
    reg = normalize_region(region_override)
    if not _skip_cache:
        cached = cache_get(uid)
        if cached and normalize_region(cached.get("region", reg)) == reg:
            acc_id = str(cached["account_id"])
            bot_state.register_account(
                uid=acc_id,
                nickname=cached.get("nickname", f"Player_{acc_id}"),
                region=reg,
                level=cached.get("level", 1),
                exp=cached.get("exp", 0),
                likes=cached.get("likes", 0),
                password=password,
                token=cached.get("token"),
                auth_uid=str(uid),
            )
            _register_credentials(cached)
            return cached
        if cached:
            cache_invalidate(uid)

    try:
        async with _LOGIN_SEMAPHORE:
            vc = await version_config(reg)
            if not vc:
                return None
            rel, cv, su = vc
            tg = await get_access_token(uid, password)
            if not tg:
                return None
            oid, at, pf = tg
            dev = get_device_for_account(uid)
            lpd = await build_majorlogin_payload(oid, at, pf, cv, dev, region=reg)
            if not lpd:
                return None
            mresp = await send_majorlogin(lpd, rel, su)
            if mresp is None:
                return None
            gl = await send_getlogin(lpd, mresp.url, mresp.token, rel)
            if gl is None:
                return None
            rp, dd = gl
            acc_id = str(mresp.account_id)
            level = int(get_proto_field(dd, 6, 1) or 1)
            exp = int(get_proto_field(dd, 7, 0) or 0)
            likes = int(get_proto_field(dd, 8, 0) or 0)
            nick = rp.nickname or get_proto_field(dd, 4, f"Player_{acc_id}")
            detected_reg = normalize_region(mresp.region or get_proto_field(dd, 3, reg))
            bot_state.register_account(
                uid=acc_id,
                nickname=nick,
                region=detected_reg,
                level=level,
                exp=exp,
                likes=likes,
                password=password,
                token=mresp.token,
                auth_uid=str(uid),
            )
            ad = {
                "account_id": mresp.account_id,
                "nickname": nick,
                "region": detected_reg,
                "level": level,
                "exp": exp,
                "likes": likes,
                "open_id": oid,
                "access_token": at,
                "platform": str(pf),
                "token": mresp.token,
                "server_time": mresp.server_time,
                "aes_ak": mresp.aes_ak,
                "iv_i": mresp.iv_i,
                "functional_addrs": rp.functional_addrs or get_proto_field(dd, 14),
                "informational_addrs": rp.informational_addrs or get_proto_field(dd, 32),
                "release_version": rel,
                "client_version": cv,
                "server_url": mresp.url,
                "login_payload_data": lpd,
                "auth_type": "guest",
                "auth_uid": str(uid),
                "auth_password": str(password),
            }
            _register_credentials(ad)
            cache_set(uid, ad)
            return ad
    except Exception as e:
        print_error(f"process_account_uid_pass ({reg}): {e}")
        return None

async def process_account_token(access_token, region_override=None, _skip_cache=False):
    reg = normalize_region(region_override)
    cache_key = f"tok_{access_token[:20]}"
    if not _skip_cache:
        cached = cache_get(cache_key)
        if cached and normalize_region(cached.get("region", reg)) == reg:
            acc_id = str(cached["account_id"])
            bot_state.register_account(
                uid=acc_id,
                nickname=cached.get("nickname", f"Player_{acc_id}"),
                region=reg,
                level=cached.get("level", 1),
                exp=cached.get("exp", 0),
                likes=cached.get("likes", 0),
                token=cached.get("token"),
            )
            _register_credentials(cached)
            return cached
    try:
        vc = await version_config(reg)
        if not vc or _requests is None:
            return None
        rel, cv, su = vc
        url = f"https://100067.connect.garena.com/oauth/token/inspect?token={access_token}"
        hdrs = {"User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)"}
        resp = await asyncio.to_thread(_requests.get, url, headers=hdrs, timeout=10)
        d = resp.json()
        if "error" in d:
            return None
        oid = d.get("open_id")
        pf = d.get("platform", 4)
        if not oid:
            return None
        dev = get_device_for_account(oid)
        lpd = await build_majorlogin_payload(oid, access_token, str(pf), cv, dev, region=reg)
        if not lpd:
            return None
        mresp = await send_majorlogin(lpd, rel, su)
        if mresp is None:
            return None
        gl = await send_getlogin(lpd, mresp.url, mresp.token, rel)
        if gl is None:
            return None
        rp, dd = gl
        acc_id = str(mresp.account_id)
        level = int(get_proto_field(dd, 6, 1) or 1)
        exp = int(get_proto_field(dd, 7, 0) or 0)
        likes = int(get_proto_field(dd, 8, 0) or 0)
        nick = rp.nickname or get_proto_field(dd, 4, f"Player_{acc_id}")
        detected_reg = normalize_region(mresp.region or get_proto_field(dd, 3, reg))
        bot_state.register_account(
            uid=acc_id,
            nickname=nick,
            region=detected_reg,
            level=level,
            exp=exp,
            likes=likes,
            token=mresp.token,
        )
        ad = {
            "account_id": mresp.account_id,
            "nickname": nick,
            "region": detected_reg,
            "level": level,
            "exp": exp,
            "likes": likes,
            "open_id": oid,
            "access_token": access_token,
            "platform": str(pf),
            "token": mresp.token,
            "server_time": mresp.server_time,
            "aes_ak": mresp.aes_ak,
            "iv_i": mresp.iv_i,
            "functional_addrs": rp.functional_addrs or get_proto_field(dd, 14),
            "informational_addrs": rp.informational_addrs or get_proto_field(dd, 32),
            "release_version": rel,
            "client_version": cv,
            "server_url": mresp.url,
            "login_payload_data": lpd,
            "auth_type": "token",
            "auth_token": access_token,
        }
        _register_credentials(ad)
        cache_set(cache_key, ad)
        return ad
    except Exception as e:
        print_error(f"process_account_token ({reg}): {e}")
        return None

# ═══════════════════════════ ACCOUNT WORKER & LOOP ═══════════════════════════
async def run_account_worker(runtime: SquadRuntime, ad, label):
    acc_id = str(ad["account_id"])
    reg = normalize_region(ad.get("region") or runtime.region)
    info_task = None
    exp_task = None
    ping_task = None
    try:
        tcp_online = await build_tcp_startup_packet(
            ad["account_id"], ad["token"], ad["server_time"],
            ad["aes_ak"], ad["iv_i"], region=reg, typ="OnLine"
        )
        tcp_chat = await build_tcp_startup_packet(
            ad["account_id"], ad["token"], ad["server_time"],
            ad["aes_ak"], ad["iv_i"], region=reg, typ="ChaT"
        )
        if ad.get("informational_addrs"):
            info_task = asyncio.create_task(informational(
                ad["informational_addrs"], tcp_chat, ad["aes_ak"], ad["iv_i"],
                region=reg, account_id=acc_id
            ))
        if ENABLE_HTTP_PING:
            ping_task = asyncio.create_task(ping_worker(acc_id, ad["token"], ad["release_version"], region=reg))

        async def exp_refresher():
            try:
                f = bot_state.account_credentials.get(acc_id)
                if f:
                    await refresh_account_profile(f)
            except Exception:
                pass
            while True:
                await asyncio.sleep(EXP_REFRESH_INTERVAL + random.uniform(-3.0, 3.0))
                try:
                    f = bot_state.account_credentials.get(acc_id)
                    if f:
                        await refresh_account_profile(f)
                except Exception:
                    pass

        exp_task = asyncio.create_task(exp_refresher())
        await functional_battle_royale(
            runtime,
            ad["functional_addrs"],
            tcp_online,
            reg,
            ad["client_version"],
            ad["aes_ak"],
            ad["iv_i"],
            account_id=acc_id,
            account_data=ad,
            account_level=int(ad.get("level", 2) or 2),
        )
    except asyncio.CancelledError:
        raise
    except Exception as e:
        bot_state.squad_log(runtime.squad_id, f"[{reg}] Account worker error {label}: {e}", "error")
    finally:
        for t in (info_task, exp_task, ping_task):
            if t and not t.done():
                t.cancel()
        for t in (info_task, exp_task, ping_task):
            if t:
                try:
                    await t
                except Exception:
                    pass

async def account_loop_guest(runtime: SquadRuntime, uid, password, region="BD", guild_id="", clan_id=""):
    reg = normalize_region(region or runtime.region)
    guild_joined_once = False
    while runtime.is_running:
        try:
            while bot_state.is_paused(str(uid)):
                bot_state.update_status(str(uid), "PAUSED")
                await asyncio.sleep(1.0)

            bot_state.update_status(str(uid), "CONNECTING")
            bot_state.squad_log(runtime.squad_id, f"🔐 [{reg}] Logging in {uid}...", "info")
            ad = await process_account_uid_pass(uid, password, region_override=reg)
            if not ad:
                bot_state.update_status(str(uid), "ERROR")
                bot_state.squad_log(runtime.squad_id, f"❌ [{reg}] Login failed {uid}", "error")
                await asyncio.sleep(10)
                continue

            acc_id = str(ad["account_id"])
            bot_state.auth_to_game_id[str(uid)] = acc_id
            bot_state.game_to_auth_id[acc_id] = str(uid)
            bot_state.squad_log(runtime.squad_id, f"✅ [{reg}] Logged in {uid} ({ad.get('nickname', '?')})", "success")

            if AUTO_JOIN_GUILD_ENABLED and AUTO_JOIN_GUILD_BEFORE_MATCH and not guild_joined_once:
                target_gid = str(guild_id or bot_state.accounts.get(acc_id, {}).get("guild_id") or DEFAULT_GUILD_ID or "").strip()
                target_cid = str(clan_id or bot_state.accounts.get(acc_id, {}).get("clan_id") or "").strip()
                await auto_join_guild_or_clan(
                    guild_id=target_gid,
                    clan_id=target_cid,
                    uid=uid,
                    password=password,
                    region=reg,
                    jwt_token=ad.get("token", ""),
                    release_version=ad.get("release_version", "OB55"),
                    squad_id=runtime.squad_id,
                )
                guild_joined_once = True

            await run_account_worker(runtime, ad, uid)
            await asyncio.sleep(2)
        except asyncio.CancelledError:
            bot_state.update_status(str(uid), "OFFLINE")
            break
        except Exception as e:
            bot_state.update_status(str(uid), "ERROR")
            bot_state.squad_log(runtime.squad_id, f"[{reg}] Worker error {uid}: {e}", "error")
            await asyncio.sleep(8)

# ═══════════════════════════ ACCOUNTS.JSON LOADER (IND + BD) ═══════════════════════════
def load_accounts_from_json(filepath: str = ACCOUNTS_FILE) -> Tuple[List[Dict[str, str]], str]:
    """
    Loads accounts for IND and/or BD from accounts.json.
    Supported formats:
      1) [{"uid": "...", "password": "...", "region": "IND"|"BD", "guild_id": "...", "clan_id": "..."}, ...]
      2) {"region": "BD", "guild_id": "...", "clan_id": "...", "accounts": [...]}
      3) {"uid1": "pass1", "uid2": "pass2"}
    """
    global DEFAULT_GUILD_ID, DEFAULT_CLAN_ID
    if not os.path.exists(filepath):
        sample = [
            {
                "uid": "123456789",
                "password": "your_password_here",
                "region": "BD",
                "guild_id": "",
                "clan_id": "",
            },
            {
                "uid": "987654321",
                "password": "your_password_here",
                "region": "IND",
                "guild_id": "",
                "clan_id": DEFAULT_CLAN_ID,
            },
        ]
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(sample, f, indent=2, ensure_ascii=False)
            print_warning(f"{filepath} পাওয়া যায়নি। IND+BD নমুনা {filepath} ফাইল তৈরি করা হয়েছে — সঠিক UID/Password বসিয়ে আবার চালান।")
        except Exception as e:
            print_error(f"{filepath} তৈরি করা যায়নি: {e}")
        return [], DEFAULT_REGION

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        print_error(f"{filepath} পড়তে সমস্যা হয়েছে: {e}")
        return [], DEFAULT_REGION

    root_region = DEFAULT_REGION
    if isinstance(raw, dict):
        if raw.get("region"):
            root_region = normalize_region(raw.get("region"))
        if isinstance(raw.get("guild_id"), str) and raw.get("guild_id").strip():
            DEFAULT_GUILD_ID = raw.get("guild_id").strip()
        if isinstance(raw.get("clan_id"), str) and raw.get("clan_id").strip():
            DEFAULT_CLAN_ID = raw.get("clan_id").strip()
        if isinstance(raw.get("accounts"), list):
            items = raw["accounts"]
        else:
            items = [{"uid": k, "password": v} for k, v in raw.items() if isinstance(v, str)]
    elif isinstance(raw, list):
        items = raw
    else:
        print_error(f"{filepath} এর ফরম্যাট সঠিক নয়।")
        return [], root_region

    parsed: List[Dict[str, str]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        uid = str(item.get("uid") or item.get("id") or "").strip()
        pw = str(item.get("password") or item.get("pass") or "").strip()
        reg = normalize_region(item.get("region") or root_region)
        gid = str(item.get("guild_id") or DEFAULT_GUILD_ID or "").strip()
        cid = str(item.get("clan_id") or (DEFAULT_CLAN_ID if reg == "IND" else "") or "").strip()
        if uid and pw:
            parsed.append({
                "uid": uid,
                "password": pw,
                "region": reg,
                "guild_id": gid,
                "clan_id": cid,
            })

    return parsed, root_region

# ═══════════════════════════ SQUAD MANAGER (IND + BD) ═══════════════════════════
class SquadManager:
    def __init__(self):
        self.squads: Dict[int, dict] = {}
        self._lock = asyncio.Lock()
        self._counter = 0

    def _allocate_squad_id(self):
        self._counter += 1
        return self._counter

    async def create_squad(self, members: List[Dict[str, str]], region: str = "BD") -> Tuple[bool, str, int]:
        reg = normalize_region(region)
        async with self._lock:
            sid = self._allocate_squad_id()
            runtime = SquadRuntime(sid, region=reg)
            uids = []
            creds = {}
            meta_map = {}
            for m in members:
                uid = str(m.get("uid", "")).strip()
                pw = str(m.get("password", "")).strip()
                m_reg = normalize_region(m.get("region") or reg)
                gid = str(m.get("guild_id") or DEFAULT_GUILD_ID or "").strip()
                cid = str(m.get("clan_id") or (DEFAULT_CLAN_ID if m_reg == "IND" else "") or "").strip()
                if not uid or not pw:
                    continue
                for other_sid, other in self.squads.items():
                    if uid in other["uids"]:
                        return False, f"UID {uid} already in Squad {other_sid}", 0
                uids.append(uid)
                creds[uid] = pw
                meta_map[uid] = {"region": m_reg, "guild_id": gid, "clan_id": cid}
                bot_state.register_account(
                    uid=uid,
                    nickname=f"Player_{uid}",
                    region=m_reg,
                    level=1,
                    exp=0,
                    likes=0,
                    password=pw,
                    guild_id=gid,
                    clan_id=cid,
                    slot=len(uids),
                )
                bot_state.accounts[uid]["squad_id"] = sid
                bot_state.accounts[uid]["status"] = "STOPPED"

            if not uids:
                return False, "No valid accounts", 0

            self.squads[sid] = {
                "runtime": runtime,
                "region": reg,
                "uids": uids,
                "task": None,
                "is_started": False,
                "credentials": creds,
                "meta": meta_map,
            }
            bot_state.squad_log(sid, f"🛡️ [{reg}] Squad {sid} created with {len(uids)} accounts", "success")
            return True, f"[{reg}] Squad {sid} created", sid

    async def start_squad(self, sid: int) -> Tuple[bool, str]:
        async with self._lock:
            if sid not in self.squads:
                return False, "Squad not found"
            squad = self.squads[sid]
            if squad["is_started"]:
                return False, "Already started"
            squad["is_started"] = True
            runtime = squad["runtime"]
            runtime.is_running = True
            runtime.team_active = True

            async def run_all():
                tasks = []
                for uid in squad["uids"]:
                    pw = squad["credentials"].get(uid, "")
                    info = squad.get("meta", {}).get(uid, {})
                    m_reg = normalize_region(info.get("region") or squad.get("region"))
                    gid = info.get("guild_id", DEFAULT_GUILD_ID)
                    cid = info.get("clan_id", "")
                    if pw:
                        t = asyncio.create_task(
                            account_loop_guest(runtime, uid, pw, region=m_reg, guild_id=gid, clan_id=cid)
                        )
                        bot_state.account_workers[uid] = t
                        tasks.append(t)
                if tasks:
                    await asyncio.gather(*tasks, return_exceptions=True)

            squad["task"] = asyncio.create_task(run_all())
            bot_state.squad_log(sid, f"▶️ [{squad['region']}] Squad {sid} started", "success")
            return True, f"[{squad['region']}] Squad {sid} started"

    async def stop_squad(self, sid: int) -> Tuple[bool, str]:
        async with self._lock:
            if sid not in self.squads:
                return False, "Squad not found"
            squad = self.squads[sid]
            runtime = squad["runtime"]
            runtime.is_running = False
            for uid in squad["uids"]:
                t = bot_state.account_workers.pop(uid, None)
                if t:
                    t.cancel()
                    try:
                        await t
                    except Exception:
                        pass
                bot_state.update_status(uid, "STOPPED")
            old_task = squad.get("task")
            if old_task:
                old_task.cancel()
                try:
                    await old_task
                except Exception:
                    pass
            squad["task"] = None
            squad["is_started"] = False
            bot_state.squad_log(sid, f"⏹ [{squad['region']}] Squad {sid} stopped", "warning")
            return True, f"[{squad['region']}] Squad {sid} stopped"

squad_mgr = SquadManager()

# ═══════════════════════════ HEALTH & STATUS API SERVER ═══════════════════════════
async def api_ping(request):
    return aiohttp.web.json_response({
        "pong": True,
        "app": BRAND_NAME,
        "credit": CREDIT_NAME,
        "version": BRAND_VERSION,
        "regions": SUPPORTED_REGIONS,
        "auto_guild_join": AUTO_JOIN_GUILD_ENABLED,
        "active_accounts": len(bot_state.accounts),
        "total_matches": bot_state.total_matches,
    })

async def api_status(request):
    return aiohttp.web.json_response({
        "credit": CREDIT_NAME,
        "brand": BRAND_NAME,
        "version": BRAND_VERSION,
        "uptime_sec": int(time.time() - bot_state.start_time),
        "total_matches": bot_state.total_matches,
        "matches_started": bot_state.matches_started,
        "total_exp_gained": bot_state.total_exp_gained,
        "accounts": list(bot_state.accounts.values()),
        "squads": [
            {
                "id": sid,
                "region": s["region"],
                "is_started": s["is_started"],
                "uids": s["uids"],
            }
            for sid, s in squad_mgr.squads.items()
        ],
    })

async def start_web_server():
    app = aiohttp.web.Application()
    app.router.add_get("/", api_ping)
    app.router.add_get("/health", api_ping)
    app.router.add_get("/api/ping", api_ping)
    app.router.add_get("/api/status", api_status)
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    for attempt in range(5):
        try:
            site = aiohttp.web.TCPSite(runner, WEB_HOST, WEB_PORT)
            await site.start()
            print_info(f"🌐 Health & Status API listening on http://{WEB_HOST}:{WEB_PORT} | Credit: {CREDIT_NAME}")
            break
        except OSError:
            if attempt == 4:
                raise
            await asyncio.sleep(1.0)
    return runner

# ═══════════════════════════ MAIN ENTRYPOINT (IND + BD) ═══════════════════════════
async def main():
    print_banner()
    print_section(f"⚙️  SYSTEM CONFIGURATION  •  CREDIT: {CREDIT_NAME}", Colors.PURPLE)
    print_info(f"👑 Credit          : {CREDIT_NAME}")
    print_info(f"🌏 Supported       : {', '.join(SUPPORTED_REGIONS)} (IND + BD Auto-Routing)")
    print_info(f"🎮 Mode            : AUTO SQUAD + AUTO GUILD/CLAN JOIN + SMART MOVEMENT")
    print_info(f"📁 Accounts File   : {ACCOUNTS_FILE}")
    print_success(f"👥 Squad Size      : {TEAM_SIZE}")
    print_info(f"🏰 Auto Guild Join : {'ENABLED' if AUTO_JOIN_GUILD_ENABLED else 'DISABLED'} (Guild ID: {DEFAULT_GUILD_ID or 'Per-Account'} | IND Clan: {DEFAULT_CLAN_ID or 'Per-Account'})")
    print_info(f"📡 HTTP Ping       : {'ENABLED' if ENABLE_HTTP_PING else 'DISABLED'}")
    print_info(f"🏃 Speed Movement  : {'ENABLED' if ENABLE_SPEED_MOVEMENT else 'DISABLED'}")
    print_info(f"🛡️  Safe Play Mode  : {'ENABLED' if SAFE_PLAY_MODE else 'DISABLED'}")

    if NETWORK_REFERENCE.get("loaded"):
        print_success(
            f"Network reference loaded: {NETWORK_REFERENCE['record_count']} records, "
            f"{len(NETWORK_REFERENCE['domains'])} domains"
        )

    web_runner = None
    try:
        web_runner = await start_web_server()
    except Exception as e:
        print_warning(f"Health web server skipped: {e}")

    accounts, _ = load_accounts_from_json(ACCOUNTS_FILE)
    if not accounts:
        print_warning(f"{ACCOUNTS_FILE} এ কোনো বৈধ অ্যাকাউন্ট পাওয়া যায়নি। ফাইলটি আপডেট করে আবার রান করুন।")
        if web_runner:
            await web_runner.cleanup()
        return

    bot_state.expected_workers = len(accounts)

    # Group accounts by region (BD and IND) and form squads of TEAM_SIZE
    by_region: Dict[str, List[Dict[str, str]]] = {}
    for acc in accounts:
        r = normalize_region(acc.get("region"))
        by_region.setdefault(r, []).append(acc)

    started_squads = 0
    for reg in ["BD", "IND"] + [k for k in by_region.keys() if k not in ("BD", "IND")]:
        reg_accounts = by_region.get(reg, [])
        for idx in range(0, len(reg_accounts), TEAM_SIZE):
            chunk = reg_accounts[idx:idx + TEAM_SIZE]
            ok, msg, sid = await squad_mgr.create_squad(chunk, region=reg)
            if ok and sid:
                s_ok, s_msg = await squad_mgr.start_squad(sid)
                if s_ok:
                    started_squads += 1
                    print_success(f"🚀 {s_msg} ({len(chunk)} bots)")
                else:
                    print_error(f"[{reg}] Squad {sid} start failed: {s_msg}")
            else:
                print_error(f"[{reg}] Squad creation failed: {msg}")

    print_colored(
        f"\n{Colors.BDGREEN}  ✅ {BRAND_NAME} IND+BD bot is running ({started_squads} squad started) • Credit: {CREDIT_NAME}{Colors.ENDC}\n"
    )

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, asyncio.CancelledError):
        print_section(f"🛑 SHUTTING DOWN  •  CREDIT: {CREDIT_NAME}", Colors.BDRED)
        for sid in list(squad_mgr.squads.keys()):
            await squad_mgr.stop_squad(sid)
        pending = [t for t in bot_state.account_workers.values() if t and not t.done()]
        for t in pending:
            t.cancel()
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
        if web_runner:
            try:
                await web_runner.cleanup()
            except Exception:
                pass
        try:
            await client.aclose()
        except Exception:
            pass
        print_success(f"👋 {BRAND_NAME} closed. Goodbye!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_warning("stopped")