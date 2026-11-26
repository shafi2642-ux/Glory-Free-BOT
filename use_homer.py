# -*- coding: utf-8 -*-
# ============================================================
# homor_skill.py — Homor Skill Builder & Controller
# ============================================================

CMD_USE_ACTIVE_SKILL = 248
SKILL_ID_CANDIDATES = [5506, 706, 5505, 5507, 1250]
SKILL_COOLDOWN_SEC = 2.0        # तुरंत दोबारा cast
SKILL_FIRST_DELAY  = 0.8

def _uleb(n):
    if n < 0: n &= 0xFFFFFFFFFFFFFFFF
    out = bytearray()
    while True:
        b = n & 0x7F; n >>= 7
        if n: out.append(b | 0x80)
        else: out.append(b); break
    return bytes(out)

def _sint16(v):
    v = int(v) & 0xFFFF
    if v > 0x7FFF: v -= 0x10000
    return v.to_bytes(2, "little", signed=True)

def _crc16(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) if (crc & 0x8000) else (crc << 1)
            crc &= 0xFFFF
    return crc

class HomorSkill:
    def __init__(self, skill_id=None, cooldown=SKILL_COOLDOWN_SEC, first_delay=SKILL_FIRST_DELAY):
        self.skill_id = int(skill_id) if skill_id else SKILL_ID_CANDIDATES[0]
        self.cooldown = float(cooldown)
        self.first_delay = float(first_delay)
        self._last_cast = 0.0
        self._candidate_idx = 0
        self._accepted_skill = None
        self.target_id = 0
        self._aim = {"x": 0, "y": 0, "z": 0}
        self.fire_count = 0
        self.skill_used = {}

    def rotate_skill_id(self):
        if self._accepted_skill:
            self.skill_id = self._accepted_skill
            return
        self._candidate_idx = (self._candidate_idx + 1) % len(SKILL_ID_CANDIDATES)
        self.skill_id = SKILL_ID_CANDIDATES[self._candidate_idx]

    def mark_accepted(self, skill_id=None):
        if skill_id:
            self._accepted_skill = int(skill_id)
            self.skill_id = int(skill_id)
        else:
            self._accepted_skill = int(self.skill_id)

    def set_aim(self, x=None, y=None, z=None):
        if x is not None: self._aim["x"] = int(x)
        if y is not None: self._aim["y"] = int(y)
        if z is not None: self._aim["z"] = int(z)

    def build_packet_body(self, player_id, tick=0, target_id=0):
        body = bytearray()
        body += _uleb(int(player_id))
        body += _uleb(int(self.skill_id))
        body += _uleb(int(self._aim["x"]))
        body += _uleb(int(self._aim["y"]))
        body += _uleb(int(self._aim["z"]))
        body += _sint16(0); body += _sint16(0); body += _sint16(0)
        tid = int(target_id) if target_id else int(self.target_id or 0)
        body += _uleb(tid)
        body += _crc16(bytes(body)).to_bytes(2, "big")
        return bytes(body)

    def should_cast(self, now, joined_at):
        if joined_at is None: return False
        if (now - joined_at) < self.first_delay: return False
        if (now - self._last_cast) < self.cooldown: return False
        return True

    def mark_cast(self, now, sid=None):
        self._last_cast = now
        self.fire_count += 1
        if sid:
            self.skill_used[sid] = self.skill_used.get(sid, 0) + 1
        if not self._accepted_skill:
            self.rotate_skill_id()