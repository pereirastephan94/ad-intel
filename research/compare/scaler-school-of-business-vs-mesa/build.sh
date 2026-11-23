set -e
cd /home/user/ad-intel
P=research/compare/scaler-school-of-business-vs-mesa
OUT=/tmp/claude-0/-home-user-ad-intel/a4bcc5c6-4d1a-5676-b1b0-2dff902eac6b/scratchpad/pages/scaler-school-of-business-vs-mesa
SR="$(cat $P/sample_rule.txt)"
python3 $P/make_series.py $P/series.json > /dev/null
python3 teardown/compare/compute.py research/scaler-school-of-business research/mesa $P/comparison.json --products $P/products.json --series $P/series.json --focus-product pgp_fulltime --snapshot 2026-11-20 --sample-order default --sample-rule "$SR" --sample-short "SSB's are 30 of its 36 live ads, Mesa's 249 of about 320 from many views; not ranked by impressions" --name-a "SSB" --name-b "Mesa"
python3 $P/make_persp.py $P/perspectives.json
python3 teardown/compare/build.py $P/comparison.json $P/perspectives.json research/scaler-school-of-business research/mesa $OUT
