from importlib import resources
from pathlib import Path

from sonouno_lhc import data
from sonouno_lhc.lhc_data import sonify_subject
from sonouno_lhc.io import extract_subjects

DATA = resources.files(data)
OUTPUT_PATH = Path('sonouno-lhc-outputs')
OUTPUT_PATH.mkdir(exist_ok=True)


def sonify_subjects(path: Path) -> None:
    data = path.read_text().split('\n')
    for subject in extract_subjects(data):
        sound, fig = sonify_subject(subject)

        # Save the plot
        plot_path = OUTPUT_PATH / f'plot-dataset-{subject.id}.png'
        fig.savefig(plot_path, format='png')

        # Generate the wav file with the sonification
        sound_path = OUTPUT_PATH / f'sound-dataset-{subject.id}.wav'
        sound.to_wav(sound_path)


sonify_subjects(DATA / 'sonification_reduced.txt')
