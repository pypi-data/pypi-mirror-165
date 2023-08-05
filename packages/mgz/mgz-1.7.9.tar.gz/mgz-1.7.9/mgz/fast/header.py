"""Fast(er) parsing for recorded game headers."""
import io
import hashlib
import re
import struct
import uuid
import zlib

from mgz.util import get_version, Version

ZLIB_WBITS = -15
CLASSES = [b'\x0a', b'\x1e', b'\x46', b'\x50']
BLOCK_END = b'\x00\x0b'
REGEXES = {}
SKIP_OBJECTS = [
    (b'\x1e\x00\x87\x02', 252)  # 647: junk DE object, thousands per file
]


def _compile_object_search():
    """Compile regular expressions for object searching."""
    class_or = b'(' + b'|'.join(CLASSES) + b')'
    for i in range(9):
        expr = class_or + struct.pack('b', i) + b'[^\x00][\x00-\xff]{3}\xff\xff\xff\xff[^\xff]'
        REGEXES[i] = re.compile(expr)


_compile_object_search()


def unpack(fmt, data):
    """Unpack bytes according to format string."""
    output = struct.unpack(fmt, data.read(struct.calcsize(fmt)))
    if len(output) == 1:
        return output[0]
    return output


def aoc_string(data):
    """Read AOC string."""
    length = unpack('<h', data)
    return data.read(length)


def de_string(data):
    """Read DE string."""
    assert data.read(2) == b'\x60\x0a'
    length = unpack('<h', data)
    return unpack(f'<{length}s', data)


def hd_string(data):
    """Read HD string."""
    length = unpack('<h', data)
    assert data.read(2) == b'\x60\x0a'
    return unpack(f'<{length}s', data)


def parse_object(data, offset):
    """Parse an object."""
    class_id, object_id, instance_id, pos_x, pos_y = struct.unpack_from('<bxH14xIxff', data, offset)
    if object_id >= 65535:
        raise RuntimeError("bad object parse")
    return dict(
        class_id=class_id,
        object_id=object_id,
        instance_id=instance_id,
        position=dict(
            x=pos_x,
            y=pos_y
        )
    )


def object_block(data, pos, player_number, index):
    """Parse a block of objects."""
    objects = []
    offset = None
    while True:
        if not offset:
            match = REGEXES[player_number].search(data, pos)
            end = data.find(BLOCK_END, pos) - pos + len(BLOCK_END)
            if match is None:
                break
            offset = match.start() - pos
            while end + 8 < offset:
                end += data.find(BLOCK_END, pos + end) - (pos + end) + len(BLOCK_END)
        if end + 8 == offset:
            break
        pos += offset
        # Speed optimization: Skip specified fixed-length objects.
        test = data[pos:pos + 4]
        for fingerprint, offset in SKIP_OBJECTS:
            if test == fingerprint:
                break
        else:
            objects.append(dict(parse_object(data, pos), index=index))
        offset = None
        pos += 31
    return objects, pos + end


def parse_mod(header, num_players, version):
    """Parse Userpatch mod version."""
    cur = header.tell()
    name_length = unpack(f'<xx{num_players}x36x5xh', header)
    resources = unpack(f'<{name_length + 1}xIx', header)
    values = unpack(f'<{resources}f', header)
    header.seek(cur)
    if version is Version.USERPATCH15:
        number = int(values[198])
        return number // 1000, '.'.join(list(str(number % 1000)))


def parse_player(header, player_number, num_players):
    """Parse a player (and objects)."""
    type_, *diplomacy, name_length = unpack(f'<bx{num_players}x9i5xh', header)
    name, resources = unpack(f'<{name_length - 1}s2xIx', header)
    header.read(resources * 4)
    start_x, start_y, civilization_id, color_id = unpack('<xff9xb3xbx', header)
    offset = header.tell()
    data = header.read()
    # Skips thousands of bytes that are not easy to parse.
    start = re.search(b'\x0b\x00.\x00\x00\x00\x02\x00\x00', data).end()
    objects, end = object_block(data, start, player_number, 0)
    sleeping, end = object_block(data, end, player_number, 1)
    doppel, end = object_block(data, end, player_number, 2)
    if data[end + 8:end + 10] == BLOCK_END:
        end += 10
    if data[end:end + 2] == BLOCK_END:
        end += 2
    header.seek(offset + end)
    return dict(
        number=player_number,
        type=type_,
        name=name,
        diplomacy=diplomacy,
        civilization_id=civilization_id,
        color_id=color_id,
        objects=objects + sleeping + doppel,
        position=dict(
            x=start_x,
            y=start_y
        )
    )


