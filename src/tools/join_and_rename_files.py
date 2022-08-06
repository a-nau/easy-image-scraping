import tqdm
import shutil
from pathlib import Path
import csv


def join_and_rename_files(base_folder: Path, target_folder: Path):
    """
    Copy files from folders in a base folder form a nested structure to a one-level structure where
    the nested folder names become part of the file name.
    """
    target_folder.mkdir(exist_ok=True)
    download_info = [["Success", "URL", "Image Path/Error"]]
    for folder in tqdm.tqdm([f for f in base_folder.iterdir() if f.is_dir()]):
        for img in [
            f for f in folder.glob("*") if f.suffix in [".png", ".jpg", ".jpeg"]
        ]:
            shutil.copyfile(img, target_folder / f"{folder.name}_{img.name}")

        # Consolidate download information
        for csv_file in [f for f in folder.rglob("*.csv")]:
            with csv_file.open("r") as f:
                reader = csv.reader(f)
                lines = [
                    (
                        (
                            row[:2]
                            + [
                                row[2]
                                .replace("/usr/src/app/output/", "")
                                .replace("/", "_")
                            ]
                        )
                        if row[0].lower() == "success"
                        else row
                    )
                    for row in reader
                ]
                download_info += lines[1:]
    with (target_folder / "_links.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(download_info)


if __name__ == "__main__":
    root_dir = Path(__file__).parent.parent.parent
    join_and_rename_files(
        root_dir / "output", root_dir / "output_joined",
    )
