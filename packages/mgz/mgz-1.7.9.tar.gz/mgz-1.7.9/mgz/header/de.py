"""Definitive Edition structure."""

from construct import (
    Struct, Int32ul, Float32l, Array, Padding, Flag, If,
    Byte, Int16ul, Bytes, Int32sl, Peek, Const, RepeatUntil,
    Int64ul, Computed
)

from mgz.enums import VictoryEnum, ResourceLevelEnum, AgeEnum, PlayerTypeEnum, DifficultyEnum
from mgz.util import find_save_version

# pylint: disable=invalid-name, bad-continuation

de_string = Struct(
    Const(b"\x60\x0A"),
    "length"/Int16ul,
    "value"/Bytes(lambda ctx: ctx.length)
)

separator = Const(b"\xa3_\x02\x00")

player = Struct(
    "dlc_id"/Int32ul,
    "color_id"/Int32sl,
    "selected_color"/Byte,
    "selected_team_id"/Byte,
    "resolved_team_id"/Byte,
    "dat_crc"/Bytes(8),
    "mp_game_version"/Byte,
    "civ_id"/Int32ul,
    "ai_type"/de_string,
    "ai_civ_name_index"/Byte,
    "ai_name"/de_string,
    "name"/de_string,
    "type"/PlayerTypeEnum(Int32ul),
    "profile_id"/Int32ul,
    Const(b"\x00\x00\x00\x00"),
    "player_number"/Int32sl,
    "hd_rm_elo"/If(lambda ctx: find_save_version(ctx) < 25.22, Int32ul),
    "hd_dm_elo"/If(lambda ctx: find_save_version(ctx) < 25.22, Int32ul),
    "prefer_random"/Flag,
    "custom_ai"/Flag,
    If(lambda ctx: find_save_version(ctx) >= 25.06, "handicap"/Bytes(8)),
)

de = "de"/Struct(
    "build"/If(lambda ctx: find_save_version(ctx) >= 25.22, Int32ul),
    "timestamp"/If(lambda ctx: find_save_version(ctx) >= 26.16, Int32ul),
    "version"/Float32l,
    "interval_version"/Int32ul,
    "game_options_version"/Int32ul,
    "dlc_count"/Int32ul,
    "dlc_ids"/Array(lambda ctx: ctx.dlc_count, Int32ul),
    "dataset_ref"/Int32ul,
    Peek("difficulty_id"/Int32ul),
    DifficultyEnum("difficulty"/Int32ul),
    "selected_map_id"/Int32ul,
    "resolved_map_id"/Int32ul,
    "reveal_map"/Int32ul,
    Peek("victory_type_id"/Int32ul),
    VictoryEnum("victory_type"/Int32ul),
    Peek("starting_resources_id"/Int32ul),
    ResourceLevelEnum("starting_resources"/Int32ul),
    "starting_age_id"/Int32ul,
    "starting_age"/AgeEnum(Computed(lambda ctx: ctx.starting_age_id - 2)),
    "ending_age_id"/Int32ul,
    "ending_age"/AgeEnum(Computed(lambda ctx: ctx.ending_age_id - 2)),
    "game_type"/Int32ul,
    separator,
    separator,
    "speed"/Float32l,
    "treaty_length"/Int32ul,
    "population_limit"/Int32ul,
    "num_players"/Int32ul,
    "unused_player_color"/Int32ul,
    "victory_amount"/Int32ul,
    separator,
    "trade_enabled"/Flag,
    "team_bonus_disabled"/Flag,
    "random_positions"/Flag,
    "all_techs"/Flag,
    "num_starting_units"/Byte,
    "lock_teams"/Flag,
    "lock_speed"/Flag,
    "multiplayer"/Flag,
    "cheats"/Flag,
    "record_game"/Flag,
    "animals_enabled"/Flag,
    "predators_enabled"/Flag,
    "turbo_enabled"/Flag,
    "shared_exploration"/Flag,
    "team_positions"/Flag,
    "sub_game_mode"/If(lambda ctx: find_save_version(ctx) >= 13.34, Int32ul),
    "battle_royale_time"/If(lambda ctx: find_save_version(ctx) >= 13.34, Int32ul),
    "handicap"/If(lambda ctx: find_save_version(ctx) >= 25.06, Flag),
    separator,
    "players"/Array(8, player),
    Bytes(9),
    "fog_of_war"/Flag,
    "cheat_notifications"/Flag,
    "colored_chat"/Flag,
    separator,
    "ranked"/Flag,
    "allow_specs"/Flag,
    "lobby_visibility"/Int32ul,
    "hidden_civs"/Flag,
    "matchmaking"/Flag,
    "spec_delay"/Int32ul,
    "scenario_civ"/If(lambda ctx: find_save_version(ctx) >= 13.13, Byte),
    "rms_crc"/If(lambda ctx: find_save_version(ctx) >= 13.13, Bytes(4)),
    "strings"/Array(23,
        Struct(
            "string"/de_string,
            "nums"/RepeatUntil(lambda x, lst, ctx: lst[-1] not in [3, 21, 23, 42, 44, 45, 46, 47], Int32ul)
        )
    ),
    # There's probably a right way to do this, but this is not it.
    "num_sn"/Computed(lambda ctx: ctx.strings[22].nums[1]),
    "strategic_numbers"/Array(lambda ctx: ctx.num_sn if find_save_version(ctx) >= 25.22 else 59, Int32sl),
    "num_ai_files"/Int64ul,
    "ai_files"/Array(lambda ctx: ctx.num_ai_files, Struct(
        Bytes(4),
        "name"/de_string,
        Bytes(4),
    )),
    If(lambda ctx: find_save_version(ctx) >= 25.02, Bytes(8)),
    "guid"/Bytes(16),
    "lobby_name"/de_string,
    If(lambda ctx: find_save_version(ctx) >= 25.22, Bytes(8)),
    "modded_dataset"/de_string,
    Bytes(19),
    If(lambda ctx: find_save_version(ctx) >= 13.13, Bytes(5)),
    If(lambda ctx: find_save_version(ctx) >= 13.17, Bytes(9)),
    If(lambda ctx: find_save_version(ctx) >= 20.06, Bytes(1)),
    If(lambda ctx: find_save_version(ctx) >= 20.16, Bytes(8)),
    If(lambda ctx: find_save_version(ctx) >= 25.06, Bytes(21)),
    If(lambda ctx: find_save_version(ctx) >= 25.22, Bytes(4)),
    If(lambda ctx: find_save_version(ctx) >= 26.16, Bytes(8)),
    de_string,
    Bytes(5),
    If(lambda ctx: find_save_version(ctx) >= 13.13, Byte),
    If(lambda ctx: find_save_version(ctx) < 13.17, Struct(
        de_string,
        Int32ul,
        Bytes(4), # usually zero
    )),
    If(lambda ctx: find_save_version(ctx) >= 13.17, Bytes(2)),
)
