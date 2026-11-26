"""
FREE FIRE UDP 2001 AUTHENTIC MOVEMENT ENGINE (Multi-Bot Ready)
Har bot ke liye alag MoveState + alag auto_move_loop.

v2 — resilient to send errors; aborts gracefully after 50 consecutive
     send failures instead of crashing the whole match.
"""
import math
import time
import random
import struct
import asyncio
import collections
from typing import Dict, Tuple, Optional, List, Any

# ==================== TUNING ====================
AUTO_MOVE_ENABLED         = True
AUTO_MOVE_START_DELAY     = 16.0
AUTO_MOVE_SPAWN_TIMEOUT   = 30.0
AUTO_MOVE_LAND_TIMEOUT    = 8.0
AUTO_MOVE_TICK_INTERVAL   = 0.25
AUTO_MOVE_WALK_SPEED      = 90
AUTO_MOVE_RUN_SPEED       = 140
AUTO_MOVE_RUN_CHANCE      = 0.0
AUTO_MOVE_RADIUS          = 1200
AUTO_MOVE_MIN_LEG         = 300
AUTO_MOVE_TURN_PER_TICK   = 15.0
AUTO_MOVE_PAUSE_RANGE     = (1.5, 3.5)
AUTO_MOVE_RESYNC_DISTANCE = 4000
AUTO_MOVE_PIGGYBACK_ACK   = True
AUTO_MOVE_MSG_KEYS        = list(range(0x64, 0x6E))
AUTO_MOVE_DEFAULT_RTT     = 120
AUTO_MOVE_MAX_SEND_ERRORS = 50          # ★ NEW: hard abort after 50 consecutive errors

# ==================== ENCODING ====================
def float_to_u32(f: float) -> int:
    return struct.unpack("<I", struct.pack("<f", float(f) + 0.0))[0]

def zigzag_decode(n: int) -> int:
    return (n >> 1) ^ -(n & 1)

async def uleb_encode(value: int) -> bytes:
    out = bytearray()
    value = int(value) & 0xFFFFFFFFFFFFFFFF
    while value >= 0x80:
        out.append((value & 0x7F) | 0x80)
        value >>= 7
    out.append(value)
    return bytes(out)

async def zigzag_encode(n: int) -> bytes:
    z = ((n << 1) ^ (n >> 63)) & 0xFFFFFFFFFFFFFFFF
    return await uleb_encode(z)

def read_varint_bytes(data: bytes, offset: int) -> Tuple[int, int]:
    r, s = 0, 0
    while True:
        if offset >= len(data):
            raise IndexError("oob")
        b = data[offset]
        offset += 1
        r |= (b & 0x7F) << s
        if not (b & 0x80):
            break
        s += 7
    return r, offset

def read_varints_list(buf: bytes) -> List[int]:
    out = []
    off = 0
    while off < len(buf):
        v, off = read_varint_bytes(buf, off)
        out.append(v)
    return out

def decode_players_v2(body: bytes) -> Dict[int, Dict[str, Any]]:
    players = {}
    if body is None or len(body) < 4:
        return players
    p = 2
    while p < len(body) - 1:
        try:
            short_id = body[p]; p += 1
            x, p = read_varint_bytes(body, p)
            y, p = read_varint_bytes(body, p)
            z, p = read_varint_bytes(body, p)
            vx, p = read_varint_bytes(body, p)
            vy, p = read_varint_bytes(body, p)
            vz, p = read_varint_bytes(body, p)
            yrot = body[p]; p += 1
            aim_y = body[p]; p += 1
            aim_xz = body[p]; p += 1
            physx_state = body[p]; p += 1
            physx_pose = body[p]; p += 1
            platform, p = read_varint_bytes(body, p)
            custom = body[p]; p += 1
        except (IndexError, ValueError):
            break
        pos = (zigzag_decode(x), zigzag_decode(y), zigzag_decode(z))
        if not (1 <= short_id <= 64) or any(abs(v) > 4000000 for v in pos):
            break
        players[short_id] = {
            "pos": pos,
            "vel": (zigzag_decode(vx), zigzag_decode(vy), zigzag_decode(vz)),
            "yrot": yrot, "aim_y": aim_y, "aim_xz": aim_xz,
            "physx_state": physx_state, "physx_pose": physx_pose,
            "platform": platform, "custom": custom,
        }
    return players

# ==================== HEADER ====================
_FIELD_SIZES = {0: 1, 1: 1, 2: 2, 3: 2, 4: 1, 5: 2}

