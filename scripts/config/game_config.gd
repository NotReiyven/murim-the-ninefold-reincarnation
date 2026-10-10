class_name GameConfig
extends RefCounted

const UI_CARD_LIFT_DUR: float = 0.12
const UI_ATTACK_DUR: float = 0.26
const UI_DAMAGE_DUR: float = 0.40
const UI_BLOCK_DUR: float = 0.25
const UI_DRAW_DUR: float = 0.40
const UI_DEATH_DUR: float = 1.20

const RNG_SALT_JUDGMENT: int = 1001
const RNG_SALT_MAP: int = 2002
const RNG_SALT_COMBAT: int = 3003
const RNG_SALT_REWARD: int = 4004
const RNG_SALT_EVENT: int = 5005
const RNG_SALT_SHOP: int = 6006

const KNOWN_FLAGS: Array[String] = [
	"iron_principle_favor",
	"marrow_pact",
	"shielded_marrow",
	"informer",
	"martyr",
	"merchant_wanderer",
	"orthodox_archive_1",
	"trait_heavenly_body",
	"unlocked_past_betrayal",
	"betrayed_wanderer"
]

const KARMA_BANDS: Dictionary[String, Dictionary] = {
	"RIGHTEOUS": {"min": 50, "max": 999, "alignment": "Orthodox", "trait_points": 10, "perk_id": "orthodox_standing"},
	"POSITIVE": {"min": 20, "max": 49, "alignment": "Orthodox", "trait_points": 8, "perk_id": "orthodox_leaning"},
	"NEUTRAL": {"min": 0, "max": 19, "alignment": "Neutral", "trait_points": 6, "perk_id": "open_road"},
	"TAINTED": {"min": -20, "max": -1, "alignment": "Demonic", "trait_points": 4, "perk_id": "marrow_initiate"},
	"ASURA": {"min": -999, "max": -21, "alignment": "Demonic", "trait_points": 2, "perk_id": "marrow_adept"}
}
