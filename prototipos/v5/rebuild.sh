set -e
cd /home/claude/hqv/v5
for f in 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22; do python3 patch_shell$f.py >/dev/null; done
python3 patch_cot9.py >/dev/null; python3 patch_cot10.py >/dev/null
for f in 7 8 9 10 11 12 13 14 15; do python3 patch_reg$f.py >/dev/null; done
python3 build5.py; python3 post_brand.py >/dev/null; python3 post_dark.py >/dev/null