_LAYOUTS = [
    (0, 1, 2, 3, 4, 5), (0, 1, 2, 3, 5, 4), (0, 1, 2, 4, 3, 5), (0, 1, 2, 4, 5, 3),
    (0, 1, 2, 5, 3, 4), (0, 1, 2, 5, 4, 3), (0, 1, 3, 2, 4, 5), (0, 1, 3, 2, 5, 4),
    (0, 1, 3, 4, 2, 5), (0, 1, 3, 4, 5, 2), (0, 1, 3, 5, 2, 4), (0, 1, 3, 5, 4, 2),
    (0, 1, 4, 2, 3, 5), (0, 1, 4, 2, 5, 3), (0, 1, 4, 3, 2, 5), (0, 1, 4, 3, 5, 2),
    (0, 1, 4, 5, 2, 3), (0, 1, 4, 5, 3, 2), (0, 1, 5, 2, 3, 4), (0, 1, 5, 2, 4, 3),
    (0, 1, 5, 3, 2, 4), (0, 1, 5, 3, 4, 2), (0, 1, 5, 4, 2, 3), (0, 1, 5, 4, 3, 2),
]

async def layouts_from_mask(mask: Any) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
    if isinstance(mask, str):
        mask_bytes = mask.encode("ascii", "ignore")
    elif isinstance(mask, bytes):
        mask_bytes = mask
    else:
        mask_bytes = str(mask).encode("ascii", "ignore")
    b0 = mask_bytes[0] if len(mask_bytes) > 0 else 0x5A
    b1 = mask_bytes[1] if len(mask_bytes) > 1 else 0xA5
    nr = _LAYOUTS[b0 % len(_LAYOUTS)]
    r  = _LAYOUTS[b1 % len(_LAYOUTS)]
    return r, nr

async def encode_header(layout, so, cmd, oid, flags, length, k, v80):
    fields = {
        0: (so & 0xFF) ^ k,
        1: (flags & 0xFF) ^ k,
        2: ((cmd & 0xFFFF) ^ v80) & 0xFFFF,
        3: (((oid or 0) & 0xFFFF) ^ v80) & 0xFFFF,
        4: 0 ^ k,
        5: ((length & 0xFFFF) ^ v80) & 0xFFFF,
    }
    out = bytearray()
    for code in layout:
        sz = _FIELD_SIZES[code]
        val = fields[code]
        if sz == 1:
            out.append(val & 0xFF)
        else:
            out.extend([val & 0xFF, (val >> 8) & 0xFF])
    return bytes(out)

async def crc7_buff(crc: int, buff: bytes) -> int:
    for b in buff:
        for bit in range(8):
            msb = (crc & 0x40) != 0
            crc = ((crc << 1) & 0x7F) | ((b >> (7 - bit)) & 1)
            if msb:
                crc ^= 0x09
    return crc & 0x7F

# ==================== STATE ====================
class MoveState:
    def __init__(self):
        self.session_start = time.time()
        self.slot: Optional[int] = None
        self.server_pos: Optional[Tuple[int, int, int]] = None
        self.server_physx_state: Optional[int] = None
        self.server_vel_y: int = 0
        self.server_update_seq: int = 0
        self.pending_ack: Optional[int] = None
        self.rtt_ms: Optional[int] = None
        self.ping_sent: Dict[int, float] = {}
        self.cmd_counts = collections.Counter()
        self.undecoded: int = 0
        self.last_2001_head = None
        self.other_players: Dict[int, Dict[str, Any]] = {}
        self.nearest_enemy_id: int = 0
        self.nearest_enemy_pos: Optional[Tuple[int, int, int]] = None
        self.send_count = 0
        self.send_errors = 0                 # ★ NEW

    def diagnostics(self) -> str:
        top = ", ".join(f"{c}x{n}" for c, n in self.cmd_counts.most_common(12)) or "none"
        enemy_str = f"nearest_enemy={self.nearest_enemy_id}" if self.nearest_enemy_id else "no enemy"
        return (f"cmds [{top}] | 2001 parsed {self.server_update_seq} | "
                f"slot {self.slot} pos {self.server_pos} | {enemy_str}")

    def on_server_frame(self, frame: Dict[str, Any]):
        cmd = frame.get("cmd")
        self.cmd_counts[cmd] += 1
        if frame.get("kind") == "RUDP" and frame.get("orderId") is not None:
            oid = frame["orderId"]
            if self.pending_ack is None or ((oid - self.pending_ack) & 0xFFFF) < 0x8000:
                self.pending_ack = oid
        if cmd == 2001:
            self._on_own_state(frame.get("content") or b"")
        elif cmd == 2012:
            self._on_other_states(frame.get("content") or b"")
        elif cmd == 3:
            c = frame.get("content") or b""
            if len(c) >= 4:
                sent = self.ping_sent.pop(struct.unpack_from("<I", c, 0)[0], None)
                if sent is not None:
                    self.rtt_ms = int((time.time() - sent) * 1000)

    def _on_other_states(self, content: bytes):
        try:
            players = decode_players_v2(content)
            if not players:
                return
            self.other_players.update(players)
            ref_pos = self.server_pos
            if ref_pos:
                mx, my, mz = ref_pos
                best_id = 0
                best_dist = float("inf")
                best_pos = None
                for pid, pdata in self.other_players.items():
                    if pid == self.slot:
                        continue
                    px, py, pz = pdata["pos"]
                    d = math.hypot(px - mx, pz - mz)
                    if d < best_dist:
                        best_dist = d
                        best_id = pid
                        best_pos = (px, py, pz)
                if best_id != 0:
                    self.nearest_enemy_id = best_id
                    self.nearest_enemy_pos = best_pos
        except Exception:
            pass

    def _on_own_state(self, content: bytes):
        try:
            v = read_varints_list(content)
        except Exception:
            return
        if len(v) < 16 or v[0] != 0 or v[1] != 2:
            return
        self.slot = v[2]
        self.server_pos = (zigzag_decode(v[3]), zigzag_decode(v[4]), zigzag_decode(v[5]))
        self.server_vel_y = zigzag_decode(v[12])
        self.server_physx_state = v[14]
        self.server_update_seq += 1

