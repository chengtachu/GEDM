
## Input Files Description

### folder path: /Input/
---

### Transmission
#### folder path: /Input/6_transmission

###### &nbsp;
#### Transmission link (land zones)
#### file: 01_Zone_conn_base.csv
Set transmission link parameters: zone connection, length, base year capacity. This configuration is only for links between terrestrial zones. **Each direction is treated as different link**.
- Transmission links as data row 
- column 1: Country/District code
- column 2: zone type
- column 3: source zone
- column 4: destination zone
- column 5: base year connection (0 or 1) - if set 0, this link still can be a **future expansion** in the model 
- column 6: interconnection with other countries (0 or 1), currently not used
- column 7: link distance (Kilometer), the distance between the centroids of the two connected zones 
- column 8: base year capacity (MW)

###### &nbsp;
#### Transmission link (offshore zones)
#### file: 02_Zone_conn_base_offshore.csv
Set transmission link parameters: zone connection, length, base year capacity. This configuration is only for links **from a offshore zone to a terrestrial zone**.
- Transmission links as data row 
- column 1: Country/District code
- column 2: zone type
- column 3: source zone
- column 4: destination zone
- column 5: base year connection (0 or 1) - if set 0, this link still can be a **future expansion** in the model 
- column 6: link distance (Kilometer), the distance between the centroids of the two connected zones 
- column 7: base year capacity (MW)





