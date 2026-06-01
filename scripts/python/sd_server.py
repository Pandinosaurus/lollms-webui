import subprocess
from pathlib import Path

from ascii_colors import ASCIIColors
from lollms.paths import LollmsPaths

global_path = Path(__file__).parent.parent.parent / "global_paths_cfg.yaml"
ASCIIColors.yellow(f"global_path: {global_path}")
lollms_paths = LollmsPaths(global_path)
shared_folder = lollms_paths.personal_path / "shared"
sd_folder = shared_folder / "auto_sd"
output_dir = lollms_paths.personal_path / "outputs/sd"
output_dir.mkdir(parents=True, exist_ok=True)
script_path = sd_folder / "lollms_sd.bat"
output_folder = lollms_paths.personal_outputs_path / "audio_out"

ASCIIColors.red(r"")
ASCIIColors.red(r"                                                          ")
ASCIIColors.red(r"   __    _____ __    __    _____ _____       _____ ____   ")
ASCIIColors.red(r"  |  |  |     |  |  |  |  |     |   __|     |   __|    \  ")
ASCIIColors.red(r"  |  |__|  |  |  |__|  |__| | | |__   |     |__   |  |  | ")
ASCIIColors.red(r"  |_____|_____|_____|_____|_|_|_|_____|_____|_____|____/  ")
ASCIIColors.red(r"                                      |_____|             ")

ASCIIColors.red(" Forked from Auto1111's Stable diffusion api")
ASCIIColors.red(" Integration in lollms by ParisNeo using mix1009's sdwebuiapi ")


subprocess.Popen(str(script_path) + " --share", cwd=sd_folder)
