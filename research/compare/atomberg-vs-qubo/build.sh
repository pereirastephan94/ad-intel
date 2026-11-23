set -e
cd /home/user/ad-intel
P=research/compare/atomberg-vs-qubo
OUT=/tmp/claude-0/-home-user-ad-intel/a4bcc5c6-4d1a-5676-b1b0-2dff902eac6b/scratchpad/pages/atomberg-vs-qubo
SR="$(cat $P/sample_rule.txt)"
python3 $P/make_series.py $P/series.json > /dev/null
python3 teardown/compare/compute.py research/atomberg research/qubo $P/comparison.json --products $P/products.json --series $P/series.json --focus-product smart_lock --snapshot 2026-11-20 --sample-order default --sample-rule "$SR" --sample-short "Atomberg's are the first 30 of about 308 live ads, Qubo's 42 of about 72, in the Library's default order, not by impressions" --name-a "Atomberg" --name-b "Qubo"
python3 $P/make_persp.py $P/perspectives.json
python3 teardown/compare/build.py $P/comparison.json $P/perspectives.json research/atomberg research/qubo $OUT
