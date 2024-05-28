script_dir=~/scripts
date >>  $script_dir/status.log
echo "Starting a download script" >>  $script_dir/status.log

if [ -f $script_dir/magnet_running.link ]; then
    echo "Already downloading" 
    echo "Already downloading" >>  $script_dir/status.log
    exit 1
fi

#mv /home/laixuan/bangumi/scripts/magnet_set.txt /home/laixuan/bangumi/scripts/magnet_running.link
tr -d '\15\32' < $script_dir/magnet_set.txt > $script_dir/magnet_running.link
echo "" >> $script_dir/magnet_running.link
tr -d '\15\32' < $script_dir/auto_magnet_set >> $script_dir/magnet_running.link
echo "" >> $script_dir/magnet_running.link
rm $script_dir/magnet_set.txt
rm $script_dir/auto_magnet_set

touch $script_dir/magnet_set.txt
touch $script_dir/auto_magnet_set

while IFS= read -r line; do
    target=$(echo $line | cut -d "%" -f 1)
    addr=$(echo $line | cut -sd "%" -f 2)
    date >>  $script_dir/status.log
    echo "-------------------------Starting a new download------------------------------------------"
    echo "-------------------------Starting a new download------------------------------------------" >>  $script_dir/status.log
    echo "transmission-cli -f  $script_dir/post_download.sh -w ' $script_dir/output/$addr' $target" >>  $script_dir/status.log
    echo "transmission-cli -f  $script_dir/post_download.sh -w ' $script_dir/output/$addr' $target"
    transmission-cli -f $script_dir/post_download.sh -w " $script_dir/$addr" $target
    date >>  $script_dir/status.log
    echo "-------------------------Finished       download------------------------------------------" >>  $script_dir/status.log
    echo "transmission-cli -f  $script_dir/post_download.sh -w '$script_dir/output/$addr' $target" >>  $script_dir/status.log
    sleep 1
done < $script_dir/magnet_running.link

rm $script_dir/magnet_running.link
