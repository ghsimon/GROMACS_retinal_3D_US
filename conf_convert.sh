# convert all conf*.xtc files to conf*.gro files using gmx trjconv
for i in {0..7..1}
do
    echo 0 | gmx trjconv -f conf/conf$i.xtc -s 6eid_capped_matched.gro -o conf/conf$i.gro
done
