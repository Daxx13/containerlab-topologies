#!/bin/bash

# Definir el array de nombres
nombres=("dc1_rr1" "dc1_rr2" "dc1_s1" "dc1_s2" "dc1_l1" "dc1_l2" "dc2_rr1" "dc2_rr2" "dc2_s1" "dc2_s2" "dc2_l1" "dc2_l2")

# Iterar sobre cada elemento del array
for nombre in "${nombres[@]}"; do
    origen="./${nombre}/${nombre}.conf"
    destino="./${nombre}/frr.conf"
    
    # Copiar el archivo, sobreescribir si existe
    cp -f "$origen" "$destino"
    
    if [ $? -eq 0 ]; then
        echo "Archivo copiado: $origen -> $destino"
    else
        echo "Error al copiar: $origen -> $destino"
    fi
done
