
supported_text_formats = {
    "ThunderSTORM (csv)": {
        # Required
        "type": "table",
        "extension": ".csv",
        "mode": "text",
        "dtype": "float32",
        "delimiter": ",",
        "comments": "",
        # specify which row is the header, set to -1 if there is no header
        "header_row": 0,
        # specify how to transform the headers to the standard header defined in smlm format,
        "header_transform": { "x [nm]": "x", "y [nm]": "y", "z [nm]": "z", "uncertainty_xy [nm]": "uncertainty_xy", "uncertainty_z [nm]": "uncertainty_z" },

        # Optional
        "name": "ThunderSTORM (csv)",
        "description": "a csv format used in thunderSTORM"
    },
    "ThunderSTORM (xls)": {
        # Required
        "type": "table",
        "extension": ".xls",
        "mode": "text",
        "dtype": "float32",
        "delimiter": "\t",
        "comments": "",
        # specify which row is the header, set to -1 if there is no header
        "header_row": 0,
        # specify how to transform the headers to the standard header defined in smlm format,
        "header_transform": { "x [nm]": "x", "y [nm]": "y", "z [nm]": "z", "uncertainty_xy [nm]": "uncertainty_xy", "uncertainty_z [nm]": "uncertainty_z" },

        # Optional
        "name": "ThunderSTORM (xls)",
        "description": "a xls format used in thunderSTORM"
    },
    "ZEISS (txt)": {
        # Required
        "type": "table",
        "extension": ".txt",
        "mode": "text",
        "dtype": "float32",
        "delimiter": "\t",
        "comments": "",
        # specify which row is the header, set to -1 if there is no header
        "header_row": 0,
        # specify how to transform the headers to the standard header defined in smlm format,
        "header_transform": { "Position X [nm]": "x", "Position Y [nm]": "y", "Position Z [nm]": "z", "First Frame": "frame" },

        # Optional
        "name": "ZEISS (txt)",
        "description": "a txt format used in ZEISS microscope"
    },
    "ZEISSv1 (csv)": {
        # Required
        "type": "table",
        "extension": ".csv",
        "mode": "text",
        "dtype": "float32",
        "delimiter": ";",
        "comments": "",
        # specify which row is the header, set to -1 if there is no header
        "header_row": 0,
        # specify how to transform the headers to the standard header defined in smlm format,
        "header_transform": { "Position X [nm]": "x", "Position Y [nm]": "y", "Position Z [nm]": "z", "First Frame": "frame" },

        # Optional
        "name": "ZEISSv1 (csv)",
        "description": "a csv format used in ZEISS microscope"
    },
    "ZEISSv2 (csv)": {
        # Required
        "type": "table",
        "extension": ".csv",
        "mode": "text",
        "dtype": "float32",
        "delimiter": ";",
        "comments": "",
        # specify which row is the header, set to -1 if there is no header
        "header_row": 0,
        # specify how to transform the headers to the standard header defined in smlm format,
        "header_transform": { "x [nm]": "x", "y [nm]": "y", "z [nm]": "z", "First Frame": "frame" },

        # Optional
        "name": "ZEISSv2 (csv)",
        "description": "a csv format used for ZEISS microscope"
    },
    "RapidSTORM (txt)": {
        # Required
        "type": "table",
        "extension": ".txt",
        "mode": "text",
        "dtype": "float32",
        "delimiter": " ",
        "comments": "",
        # specify which row is the header, set to -1 if there is no header
        "header_row": 0,

        # specify how to transform the headers to the standard header defined in smlm format,
        "header_transform": { "*all*": 'identifier="([\\w\\d\\-_]+)"', "Position-0-0": "x", "Position-1-0": "y", "Position-2-0": "z", "ImageNumber-0-0": "frame" },

        # Optional
        "name": "RapidSTORM (txt)",
        "description": "a text format used in RapidSTORM"
    },
    "Space Seperated List (txt)": {
        # Required
        "type": "table",
        "extension": ".txt",
        "mode": "text",
        "dtype": "float32",
        "delimiter": " ",
        "comments": "",
        # specify which row is the header, set to -1 if there is no header
        "header_row": 0,

        # specify how to transform the headers to the standard header defined in smlm format,
        "header_transform": {},

        # Optional
        "name": "Space Seperated List (txt)",
        "description": "A list of coordinates seperated with space."
    },
    "Nikon NSTORM (txt)": {
        # Required
        "type": "table",
        "extension": ".txt",
        "mode": "text",
        "dtype": "float32",
        "delimiter": "\t",
        "comments": "",
        # specify which row is the header, set to -1 if there is no header
        "header_row": 0,
        # specify how to transform the headers to the standard header defined in smlm format,
        "header_transform": { "X": "x", "Y": "y", "Z": "z", "Frame": "frame" },

        # Optional
        "name": "Nikon NSTORM (txt)",
        "description": "a txt format exported from Nikon NSTORM software"
    },
}