WITH ICkind AS (
	SELECT DISTINCT a.[subject_Patient_value] AS Patientnummer
		,a.[period_start] AS Starttijd
		,a.[period_end] AS Eindtijd
	FROM
		PUB.kinder_ic_infecties.Encounter a
		LEFT JOIN PUB.kinder_ic_infecties.Location d ON a.location_Location = d.id
	WHERE (a.identifier_system = 'https://metadata.lumc.nl/ids/HixOpnamePeriode' OR a.identifier_system = 'https://metadata.lumc.nl/ids/HixOpname')
		AND (a.specialty_Organization_value = 'ICKG' OR a.specialty_Organization_value = 'ICKIN' OR a.specialty_Organization_value = 'PICU'
			OR d.identifier2_value = 'PICU'  OR d.identifier2_value = 'ICKG')
)

SELECT DISTINCT
	h.[subject_patient_value] AS Patientnummer
	,h.[code_display_original] AS Value
	,h.[valueQuantity_value] AS Number
	,h.[valueQuantity_code_original] AS Eenheid 
	,h.[effectiveDateTime] AS Tijdstip
  FROM 
    PUB.kinder_ic_infecties.Observation h WITH (nolock)
    RIGHT JOIN ICkind ick ON h.[subject_patient_value] = ick.Patientnummer
  WHERE 
	(h.[code_display_original] = 'Hemoglobine' OR h.[code_display_original] = 'Hematocriet' OR h.[code_display_original] = 'Erytrocyten' 
	OR h.[code_display_original] = 'Trombocyten' OR h.[code_display_original] = 'Leukocyten' OR h.[code_display_original] = 'Lymfocyten')
	AND (h.[valueQuantity_value] IS NOT NULL)	
	AND (h.[effectiveDateTime] BETWEEN ick.[Starttijd] AND ick.[Eindtijd])
	AND (h.[valueQuantity_value] IS NOT NULL)
ORDER BY Patientnummer, Tijdstip