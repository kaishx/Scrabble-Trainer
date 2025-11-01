import re, random

# === INPUT FILES ===
FAKE_FILE = "fake_words.txt"
CSW_FILE = "all_real_words.txt"
OUTPUT_FILE = "fake_words_cleaned.txt"

# === CONFIG ===
UNPRONOUNCEABLE_CLUSTERS = [
    "QH","VW","ZF","WD","HP","CM","CW","JJ","HH","XX","ZZ","VV",
    "QG","PT","GM","KL","XR","WX","MX","XD","QX","QJ","CQ","QQ",
    "QN","QM","QP","QV","QZ","VX","XZ","ZX","XC","SX","DX","FX",
    "GX","HX","JX","KX","LX","NX","PX","RX","TX","UX","ZX","BZ",
    "TZ","DZ","SZ","FZ","NZ","KZ","ZG","ZH","ZN","ZP","ZQ",
    "ZR","ZS","ZT","ZW","ZY","WQ","WZ","WV","WF","WL","WP",
    "WN","WB","WHH","WRR","WT","WY","YQ","YV","YF","YX","YB","YC",
    "YH","YK","YM","YN","YP","YR","YT","YW","YZ","RQ","RQH",
    "LM","BN","TL","LD","LR","RTT","DDH","GGH","GQ","PQ","QS",
    "JH","HJ","GHM","HNG","GNH","NHG","PHR","THL","TLH","DLH",
    "HRR","HLL","LRH","RLH","RHN","HRN","MRR","NHH","LHH","CHH",
    "QA","QE","UQ","OQ","QO","IQ","AQ","UWU","UW","BW","CW"
]
RARE_LETTERS = set("VXZJKQ")
VOWELS = set("AEIOUY")
SUFFIXES = ["ED", "ER", "EN", "AL", "LY", "ING", "FUL", "OUS", "ISH", "LESS", "MENT", "TION", "TE"]
random.seed(20251101)

# --- Load CSW words ---
with open(CSW_FILE, encoding="utf8", errors="ignore") as f:
    real_words = {w.strip().upper() for w in re.split(r"\W+", f.read()) if w.strip()}

# --- Helper functions ---
def too_many_rare(word):
    return len([c for c in word if c in RARE_LETTERS]) / len(word) > 0.2

def bad_cluster(word):
    return any(c in word for c in UNPRONOUNCEABLE_CLUSTERS) or re.search(r"Q(?!U)", word)

def has_vowel(word):
    return any(c in VOWELS for c in word)

consonants = list("BCDFGHLMNPRSTW")
vowels = list("AEIOU")

def make_pronounceable(length):
    """Build a pronounceable fake word of the same length, possibly with a suffix."""
    suffix = random.choice(SUFFIXES)
    stem_len = max(length - len(suffix), 2)
    pattern = random.choice(["CVCV", "CVCC", "CVVC", "VCVC", "CVCVC", "CVVCV", "CVCCV"])
    w = ""
    while len(w) < stem_len:
        for p in pattern:
            w += random.choice(vowels if p == "V" else consonants)
            if len(w) >= stem_len:
                break
    candidate = (w[:stem_len] + suffix).upper()
    return candidate[:length]

# --- Process fake list ---
with open(FAKE_FILE, encoding="utf8") as f:
    original = [w.strip().upper() for w in f.read().split() if w.strip()]

cleaned = []
for word in original:
    if len(word) < 4:
        cleaned.append(word)  # short plausible
        continue
    if (too_many_rare(word) or bad_cluster(word) or not has_vowel(word) or word in real_words):
        # Replace with pronounceable fake same length, possibly with suffix
        new_word = None
        for _ in range(2000):
            candidate = make_pronounceable(len(word)).upper()
            if candidate not in real_words and has_vowel(candidate):
                new_word = candidate
                break
        cleaned.append(new_word or word)
    else:
        cleaned.append(word)

# --- Save result ---
with open(OUTPUT_FILE, "w", encoding="utf8") as f:
    f.write(" ".join(cleaned))

print(f"Cleaned list written to {OUTPUT_FILE} with {len(cleaned)} words.")
