
import random


adjvs = ["SWINGING", "RADIANT", "BRONZE", "RED", "GREEN", "PINK", "STONE",
    "PURPLE", "NAVY", "SCARLET", "FALLEN", "FUCHSIA", "EMERALD", "DESERT",
    "SACRED", "FROZEN", "CELTIC", "SWOOPING", "LEAD", "TURQUOISE", "GRAY",
    "BEIGE", "OLIVE", "SILENT", "MAROON", "GLASS", "FADING", "CRIMSON",
    "BLUE", "AMBER", "TEAL", "BLACK", "FLYING", "COPPER", "LIME", 
"GOLDEN",
    "VENGEFUL", "AGING", "EMPTY", "STEEL", "IRON", "SPECTRAL", "LOST",
    "WHITE", "FROWNING", "YELLOW", "FORGOTTEN", "AQUA", "PLASTIC", "LAZY",
    "SILVER", "SWIFT", "CHASING"]

nouns = ["COPPERTONE", "JOCKEY", "TIMBERWOLF", "SAWHORSE", "PANDA", 
"SANDSTORM",
    "SEARCHLIGHT", "RAINBOW", "RENAISSANCE", "SPEEDWAY", "VOLUNTEER",
    "PHOENIX", "MARVEL", "SUNBURN", "DRILLER", "MARKSMAN", "DASHER",
    "JAVELIN", "SNOWBANK", "HUMMINGBIRD", "RADIANCE", "RIBBON", 
"INSTRUCTOR",
    "ROSEBUD", "THUNDER", "RAMROD", "ALPINE", "AUTHOR", "DOGWOOD",
    "CORNERSTONE", "RAINDANCE", "LANCER", "SUNDANCE", "EAGLE", 
"DAREDEVIL",
    "ROVER", "MIRACLE", "TRANQUILITY", "STARBURST", "PROFESSOR", "APOLLO",
    "SUNSHINE", "DUSTER", "PATHFINDER", "SWORDFISH", "MAHOGANY", 
"PHOTOGRAPH",
    "DERBY", "STARDUST", "DYNAMO", "CENTURION", "MECHANIC", "STARLIGHT",
    "RHYME", "LASER", "PIONEER", "GRANDMA", "DANCER", "PEBBLES",
    "SCREWDRIVER", "SCORECARD", "WITNESS", "DIAMOND", "VELVET", 
"DASHBOARD",
    "SUPERVISOR", "PASSKEY", "SILHOUETTE", "RENEGADE", "SUGARFOOT", 
"VENUS",
    "PROVIDENCE", "DEACON", "DRAGON", "SAHARA", "CHAMPION"]


def int_to_roman(n):
    if not isinstance(n, type(1)):
        raise TypeError(f"Expected integer, got {type(n)}")
    if not (0 < n < 4000):
        raise ValueError("Argument must be between 1 and 3999")
    ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
    nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
    result = []
    for i in range(len(ints)):
        count = int(n / ints[i])
        result.append(nums[i] * count)
        n -= ints[i] * count
    return ''.join(result)


def hash32(x):
    x += 0x3243f6a8
    x ^= x >> 15
    x *= 0xd168aaad
    x ^= x >> 15
    x *= 0xaf723597
    x ^= x >> 15
    return x


def codename_by_state(state):
    a = (state <<  3 | 5) & 0xfff
    c = (state >>  8 | 1) & 0xfff
    s =  state >> 20; 
    while True:
        s = (s*a + c) & 0xfff
        if s < len(adjvs)*len(nouns):
            break
    i = int(s % len(adjvs))
    j = int(s / len(adjvs))
    return ((state & 0xfffff) | s<<20), f"{adjvs[i]} {nouns[j]}"


def generate( *, index=None, seed=0):
    if index is None:
        index = random.randrange(4028)
    if not isinstance(seed, type(1)):
        raise TypeError(f"Expected seed to be integer, got {type(input)}")
    if not isinstance(index, type(1)):
        raise TypeError(f"index is expected to be an integer, got {type(input)}")
    if index < 0:
        raise ValueError('index must be positive')
    hash = hash32(seed)
    loop_count = (index // 4028) + 1
    if loop_count > 1:
        index = index % 4028
        if loop_count >= 4000:
            raise ValueError(f"index is must be less than 16107972")
        for _ in range(loop_count):
            seed = hash32(hash)        
    for _ in range(index + 1):
        hash, buf = codename_by_state(hash)
    
    codename = buf
    if loop_count > 1:
        codename = f"{codename} {int_to_roman(loop_count)}"
    return codename


if __name__ == '__main__':
    print(generate(index=16107972))
