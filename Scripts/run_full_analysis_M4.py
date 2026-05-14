import os
import sys
import importlib.util

script_folder = os.path.dirname(os.path.abspath(__file__))
project_folder = os.path.dirname(script_folder)
os.chdir(project_folder)
sys.path.append(script_folder)

pyc_path = os.path.join(script_folder, "data_preparation_M2.cpython-311.pyc")
spec = importlib.util.spec_from_file_location("data_preparation_M2", pyc_path)
data_preparation_M2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data_preparation_M2)

download_answer_files = data_preparation_M2.download_answer_files
collate_answer_files = data_preparation_M2.collate_answer_files

from data_extraction_M1 import extract_answers_sequence, write_answers_sequence
from data_analysis_M3 import generate_means_sequence, visualize_data


def main():
    base_url = "https://raw.githubusercontent.com/fc-leeds/MATH1604_2025_2026_data/main"
    data_folder = "data"
    output_folder = "output"
    total_respondents = 64

    os.makedirs(data_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(output_folder):
        if filename.startswith("answers_list_respondent_") or filename == "collated_answers.txt":
            os.remove(os.path.join(output_folder, filename))

    print("Downloading files...")
    download_answer_files(base_url, data_folder, total_respondents)

    print("Collating files using M2...")
    collate_answer_files(data_folder)

    valid_files = []

    print("Extracting sequences using M1...")
    for i in range(1, total_respondents + 1):
        file_path = os.path.join(data_folder, f"answers_respondent_{i}.txt")

        if os.path.exists(file_path):
            answers = extract_answers_sequence(file_path)

            if len(answers) == 100:
                valid_files.append(file_path)
                write_answers_sequence(answers, i, output_folder)
            else:
                print(f"Skipped respondent {i}: {len(answers)} answers")
        else:
            print(f"Missing respondent file {i}")

    collated_path = os.path.join(output_folder, "collated_answers.txt")

    print("Creating clean collated file...")
    with open(collated_path, "w", encoding="utf-8") as output_file:
        for file_path in valid_files:
            with open(file_path, "r", encoding="utf-8") as input_file:
                output_file.write(input_file.read().strip())
            output_file.write("\n*\n")

    print("Generating means using M3...")
    means = generate_means_sequence(collated_path)
    print("First 10 means:", means[:10])

    print("Visualising using M3...")
    visualize_data(collated_path, 1)
    visualize_data(collated_path, 2)

    print("Full analysis complete.")


if __name__ == "__main__":
    main()