# ==================== 2001 BUILDER ====================
async def build_player_state_sync_2001(
    key_bytes, mask, msg_key, slot, pos, stick, move_input, vel,
    physx_state, physx_pose, facing, net_tick, counter_ms, ack_order=None
) -> bytes:
    body = bytearray()
    body += await uleb_encode((1 << 24) | int(slot))
    for value in (*pos, *stick, *move_input, *vel):
        body += await zigzag_encode(int(round(value)))
    body += await uleb_encode(int(physx_state))
    body += await uleb_encode(int(physx_pose))
    for f in facing:
        body += await uleb_encode(float_to_u32(f))
    body += b"\x00\x00"
    body += await uleb_encode(int(net_tick))
    body += b"\x00\x00\x00"
    body += await uleb_encode(int(counter_ms))
    body = bytes(body)

    k = key_bytes[0]
    v80 = ((k << 8) | k) & 0xFFFF
    flags = 4 if ack_order is not None else 0
    nr = (await layouts_from_mask(mask))[1]
    hdr = bytearray([msg_key & 0xFF, 0])
    hdr += await encode_header(nr, 0, 2001, None, flags, len(body), k, v80)
    if ack_order is not None:
        a = ((int(ack_order) & 0xFFFF) ^ v80) & 0xFFFF
        hdr += bytes([a & 0xFF, a >> 8, k])
    packet = bytearray(hdr + body)
    packet[1] = await crc7_buff(0, bytes(packet[2:])) & 0x7F
    return bytes(packet)