def parse_lobby(data, version, save):
    """Parse lobby data."""
    if version is Version.DE:
        data.read(5)
        if save >= 20.06:
            data.read(9)
        if save >= 26.16:
            data.read(5)
    data.read(8)
    if version not in (Version.DE, Version.HD):
        data.read(1)
    reveal_map_id, map_size, population, game_type_id, lock_teams = unpack('I4xIIbb', data)
    if version in (Version.DE, Version.HD):
        data.read(5)
        if save >= 13.13:
            data.read(4)
        if save >= 25.22:
            data.read(1)
    chat = []
    for _ in range(0, unpack('<I', data)):
        message = data.read(unpack('<I', data)).strip(b'\x00')
        if len(message) > 0:
            chat.append(message)
    seed = None
    if version is Version.DE:
        seed = unpack('<i', data)
    return dict(
        reveal_map_id=reveal_map_id,
        map_size=map_size,
        population=population * (25 if version not in (Version.DE, Version.HD) else 1),
        game_type_id=game_type_id,
        lock_teams=lock_teams == 1,
        chat=chat,
        seed=seed
    )


def parse_map(data, version):
    """Parse map."""
    data.read(60)
    tile_format = '<xbbx'
    if version is Version.DE:
        tile_format = '<bxb6x'
        data.read(8)
    size_x, size_y, zone_num = unpack('<III', data)
    tile_num = size_x * size_y
    for _ in range(zone_num):
        if version in (Version.DE, Version.HD):
            data.read(2048 + (tile_num * 2))
        else:
            data.read(1275 + tile_num)
        num_floats = unpack('<I', data)
        data.read(num_floats * 4)
        data.read(4)
    all_visible = unpack('<bx', data)
    tiles = [unpack(tile_format, data) for _ in range(tile_num)]
    num_data = unpack('<I4x', data)
    data.read(num_data * 4)
    for _ in range(0, num_data):
        num_obs = unpack('<I', data)
        data.read(num_obs * 8)
    x2, y2 = unpack('<II', data)
    data.read(x2 * y2 * 4)
    restore_time = unpack('<I', data)
    #if restore_time > 0:
    #    raise RuntimeError("restored matches can't be parsed yet")
    return dict(
        all_visible=all_visible == 1,
        restore_time=restore_time,
        dimension=size_x,
        tiles=tiles
    )


def parse_scenario(data, num_players, version, save):
    """Parse scenario section."""
    data.read(4455)
    if version is Version.DE:
        data.read(128)
    instructions = aoc_string(data)
    for _ in range(0, 9):
        aoc_string(data)
    data.read(78)
    for _ in range(0, 16):
        aoc_string(data)
    data.read(196)
    for _ in range(0, 16):
        data.read(24)
        if version in (Version.DE, Version.HD):
            data.read(4)
    data.read(12672)
    if version is Version.DE:
        data.read(196)
    else:
        for _ in range(0, 16):
            data.read(332)
    if version is Version.HD:
        data.read(644)
    data.read(88)
    if version is Version.HD:
        data.read(16)
    map_id, difficulty_id = unpack('<II', data)
    remainder = data.read()
    if version is Version.DE:
        if save >= 26.16:
            settings_version = 3.0
        elif save >= 25.22:
            settings_version = 2.6
        elif save >= 25.06:
            settings_version = 2.5
        elif save >= 13.34:
            settings_version = 2.4
        else:
            settings_version = 2.2
        end = remainder.find(struct.pack('<d', settings_version))
        end += 1045
    else:
        end = remainder.find(b'\x9a\x99\x99\x99\x99\x99\xf9\x3f') + 13
    data.seek(end - len(remainder), 1)
    return dict(
        map_id=map_id,
        difficulty_id=difficulty_id,
        instructions=instructions
    )


