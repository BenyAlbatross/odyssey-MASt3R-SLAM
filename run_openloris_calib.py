import os
import subprocess
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# Path to OpenLORIS dataset root (edit if needed)
OPENLORIS_ROOT = "/home/odyssey_sharedws/DATASETS/openLORIS_png"
# Output results folder
OUTPUT_ROOT = "testtstamps_openLORIS_MAST3RSLAM_results_calib"
# Config file for MASt3R-SLAM
CONFIG = "config/eval_calib.yaml"
# Intrinsic calibration file
INTRINSIC_CALIBRATION = "config/openloris_intrinsics.yaml"

OPENLORIS_SCENES = {
    "office":   ["office1-1"], #, "office1-2", "office1-3", "office1-4", "office1-5", "office1-6", "office1-7"],
    #"corridor": ["corridor1-1"],# "corridor1-2", "corridor1-3", "corridor1-4", "corridor1-5"],
    #"home":     ["home1-1", "home1-2", "home1-3", "home1-4", "home1-5"],
    #"cafe":     ["cafe1-1", "cafe1-2"],
    #"market":   ["market1-1", "market1-2", "market1-3"]
}

for env, scenes in OPENLORIS_SCENES.items():
    for scene in scenes:
        scene_path = os.path.join(OPENLORIS_ROOT, env, scene)
        if not os.path.isdir(scene_path):
            # Skip if the scene folder does not exist
            print(f"[skip] No folder for {env}/{scene} in {OPENLORIS_ROOT}" )
            continue
        color_path = os.path.join(OPENLORIS_ROOT, env, scene, "color")
        if not os.path.isdir(color_path):
            # Skip if the color folder does not exist
            print(f"[skip] No color folder in {color_path}")
            continue
        # Prepare output folder
        save_as = os.path.join(OUTPUT_ROOT, env, scene)
        os.makedirs(save_as, exist_ok=True)
        # Run MASt3R-SLAM
        print(f"[run] {env}/{scene} (with calib)")
        cmd = [
            "python", "main.py",
            "--dataset", color_path,
            "--config", CONFIG,
            "--calib", INTRINSIC_CALIBRATION,
            "--save-as", save_as,
            "--no-viz"
        ]
        try:
            subprocess.run(cmd, check=True)
            print(f"[done] {env}/{scene} results saved to {save_as}")
        except subprocess.CalledProcessError as e:
            print(f"[error] Failed on {env}/{scene}: {e}")
print("All scenes processed (calib version).")