# ==================== MAIN LOOP (per-bot) ====================
async def auto_move_loop(sock, ip, port, key_bytes, mask, state, stop_event, label=""):
    loop = asyncio.get_event_loop()

    async def wait(seconds):
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=seconds)
            return True
        except asyncio.TimeoutError:
            return False

    next_report = time.time() + AUTO_MOVE_SPAWN_TIMEOUT
    landed_deadline = None
    while True:
        if state.slot is not None and state.server_pos is not None:
            if landed_deadline is None:
                landed_deadline = time.time() + AUTO_MOVE_LAND_TIMEOUT
            if (state.server_physx_state == 0 and state.server_vel_y == 0) or time.time() > landed_deadline:
                break
        elif time.time() > next_report:
            print(f"[MOVE{label}] waiting for spawn: {state.diagnostics()}")
            next_report = time.time() + AUTO_MOVE_SPAWN_TIMEOUT
        if await wait(0.2):
            return

    pos = list(state.server_pos)
    anchor = tuple(pos)
    seen_seq = state.server_update_seq
    heading = random.uniform(-math.pi, math.pi)
    stick = (math.sin(heading) * 100, 0.0, math.cos(heading) * 100)
    target = None
    speed = 0
    freeze_until = time.time() + AUTO_MOVE_START_DELAY
    pause_until = freeze_until + random.uniform(0.2, 0.6)
    recent_sent = collections.deque(maxlen=40)
    last_send = time.time()
    active_logged = False
    step_count = 0
    print(f"[MOVE{label}] Spawn slot={state.slot} pos={anchor} → buy-phase {AUTO_MOVE_START_DELAY:.0f}s")

    while not stop_event.is_set():
        now = time.time()
        dt_ms = (now - last_send) * 1000.0
        last_send = now

        if state.server_update_seq != seen_seq and state.server_pos:
            seen_seq = state.server_update_seq
            sx, sy, sz = state.server_pos
            if recent_sent and all(math.hypot(sx - p[0], sz - p[2]) > AUTO_MOVE_RESYNC_DISTANCE for p in recent_sent):
                print(f"[MOVE{label}] Resync anchor → {state.server_pos}")
                pos = [sx, sy, sz]
                anchor = (sx, sy, sz)
                target = None
                recent_sent.clear()
                freeze_until = now + 15.0
                pause_until = freeze_until + random.uniform(0.2, 0.6)
                active_logged = False

        if now < freeze_until:
            move_input = (0.0, 0.0)
            vel = (0.0, 0.0, 0.0)
            pose = 0
            target = None
        else:
            if not active_logged:
                print(f"[MOVE{label}] Buy phase end → safe micro-shuffle active")
                active_logged = True

            if target is None and now >= pause_until:
                cand = pos
                for _ in range(12):
                    ang = random.uniform(-math.pi, math.pi)
                    dist = random.uniform(AUTO_MOVE_MIN_LEG, AUTO_MOVE_RADIUS)
                    cand = (anchor[0] + math.sin(ang) * dist, anchor[2] + math.cos(ang) * dist)
                    if math.hypot(cand[0] - pos[0], cand[1] - pos[2]) >= AUTO_MOVE_MIN_LEG:
                        break
                target = cand
                run = random.random() < AUTO_MOVE_RUN_CHANCE
                speed = AUTO_MOVE_RUN_SPEED if run else AUTO_MOVE_WALK_SPEED

            move_input = (0.0, 0.0)
            vel = (0.0, 0.0, 0.0)
            pose = 0
            if target is not None:
                dx, dz = target[0] - pos[0], target[1] - pos[2]
                remaining = math.hypot(dx, dz)
                step = speed * dt_ms / 100.0
                if remaining <= step:
                    pos[0], pos[2] = target
                    target = None
                    pause_until = now + random.uniform(*AUTO_MOVE_PAUSE_RANGE)
                else:
                    want = math.atan2(dx, dz)
                    diff = (want - heading + math.pi) % (2 * math.pi) - math.pi
                    max_turn = math.radians(AUTO_MOVE_TURN_PER_TICK)
                    heading += max(-max_turn, min(max_turn, diff))
                    ux, uz = math.sin(heading), math.cos(heading)
                    stick = (ux * 100, 0.0, uz * 100)
                    move_input = (stick[0], stick[2])
                    vel = (ux * speed, 0.0, uz * speed)
                    pose = 1 if speed > 0 else 0
                    pos[0] += ux * step
                    pos[2] += uz * step

        if state.nearest_enemy_pos is not None:
            dx_e = state.nearest_enemy_pos[0] - pos[0]
            dz_e = state.nearest_enemy_pos[2] - pos[2]
            aim_heading = math.atan2(dx_e, dz_e)
            facing = (math.sin(aim_heading), 0.0, math.cos(aim_heading))
        else:
            facing = (math.sin(heading), 0.0, math.cos(heading))

        rtt = state.rtt_ms if state.rtt_ms is not None else AUTO_MOVE_DEFAULT_RTT
        ack = None
        if AUTO_MOVE_PIGGYBACK_ACK and state.pending_ack is not None:
            ack, state.pending_ack = state.pending_ack, None
        try:
            pkt = await build_player_state_sync_2001(
                key_bytes, mask, random.choice(AUTO_MOVE_MSG_KEYS), state.slot,
                pos, stick, move_input, vel, 0, pose, facing,
                max(1, min(1000, rtt)), int((now - state.session_start) * 1000), ack_order=ack
            )
            await loop.sock_sendto(sock, pkt, (ip, port))
            recent_sent.append((round(pos[0]), round(pos[1]), round(pos[2])))
            state.send_count += 1
            state.send_errors = 0    # ★ reset on success
            step_count += 1
            if step_count % 40 == 0:
                dist_sp = math.hypot(pos[0] - anchor[0], pos[2] - anchor[2])
                status_str = f"buy-phase ({freeze_until - now:.1f}s)" if now < freeze_until else f"shuffle dist={dist_sp:.0f}"
                enemy_str = f"enemy={state.nearest_enemy_id}" if state.nearest_enemy_id else "no-enemy"
                print(f"[MOVE{label}] pos=({int(pos[0])},{int(pos[1])},{int(pos[2])}) {status_str} pose={pose} {enemy_str} sent={state.send_count}")
        except Exception as e:
            state.send_errors += 1
            if state.send_errors <= 5 or state.send_errors % 20 == 0:
                print(f"[MOVE{label}] send err #{state.send_errors}: {e}")
            if state.send_errors >= AUTO_MOVE_MAX_SEND_ERRORS:
                print(f"[MOVE{label}] too many send errors ({state.send_errors}) — aborting movement for this match")
                return
        if await wait(AUTO_MOVE_TICK_INTERVAL):
            return