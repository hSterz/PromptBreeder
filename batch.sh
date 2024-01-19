#!/bin/bash
# Name of the job
#SBATCH -J prompt
#SBATCH --time=4:0:0
#SBATCH --output=/mnt/nas_home/hs850/PromptBreeder/output/out_%A.txt
# Number of GPU
#SBATCH --gres=gpu:1
#SBATCH --exclude=ltl-gpu01,ltl-gpu02

python main.py -mp 2 -ts 4 -e 10 -n 40 -p "Select all answers that apply. Start your answer with a list of the letters indicating the correct answer options or 'None' if there is no correct answer."