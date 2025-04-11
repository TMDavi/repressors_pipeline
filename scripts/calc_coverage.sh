braganca='/MP_Data/storage/oscar/oscar_repressores/Braganca_merged'
altamira='/MP_Data/storage/oscar/oscar_repressores/Altamira_merged'
maraba='/MP_Data/storage/oscar/oscar_repressores/Maraba_merged'

#for sample in ${braganca}/mapped_reads/*sorted.bam
#do
    sample_name=`basename ${sample} _vs_DNA_repressores_sorted.bam`
#    #coverm contig --bam-files ${sample} --methods mean --output-file ${braganca}/coverage/${sample_name}_coverage.tsv
    bedtools genomecov -ibam ${sample} > ${braganca}/coverage/${sample_name}_coverage.tsv
#done

for sample in ${altamira}/mapped_reads/*sorted.bam
do
    sample_name=`basename ${sample} _vs_DNA_repressores_sorted.bam`
    #coverm contig --bam-files ${sample} --methods mean --output-file ${altamira}/coverage/${sample_name}_coverage.tsv
    bedtools genomecov -ibam ${sample} -g DNA_repressores.genome > ${altamira}/coverage/${sample_name}_coverage.tsv
done

#for sample in ${maraba}/mapped_reads/*sorted.bam
#do
#    sample_name=`basename ${sample} _vs_DNA_repressores_sorted.bam`
    #coverm contig --bam-files ${sample} --methods mean --output-file ${maraba}/coverage/${sample_name}_coverage.tsv
#    bedtools genomecov -ibam ${sample} > ${maraba}/coverage/${sample_name}_coverage.tsv
#done