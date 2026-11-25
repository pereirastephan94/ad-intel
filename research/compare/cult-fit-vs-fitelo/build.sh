set -e
cd /home/user/ad-intel
P=research/compare/cult-fit-vs-fitelo
S=/tmp/claude-0/-home-user-ad-intel/a4bcc5c6-4d1a-5676-b1b0-2dff902eac6b/scratchpad
SR="$(cat $P/sample_rule.txt)"
# Fitelo: only its written-up ads (34 of 58 on 25 Nov 2026); see written_up.py
python3 $P/written_up.py research/fitelo $S/fitelo-written
python3 teardown/compare/compute.py research/cult-fit $S/fitelo-written $P/comparison.json --products $P/products.json --series $P/series.json --sample-order default --sample-rule "$SR" --sample-short "the first the Library shows, in its default order, not by impressions" --name-a "Cult.fit" --name-b "Fitelo"
python3 $P/make_persp.py $P/perspectives.json
python3 teardown/compare/build.py $P/comparison.json $P/perspectives.json research/cult-fit research/fitelo $S/pages/cult-fit-vs-fitelo
