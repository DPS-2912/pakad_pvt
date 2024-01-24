temp = "max_in_interarrival,max_out_interarrival,max_total_interarrival,avg_in_interarrival,avg_out_interarrival,avg_total_interarrival,std_in_interarrival,std_out_interarrival,std_total_interarrival,75th_percentile_in_interarrival,75th_percentile_out_interarrival,75th_percentile_total_interarrival,25th_percentile_in_times,50th_percentile_in_times,75th_percentile_in_times,100th_percentile_in_times,25th_percentile_out_times,50th_percentile_out_times,75th_percentile_out_times,100th_percentile_out_times,25th_percentile_total_times,50th_percentile_total_times,75th_percentile_total_times,100th_percentile_total_times,in_count,out_count,total_count,in_count_in_first30,out_count_in_first30,in_count_in_last30,out_count_in_last30,std_out_concentration,avg_out_concentration,avg_count_per_sec,std_count_per_sec,avg_order_in,avg_order_out,std_order_in,std_order_out,50th_out_concentration,50th_count_per_sec,min_count_per_sec,max_count_per_sec,max_out_concentrations,in_percentage,out_percentage,sum_alt_concentration,sum_alt_per_sec,sum_intertimestats,sum_timestats,sum_number_pkts"

for i in range(1,72):
   temp = temp + ','
   temp = temp + 'altconc_' + str(i)

for i in range(1,22):
   temp = temp + ','
   temp = temp + 'alt_per_sec_' + str(i)

for i in range(1,33):
   temp = temp + ','
   temp = temp + 'unknown_' + str(i)

temps = temp.split(',')

print(len(temps))
print(temp)