def parse_de(data, version, save, skip=False):
    """Parse DE-specific header."""
    if version is not Version.DE:
        return None
    build = None
    if save >= 25.22 and not skip:
        build = unpack('<I', data)
    timestamp = None
    if save >= 26.16 and not skip:
        timestamp = unpack('<I', data)
    data.read(12)
    dlc_count = unpack('<I', data)
    data.read(dlc_count * 4)
    data.read(4)
    difficulty_id = unpack('<I', data)
    data.read(4)
    rms_map_id = unpack('<I', data)
    data.read(12)
    starting_age_id = unpack('<I', data)
    data.read(46)
    random_positions, all_technologies = unpack('<bb', data)
    data.read(2)
    lock_speed = unpack('<b', data)
    data.read(20)
    if save >= 25.06:
        data.read(1)
    players = []
    for _ in range(8):
        data.read(4)
        color_id = unpack('<i', data)
        data.read(2)
        team_id = unpack('<b', data)
        data.read(9)
        civilization_id = unpack('<I', data)
        de_string(data)
        data.read(1)
        de_string(data)
        name = de_string(data)
        data.read(4)
        profile_id, number = unpack('<I4xi', data)
        if save < 25.22:
            data.read(8)
        prefer_random = unpack('b', data)
        data.read(1)
        if save >= 25.06:
            data.read(8)
        if name:
            players.append(dict(
                number=number,
                color_id=color_id,
                team_id=team_id,
                name=name,
                profile_id=profile_id,
                civilization_id=civilization_id,
                prefer_random=prefer_random == 1
            ))
    data.read(17)
    allow_specs = unpack('b', data)
    visibility = unpack('<I', data)
    hidden_civs = unpack('b', data)
    data.read(1)
    spec_delay = unpack('<I', data)
    data.read(5)
    strings = []
    for _ in range(23):
        strings.append(de_string(data).decode('utf-8').split(':'))
        c = unpack('<I', data)
        while c in [3, 21, 23, 42, 44, 45, 46, 47]:
            c = unpack('<I', data)
    if save < 25.22:
        data.read(236)
    if save >= 25.22:
        data.seek(-4, 1)
        l = unpack('<I', data)
        data.read(l * 4)
    for _ in range(unpack('<Q', data)):
        data.read(4)
        de_string(data)
        data.read(4)
    if save >= 25.02:
        data.read(8)
    guid = data.read(16)
    lobby = de_string(data)
    if save >= 25.22:
        data.read(8)
    mod = de_string(data)
    data.read(33)
    if save >= 20.06:
        data.read(1)
    if save >= 20.16:
        data.read(8)
    if save >= 25.06:
        data.read(21)
    if save >= 25.22:
        data.read(4)
    if save >= 26.16:
        data.read(8)
    if not skip:
        de_string(data)
        data.read(8)
    rms_mod_id = None
    rms_filename = None
    for s in strings:
        if s[0] == 'SUBSCRIBEDMODS' and s[1] == 'RANDOM_MAPS':
            rms_mod_id = s[3].split('_')[0]
            rms_filename = s[2]
    return dict(
        players=players,
        guid=str(uuid.UUID(bytes=guid)),
        hash=hashlib.sha1(guid),
        lobby=lobby.decode('utf-8'),
        mod=mod.decode('utf-8'),
        difficulty_id=difficulty_id,
        starting_age_id=starting_age_id - 2 if starting_age_id > 0 else 0,
        team_together=not bool(random_positions),
        all_technologies=bool(all_technologies),
        lock_speed=bool(lock_speed),
        build=build,
        timestamp=timestamp,
        spec_delay=spec_delay,
        allow_specs=bool(allow_specs),
        hidden_civs=bool(hidden_civs),
        visibility_id=visibility,
        rms_mod_id=rms_mod_id,
        rms_map_id=rms_map_id,
        rms_filename=rms_filename
    )


