if [ $# != 6 ]; then
    echo "Usage: ./accounting_extraction.sh labeling_file atop_file_path result_file_path result_file_name target_server_ip target_server_password"
    exit 1
fi

labeling_file=$1
labeling_abs_file=$(realpath "$labeling_file")
atop_file_path=$2
result_file_path=$3
result_file_name=$4
target_server_ip=$5
target_server_password=$6
root_path=$(pwd)
code_path=$(dirname $(realpath "$0"))
result_file_abs_path="${root_path}/${result_file_path}"
atop_file_abs_path=$(cd $atop_file_path; pwd)

cd $atop_file_abs_path
for d in $(ls | grep .raw); do
	sh "${code_path}/auto_accounting_process.sh" ${atop_file_abs_path} $d ${code_path} ${target_server_ip} ${target_server_password}
done

python3 "${code_path}/filter_label_atop.py" $labeling_abs_file $result_file_abs_path $result_file_name

cd $root_path