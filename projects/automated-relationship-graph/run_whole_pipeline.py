from scripts.generate_crm_csvs import run_generate_crm_csvs
from scripts.build_flourish_export import run_build_flourish_export
from scripts.build_popups import run_popup_engine


def run_whole_pipeline():
    run_generate_crm_csvs()
    run_build_flourish_export()
    run_popup_engine()

if __name__ == '__main__':
    run_whole_pipeline()