def parse_hd(data, version, save):
    """Parse HD-specifc header."""
    if version is not Version.HD or save <= 12.34:
        return None
    data.read(12)
    dlc_count = unpack('<I', data)
    data.read(dlc_count * 4)
    data.read(4)
    difficulty_id, map_id = unpack('<II', data)
    data.read(80)
    players = []
    for _ in range(8):
        data.read(4)
        color_id = unpack('<i', data)
        data.read(12)
        civilization_id = unpack('<I', data)
        hd_string(data)
        data.read(1)
        hd_string(data)
        name = hd_string(data)
        data.read(4)
        steam_id, number = unpack('<Qi', data)
        data.read(8)
        if name:
            players.append(dict(
                number=number,
                color_id=color_id,
                name=name,
                profile_id=steam_id,
                civilization_id=civilization_id
            ))
    data.read(26)
    hd_string(data)
    data.read(8)
    hd_string(data)
    data.read(8)
    hd_string(data)
    data.read(8)
    guid = data.read(16)
    lobby = hd_string(data)
    mod = hd_string(data)
    data.read(8)
    hd_string(data)
    data.read(4)
    return dict(
        players=players,
        guid=str(uuid.UUID(bytes=guid)),
        lobby=lobby.decode('utf-8'),
        mod=mod.decode('utf-8'),
        map_id=map_id,
        difficulty_id=difficulty_id
    )


def decompress(data):
    """Decompress header bytes."""
    prefix_size = 8
    header_len, _ = unpack('<II', data)
    zlib_header = data.read(header_len - prefix_size)
    return io.BytesIO(zlib.decompress(zlib_header, wbits=ZLIB_WBITS))


def parse_version(header, data):
    """Parse and compute game version."""
    log = unpack('<I', data)
    game, save = unpack('<7sxf', header)
    version = get_version(game.decode('ascii'), round(save, 2), log)
    return version, game.decode('ascii'), round(save, 2), log


def parse_players(header, num_players, version):
    """Parse all players."""
    cur = header.tell()
    gaia = b'Gaia' if version in (Version.DE, Version.HD) else b'GAIA'
    anchor = header.read().find(b'\x05\x00' + gaia + b'\x00')
    header.seek(cur + anchor - num_players - 43)
    mod = parse_mod(header, num_players, version)
    players = [parse_player(header, number, num_players) for number in range(num_players)]
    cur = header.tell()
    points_version = header.read().find(b'\x00\x00\x00@')
    header.seek(cur)
    header.read(points_version)
    for _ in range(num_players):
        version = unpack('<f', header)
        entries = unpack('<i', header)
        header.read(5 + (entries * 44))
        points = unpack('<i', header)
        header.read(8 + (points * 32))
    return players, mod


def parse_metadata(header):
    """Parse recorded game metadata."""
    ai, game_speed, owner_id, num_players, cheats = unpack('<I24xf17xhbxb', header)
    if ai > 0:
        raise RuntimeError("don't know how to parse ai")
    return dict(
        speed=game_speed,
        owner_id=owner_id,
        cheats=cheats == 1
    ), num_players


def parse(data):
    """Parse recorded game header."""
    try:
        header = decompress(data)
        version, game, save, log = parse_version(header, data)
        if version not in (Version.USERPATCH15, Version.DE, Version.HD):
            raise RuntimeError(f"{version} not supported")
        de = parse_de(header, version, save)
        hd = parse_hd(header, version, save)
        metadata, num_players = parse_metadata(header)
        map_ = parse_map(header, version)
        players, mod = parse_players(header, num_players, version)
        scenario = parse_scenario(header, num_players, version, save)
        lobby = parse_lobby(header, version, save)
    except (struct.error, zlib.error, AssertionError, MemoryError, ValueError) as e:
        raise RuntimeError(f"could not parse: {e}")
    return dict(
        version=version,
        game_version=game,
        save_version=save,
        log_version=log,
        players=players,
        map=map_,
        de=de,
        hd=hd,
        mod=mod,
        metadata=metadata,
        scenario=scenario,
        lobby=lobby
    )
