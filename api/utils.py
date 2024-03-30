import os
import re
from pypdf import PdfReader
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def extract_data_from_pdf(pdf_path):
    logger.info("Extracting data from PDF: %s", pdf_path)

    try:
        reader = PdfReader(pdf_path)
        number_of_pages = len(reader.pages)
        all_text = ""
        for page_number in range(number_of_pages):
            page = reader.pages[page_number]
            page_text = page.extract_text()
            all_text += page_text + "\n"
    except Exception as e:
        logger.error("Error occurred while reading PDF: %s", str(e))
        return None
    text = all_text
    logger.debug("PDF text extracted successfully")

    """Regular expression patterns"""
    model_pattern = r'Model.*$'
    # size_pattern = r"Size (.+?)(?=Rollers|$)"
    size_pattern = r"Size ([^\n]+)"
    rollers_pattern = r"Rollers ([^\n]+)"
    quantity_pattern = r'Quantity\s*(\d+)'
    track_radius_pattern = r"Track Radius (\d+) IN\."
    strut_size_pattern = r"Strut Size ([^\n]+)"
    track_size_pattern = r"Track Size (\d+ IN\. Bolted)"
    quantity_standard_pattern = r"Quantity Standard -\s*(\d+)"
    track_config_pattern = r"Track Configuration(.+?)(?=Track Appearance|$)"
    track_appearance_pattern = r"Track Appearance ([^\n]+)"
    jamb_mount_pattern = r"Jamb Mount(.+?)(?=Additional Selection|$)"
    additional_selection_pattern = r"Additional Selection ([^\n]+)"
    jamb_material_pattern = r"Jamb Material(.+?)(?=VDS Color|$)"
    vds_color_pattern = r"VDS Color ([^\n]+)"
    additional_customization_pattern = r"Additional Customization ([^\n]+)"
    type_pattern = r"Type(.+?)(?=Cyclage|$)"
    cyclage_pattern = r"Cyclage ([^\n]+)"
    spring_count_pattern = r"Spring Count(.+?)(?=Drum|$)"
    drum_pattern = r"Drum ([^\n]+)"
    wire_size_pattern = r"Wire Size(.+?)(?=Shaft|$)"
    shaft_pattern = r"Shaft ([^\n]+)"
    spring_id_pattern = r"Spring ID(.+?)(?=Shaft Diameter|$)"
    shaft_diameter_pattern = r"Shaft Diameter ([^\n]+)"
    prod_length_pattern = r"Prod. Length(.+?)(?=Auxilary Bearings|$)"
    auxilary_bearings_pattern = r"Auxilary Bearings ([^\n]+)"
    spring_turns_pattern = r"Spring Turns(.+?)(?=Cable Size|$)"
    cable_size_pattern = r"Cable Size ([^\n]+)"
    weight_pattern = r"Weight ([^\n]+)"
    only_model_pattern = r"Model\s*:\s*(.+)"

    tbl_dict = {'# Section Bundles': '0', '# Hardware Cartons': '0', '# Track Bundles': '0', '# of Struts': '0', '# Torsion Springs': '0', 'Feet of VDS': '0'}

    lines = text.strip().split('\n')
    last_line = lines[-1]
         
    values = last_line.strip().split()
    if "of" in last_line:
        tbl_dict['# of Struts'] = values[values.index("of") - 1] + " of " + values[values.index("of") + 1]
        tbl_dict['# Torsion Springs'] = values[-2]
        tbl_dict['Feet of VDS'] = values[-1]
    else:
        tbl_dict['# of Struts'] = values[3]
        tbl_dict['# Torsion Springs'] = values[4]
        tbl_dict['Feet of VDS'] = values[5]


    tbl_dict['# Section Bundles'] = values[0]
    tbl_dict['# Hardware Cartons'] = values[1]
    tbl_dict['# Track Bundles'] = values[2]

    """Search for matches in the text"""
    model_match = re.search(model_pattern, text, re.MULTILINE)
    size_match = re.search(size_pattern, text)
    quantity_match = re.search(quantity_pattern, text)
    rollers_match = re.search(rollers_pattern, text)
    track_radius_match = re.search(track_radius_pattern, text)
    strut_size_match = re.search(strut_size_pattern, text)
    track_size_match = re.search(track_size_pattern, text)
    quantity_standard_match = re.search(quantity_standard_pattern, text)
    track_config_match = re.search(track_config_pattern, text)
    track_appearance_match = re.search(track_appearance_pattern, text)
    jamb_mount_match = re.search(jamb_mount_pattern, text)
    additional_selection_match = re.search(additional_selection_pattern, text)
    jamb_material_match = re.search(jamb_material_pattern, text)
    vds_color_match = re.search(vds_color_pattern, text)
    additional_customization_match = re.search(additional_customization_pattern, text)
    type_match = re.search(type_pattern, text)
    cyclage_match = re.search(cyclage_pattern, text)
    spring_count_match = re.search(spring_count_pattern, text)
    drum_match = re.search(drum_pattern, text)
    wire_size_match = re.search(wire_size_pattern, text)
    shaft_match = re.search(shaft_pattern, text)
    spring_id_match = re.search(spring_id_pattern, text)
    shaft_diameter_match = re.search(shaft_diameter_pattern, text)
    prod_length_match = re.search(prod_length_pattern, text)
    auxilary_bearings_match = re.search(auxilary_bearings_pattern, text)
    spring_turns_match = re.search(spring_turns_pattern, text)
    cable_size_match = re.search(cable_size_pattern, text)
    weight_match = re.search(weight_pattern, text)


    # Extract matched groups
    data = {
        "Model Description": model_match.group(0)[6:] if model_match else None,
        "Model": re.search(only_model_pattern, model_match.group(0)[6:]).group(1).strip(),
        "Quantity": quantity_match.group(1) if quantity_match else None,
        "Wide": (size_match.group(1).split(", ")[0])[:-5] if size_match else None,
        "High": ((size_match.group(1).split(", ")[1]).split("Rollers")[0]).split(" high")[0] if "Rollers" in size_match.group(1) else (size_match.group(1).split(", ")[1]),
        "Rollers": rollers_match.group(1) if rollers_match else None,
        "Track Radius": track_radius_match.group(0)[13:] if track_radius_match else None,
        "Strut Size": strut_size_match.group(0)[11:] if strut_size_match else None,
        "Track Size": track_size_match.group(0)[11:] if track_size_match else None,
        "Quantity Standard": int(quantity_standard_match.group(1)) if quantity_standard_match else None,
        "Track Configuration": track_config_match.group(1).strip() if track_config_match else None,
        "Track Appearance": track_appearance_match.group(1).strip() if track_appearance_match else None,
        "Jamb Mount": jamb_mount_match.group(0)[11:] if jamb_mount_match else None,
        "Additional Selection": additional_selection_match.group(0) if additional_selection_match else None,
        "Jamb Material": jamb_material_match.group(0)[14:] if jamb_material_match else None,
        "VDS Color": vds_color_match.group(0) if vds_color_match else None,
        "Additional Customization": additional_customization_match.group(0)[25:] if additional_customization_match else None,
        "Type": type_match.group(0)[5:] if type_match else None,
        "Cyclage": cyclage_match.group(0)[8:] if cyclage_match else None,
        "Spring Count": spring_count_match.group(0)[13:] if spring_count_match else None,
        "Drum": drum_match.group(0)[5:] if drum_match else None,
        "Wire Size": wire_size_match.group(0)[10:] if wire_size_match else None,
        "Shaft": shaft_match.group(0)[6:] if shaft_match else None,
        "Spring ID": spring_id_match.group(0)[10:] if spring_id_match else None,
        "Shaft Diameter": shaft_diameter_match.group(0)[15:] if shaft_diameter_match else None,
        "Prod length": prod_length_match.group(0)[13:] if prod_length_match else None,
        "Auxilary Bearings": auxilary_bearings_match.group(0)[18:] if auxilary_bearings_match else None,
        "Spring Turns": spring_turns_match.group(0)[13:] if spring_turns_match else None,
        "Cable Size": cable_size_match.group(0)[11:] if cable_size_match else None,
        "Weight": str(round(float(''.join(filter(lambda x: x.isdigit() or x == '.', weight_match.group(0)))), 2)) + " " + weight_match.group(0).split(" ")[-1] if weight_match else None,
        "Section Bundles": tbl_dict['# Section Bundles'], 
        "Hardware Cartons": tbl_dict['# Hardware Cartons'], 
        "Track Bundles": tbl_dict['# Track Bundles'], 
        "Of Struts": tbl_dict['# of Struts'], 
        "Torsion Springs": tbl_dict['# Torsion Springs'], 
        "Feet of VDS": tbl_dict['Feet of VDS']
    }

    logger.info("Data extracted successfully from PDF")
    return data
