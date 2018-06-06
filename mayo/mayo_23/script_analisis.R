library(crafter)
library(dplyr)
library(ggplot2)
library(igraph)

pcap_capture <- read_pcap("syn_attack.pcap")
pcap_capture_info <- pcap_capture$packet_info()
pcap_capture_ip <- pcap_capture$get_layer("IP")
pcap_capture_tcp <- pcap_capture$get_layer("TCP")
pcap_capture_IPs <- pcap_capture$get_ips("all")
# Pares
pairs <- count(pcap_capture_ip, src, dst, protocol_name)
# Nodos
nodes <- unique(c(pairs$src, pairs$dst))
# Grafo
g <- graph_from_data_frame(pairs, directed=TRUE, vertices=nodes)
# Obtencion de las IPs involucradas
ips <- unique(c(pcap_capture_ip$src,pcap_capture_ip$dst));
cont_rangos <- table(cut(pcap_capture_info$packet_size, c(0,20,40,80,160,320,640,1280,2560), 
                         include.lowest=TRUE);
print(cont_rangos);
start_time = pcap_capture_ip$tv_sec[1] + pcap_capture_ip$tv_usec[1]/1e6;
t = (pcap_capture_ip$tv_sec + pcap_capture_ip$tv_usec/1e6) - start_time;
time_divs = seq(0, max(t)+1, by=0.5);
cont_pack_seg = table(cut(t,time_divs, 
                      include.lowest=TRUE));
nom_filas=rownames(cont_pack_seg);

valores = as.vector(cont_pack_seg);
plot(time_divs[c(0:length(valores))],valores,type="l",
     col="blue",main="Conteo de paquetes",xlab = "t",ylab="Paquetes/segundo")
