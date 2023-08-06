import copy
import pywapor.se_root as se_root
from functools import partial
import types

def find_example(sources):
    for x in sources.values():
        prod = [product for product in x["products"] if "is_example" in product.keys()]
        if len(prod) >= 1:
            for pro in prod:
                if pro["is_example"]:
                    example_source = (pro["source"], pro["product_name"])
                    if isinstance(example_source[0], types.FunctionType):
                        example_source = (example_source[0].__name__, example_source[1])
                    elif isinstance(example_source[0], partial):
                        example_source = (example_source[0].func.__name__, example_source[1])
                    return example_source


def pre_et_look_levels(level = "level_1", bin_length = "DEKAD"):

    se_root_dler = partial(se_root.se_root, bin_length = bin_length, 
                            sources = level)

    level_1 = {

        "ndvi": {
            "products": [
                {
                    "source": "MODIS",
                    "product_name": "MOD13Q1.061",
                    "enhancers": "default",
                    "is_example": True
                },
                {
                    "source": "MODIS",
                    "product_name": "MYD13Q1.061",
                    "enhancers": "default",
                }
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "nearest",
            },

        "r0": {
            "products": [
                {
                    "source": "MODIS",
                    "product_name": "MCD43A3.061",
                    "enhancers": "default",
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "se_root": {
            "products": [
                {
                    "source": se_root_dler,
                    "product_name": "v2",
                    "enhancers": "default",
                },
            ],
            "composite_type": "max",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
        },

        "p": {
            "products": [
                {
                    "source": "CHIRPS",
                    "product_name": "P05",
                    "enhancers": "default",
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "z": {
            "products": [
                {
                    "source": "SRTM",
                    "product_name": "30M",
                    "enhancers": "default",
                },
            ],
            "composite_type": None,
            "temporal_interp": None,
            "spatial_interp": "bilinear",
            },

        "ra": {
            "products": [
                {
                    "source": "MERRA2",
                    "product_name": "M2T1NXRAD.5.12.4",
                    "enhancers": "default",
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "t_air": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "t_air_max": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "composite_type": "max",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "t_air_min": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "composite_type": "min",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "u2m": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "v2m": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "qv": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "p_air": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "p_air_0": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "wv": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "land_mask": {
            "products": [
                {
                    "source": "GLOBCOVER",
                    "product_name": "2009_V2.3_Global",
                    "enhancers": "default",
                },
            ],
            "composite_type": None,
            "temporal_interp": None,
            "spatial_interp": "nearest",
            },

        "rs_min": {
            "products": [
                {
                    "source": "GLOBCOVER",
                    "product_name": "2009_V2.3_Global",
                    "enhancers": "default",
                },
            ],
            "composite_type": None,
            "temporal_interp": None,
            "spatial_interp": "nearest",
            },

        "z_obst_max": {
            "products": [
                {
                    "source": "GLOBCOVER",
                    "product_name": "2009_V2.3_Global",
                    "enhancers": "default",
                },
            ],
            "composite_type": None,
            "temporal_interp": None,
            "spatial_interp": "nearest",
            },

    }

    statics = [
                'lw_offset', 'lw_slope', 'z_oro', 'rn_offset', 'rn_slope', 't_amp_year', 't_opt', 'vpd_slope',
                # 'land_mask', 'rs_min', 'z_obst_max' # NOTE generated from lulc
            ]

    for var in statics:

        level_1[var] =  {
            "products": [
                {
                    "source": "STATICS",
                    "product_name": "WaPOR2",
                    "enhancers": "default",
                },
            ],
            "composite_type": None,
            "temporal_interp": None,
            "spatial_interp": "bilinear",
        }

    level_2 = copy.deepcopy(level_1)

    level_2["ndvi"] = {

            "products": [
                {
                    "source": "PROBAV",
                    "product_name": "S5_TOC_100_m_C1",
                    "enhancers": "default",
                    "is_example": True
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "nearest",
            }

    level_2["r0"] = {

            "products": [
                {
                    "source": "PROBAV",
                    "product_name": "S5_TOC_100_m_C1",
                    "enhancers": "default",
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "nearest",
            }

    level_2_v3 = dict()

    level_2_v3["ndvi"] = {

            "products": [
                {
                    "source": "SENTINEL2",
                    "product_name": "S2MSI2A",
                    "enhancers": "default",
                    "is_example": True
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "nearest",
            }

    level_2_v3["r0"] = {

            "products": [
                {
                    "source": "SENTINEL2",
                    "product_name": "S2MSI2A",
                    "enhancers": "default",
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "nearest",
            }

    level_2_v3["se_root"] = {
            "products": [
                {
                    "source": se_root_dler,
                    "product_name": "v3",
                    "enhancers": "default",
                },
            ],
            "composite_type": "max",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
        }

    level_2_v3["p"] = {
        "products": [
            {
                "source": "CHIRPS",
                "product_name": "P05",
                "enhancers": "default",
            },
        ],
        "composite_type": "mean",
        "temporal_interp": "linear",
        "spatial_interp": "bilinear",
        }

    level_2_v3["z"] = {
        "products": [
            {
                "source": "COPERNICUS",
                "product_name": "GLO30",
                "enhancers": "default",
            },
        ],
        "composite_type": None,
        "temporal_interp": None,
        "spatial_interp": "bilinear",
        }

    for var, composite_type in [("t_air", "mean"), ("t_air_min", "min"), ("t_air_max", "max"), 
                                # ("t_dew", "mean"), # NOTE ETLook usees t_dew to calc `vp`, but that one is directly available from agERA5.
                                # ("rh", "mean"), 
                                ("u", "mean"), ("vp", "mean"), ("ra", "mean")]:
        level_2_v3[var] = {
            "products": [
                {
                    "source": "ERA5",
                    "product_name": "sis-agrometeorological-indicators",
                    "enhancers": "default",
                },
            ],
            "composite_type": composite_type,
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            }

    for var in ["p_air", "p_air_0"]:
        level_2_v3[var] = {
            "products": [
                {
                    "source": "ERA5",
                    "product_name": 'reanalysis-era5-single-levels',
                    "enhancers": "default",
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            }

    statics_v2 = [
                'z_oro', 'rn_offset', 'rn_slope', 't_amp_year', 't_opt', 'vpd_slope',
                'land_mask', 'rs_min', 'z_obst_max'
            ]

    for var in statics_v2:
        level_2_v3[var] = {
            'products': [
                {
                    'source': "STATICS",
                    'product_name': "WaPOR2",
                    'enhancers': 'default'
                },
            ],
        'composite_type': None,
        'temporal_interp': None,
        'spatial_interp': 'bilinear'}

    statics_v3 = [
                'lw_offset', 'lw_slope'
            ]

    for var in statics_v3:
        level_2_v3[var] = {
            'products': [
                {
                    'source': "STATICS",
                    'product_name': "WaPOR3",
                    'enhancers': 'default'
                },
            ],
        'composite_type': None,
        'temporal_interp': None,
        'spatial_interp': 'bilinear'}
    



    levels = {
            "level_1": level_1,
            "level_2": level_2,
            "level_2_v3": level_2_v3
                }

    return levels[level]

def pre_se_root_levels(level = "level_1"):

    level_1 = {

        "ndvi": {
            "products": [
                {
                    "source": "MODIS",
                    "product_name": "MOD13Q1.061",
                    "enhancers": "default",
                    "is_example": True,
                },
                {
                    "source": "MODIS",
                    "product_name": "MYD13Q1.061",
                    "enhancers": "default", 
                }
            ],
            "temporal_interp": "linear",
            "spatial_interp": "nearest",
            },

        "lst": {
            "products": [
                {
                    "source": "MODIS",
                    "product_name": "MOD11A1.061",
                    "enhancers": "default",
                },
                {
                    "source": "MODIS",
                    "product_name": "MYD11A1.061",
                    "enhancers": "default",
                },
            ],
            "temporal_interp": None,
            "spatial_interp": "nearest",
        },

        "t_air": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "t_air_max": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "t_air_min": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "u2m": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "v2m": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "qv": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "wv": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "p_air": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },

        "p_air_0": {
            "products": [
                {
                    "source": "GEOS5",
                    "product_name": "inst3_2d_asm_Nx",
                    "enhancers": "default",
                },
            ],
            "temporal_interp": "linear",
            "spatial_interp": "bilinear",
            },
    }

    statics = ["r0_bare", "r0_full"]

    for var in statics:

        level_1[var] =  {
            "products": [
                {
                    "source": "STATICS",
                    "product_name": "WaPOR2",
                    "enhancers": "default",
                },
            ],
            "temporal_interp": None,
            "spatial_interp": "bilinear",
        }

    level_2 = copy.deepcopy(level_1)

    level_2["ndvi"] = {

            "products": [
                {
                    "source": "PROBAV",
                    "product_name": "S5_TOC_100_m_C1",
                    "enhancers": "default",
                    "is_example": True
                },
            ],
            "composite_type": "mean",
            "temporal_interp": "linear",
            "spatial_interp": "nearest",
            }

    level_2_v3 = dict()

    level_2_v3["ndvi"] = {
        "products": [
            {
                "source": "SENTINEL2",
                "product_name": "S2MSI2A",
                "enhancers": "default",
                "is_example": True
            },
        ],
        "temporal_interp": "linear",
        "spatial_interp": "nearest"}

    level_2_v3['bt'] = {
        'products': [
            {
                'source': 'VIIRSL1',
                'product_name': 'VNP02IMG',
                'enhancers': 'default'
            },
        ],
        'temporal_interp': None,
        'spatial_interp': 'nearest'}

    for var in ["u", "t_dew", "p_air_0", "p_air", "t_air", "wv"]:
        level_2_v3[var] = {
            'products': [
                {
                    'source': 'ERA5',
                    'product_name': 'reanalysis-era5-single-levels',
                    'enhancers': 'default'
                },
            ],
        'temporal_interp': "linear",
        'spatial_interp': 'bilinear'}

    for var in ["r0_bare", "r0_full"]:
        level_2_v3[var] = {
            'products': [
                {
                    'source': "STATICS",
                    'product_name': "WaPOR2",
                    'enhancers': 'default'
                },
            ],
        'temporal_interp': "linear",
        'spatial_interp': 'bilinear'}


    levels = {
                "level_1": level_1,
                "level_2": level_2,
                "level_2_v3": level_2_v3,
                }

    return levels[level]

if __name__ == "__main__":

    et_look_sources_lvl1 = pre_et_look_levels(level = "level_1", bin_length = "DEKAD")
    et_look_sources_lvl2 = pre_et_look_levels(level = "level_2", bin_length = "DEKAD")
    et_look_sources_lvl2_v3 = pre_et_look_levels(level = "level_2_v3", bin_length = "DEKAD")

    se_root_sources_lvl1 = pre_se_root_levels(level = "level_1")
    se_root_sources_lvl2 = pre_se_root_levels(level = "level_2")
    se_root_sources_lvl2_v3 = pre_se_root_levels(level = "level_2_v3")

    