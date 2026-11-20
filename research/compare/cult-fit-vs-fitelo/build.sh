set -e
cd /home/user/ad-intel
P=research/compare/cult-fit-vs-fitelo
SR="$(cat $P/sample_rule.txt)"
python3 teardown/compare/compute.py research/cult-fit research/fitelo $P/comparison.json --products $P/products.json --series $P/series.json --sample-order default --sample-rule "$SR" --sample-short "the first the Library shows, in its default order, not by impressions" --name-a "Cult.fit" --name-b "Fitelo" > /dev/null
python3 $P/make_persp.py $P/perspectives.json
python3 teardown/compare/build.py $P/comparison.json $P/perspectives.json research/cult-fit research/fitelo /tmp/claude-0/-home-user-ad-intel/881fe6a6-b751-599d-a717-87e6df82ea58/scratchpad/pages/cult-fit-vs-fitelo
