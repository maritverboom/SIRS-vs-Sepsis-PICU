SELECT DISTINCT a.[subject_Patient_value] AS Patientnummer
		,a.[period_start] AS Opname
		,a.[period_end] AS Ontslag
		,a.[specialty_Organization_value] AS Specialisme
		,a.[length] AS LengteOpname
		,a.[length_unit] AS LengteEenheid
		,a.[status_display_original] AS Status
		,a.[class_display_original] AS TypeOpname1
		,a.[type1_display] AS TypeOpname2

	FROM
		PUB.kinder_ic_infecties.Encounter a
		LEFT JOIN PUB.kinder_ic_infecties.Location d ON a.location_Location = d.id
	WHERE (a.identifier_system = 'https://metadata.lumc.nl/ids/HixOpnamePeriode' OR a.identifier_system = 'https://metadata.lumc.nl/ids/HixOpname')
	AND (a.specialty_Organization_value = 'ICKG' OR a.specialty_Organization_value = 'ICKIN' OR a.specialty_Organization_value = 'PICU'
			OR d.identifier2_value = 'PICU'  OR d.identifier2_value = 'ICKG')
	AND (a.period_start BETWEEN '2017-01-01' AND '2022-04-01')
	AND (a.status_display_original = 'Ontslagen' OR a.status_display_original = 'Opgenomen')

ORDER BY Patientnummer 